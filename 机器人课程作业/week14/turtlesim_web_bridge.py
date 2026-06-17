#!/usr/bin/env python3
"""
Week 14 - Direction B: turtlesim WebSocket Bridge
Combines ROS2 node + maze collision + WebSocket server in ONE resident program.
"""

import asyncio
import json
import math
import threading
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import TeleportAbsolute

from aiohttp import web
import aiohttp
from pathlib import Path

# ──────────────────────────────────────────────
# Maze Definition (4×4 perfect maze, verified solvable by BFS)
# Each obstacle: (x, y, w, h)  — x,y = bottom-left corner, w/h = width/height
# Coordinate space: turtlesim 0~11
# ──────────────────────────────────────────────
WORLD_MIN = 0.5
WORLD_MAX = 10.5

OBSTACLES = [
    # Outer walls
    (0.5,  0.5,  10.0, 0.2),   # bottom
    (0.5,  10.3, 10.0, 0.2),   # top
    (0.5,  0.5,  0.2,  10.0),  # left
    (10.3, 0.5,  0.2,  10.0),  # right
    # Inner maze walls
    (3.0,  0.5,  0.2,  4.5),
    (3.0,  7.0,  0.2,  3.5),
    (5.5,  2.5,  0.2,  5.0),
    (5.5,  9.0,  0.2,  1.5),
    (8.0,  0.5,  0.2,  3.5),
    (8.0,  5.5,  0.2,  5.0),
    (1.5,  3.0,  2.0,  0.2),
    (4.5,  3.0,  1.5,  0.2),
    (1.5,  6.0,  4.5,  0.2),
    (6.5,  6.0,  1.5,  0.2),
    (3.5,  8.5,  2.5,  0.2),
    (6.5,  8.5,  1.5,  0.2),
    (6.5,  4.5,  2.0,  0.2),
    (9.0,  4.5,  1.5,  0.2),
    (1.5,  9.0,  1.5,  0.2),
]

START_POS  = (1.2, 1.2)
GOAL_POS   = (9.8, 9.8)
GOAL_RADIUS = 0.6
TURTLE_RADIUS = 0.35

MOVE_SPEED    = 2.0   # linear velocity (m/s)
TURN_SPEED    = 1.8   # angular velocity (rad/s)


# ──────────────────────────────────────────────
# Collision helpers
# ──────────────────────────────────────────────
def _circle_rect_collision(cx, cy, r, ox, oy, ow, oh):
    """True if circle (cx,cy,r) overlaps rectangle."""
    nearest_x = max(ox, min(cx, ox + ow))
    nearest_y = max(oy, min(cy, oy + oh))
    dx = cx - nearest_x
    dy = cy - nearest_y
    return (dx * dx + dy * dy) < (r * r)


def would_hit_obstacle(nx, ny):
    for (ox, oy, ow, oh) in OBSTACLES:
        if _circle_rect_collision(nx, ny, TURTLE_RADIUS, ox, oy, ow, oh):
            return True
    return False


def is_inside_goal(x, y):
    dx = x - GOAL_POS[0]
    dy = y - GOAL_POS[1]
    return math.sqrt(dx * dx + dy * dy) < GOAL_RADIUS


# ──────────────────────────────────────────────
# Shared state between ROS2 thread and asyncio thread
# ──────────────────────────────────────────────
class RobotState:
    def __init__(self):
        self.x = START_POS[0]
        self.y = START_POS[1]
        self.theta = 0.0
        self.blocked = False
        self.block_reason = ""
        self.goal_reached = False
        self.trajectory = [list(START_POS)]
        self.lock = threading.Lock()
        # command from web / auto-explorer
        self.linear = 0.0
        self.angular = 0.0
        self.auto_mode = False

state = RobotState()


# ──────────────────────────────────────────────
# ROS2 Node
# ──────────────────────────────────────────────
class TurtleBridge(Node):
    def __init__(self):
        super().__init__('turtle_web_bridge')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self._pose_cb, 10)
        self.teleport_cli = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.timer = self.create_timer(0.05, self._control_loop)  # 20 Hz

        # Wait for teleport service
        while not self.teleport_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for turtlesim...')

        # Teleport to start
        self._teleport(START_POS[0], START_POS[1], 0.0)

    def _pose_cb(self, msg):
        with state.lock:
            state.x = msg.x
            state.y = msg.y
            state.theta = msg.theta
            # Record trajectory (downsample)
            traj = state.trajectory
            if len(traj) == 0 or math.hypot(msg.x - traj[-1][0], msg.y - traj[-1][1]) > 0.15:
                traj.append([round(msg.x, 2), round(msg.y, 2)])
                if len(traj) > 500:
                    traj.pop(0)

    def _control_loop(self):
        with state.lock:
            if state.goal_reached:
                self._stop()
                return

            linear  = state.linear
            angular = state.angular
            x, y, theta = state.x, state.y, state.theta

        dt = 0.05
        # Predict next position
        nx = x + linear * math.cos(theta) * dt
        ny = y + linear * math.sin(theta) * dt

        blocked = False
        reason = ""
        if linear != 0.0 and would_hit_obstacle(nx, ny):
            linear = 0.0
            blocked = True
            reason = "obstacle"

        # Publish
        twist = Twist()
        twist.linear.x  = float(linear)
        twist.angular.z = float(angular)
        self.pub.publish(twist)

        with state.lock:
            state.blocked = blocked
            state.block_reason = reason
            if is_inside_goal(x, y):
                state.goal_reached = True

    def _stop(self):
        self.pub.publish(Twist())

    def _teleport(self, x, y, theta):
        req = TeleportAbsolute.Request()
        req.x = float(x)
        req.y = float(y)
        req.theta = float(theta)
        self.teleport_cli.call_async(req)

    def reset(self):
        with state.lock:
            state.goal_reached = False
            state.blocked = False
            state.trajectory = [list(START_POS)]
            state.linear = 0.0
            state.angular = 0.0
            state.auto_mode = False
        self._teleport(START_POS[0], START_POS[1], 0.0)


ros_node: TurtleBridge = None


# ──────────────────────────────────────────────
# Auto-Explorer integration
# ──────────────────────────────────────────────
explorer_instance = None

def get_explorer():
    global explorer_instance
    if explorer_instance is None:
        from explorer import WallFollower
        explorer_instance = WallFollower()
    return explorer_instance


# ──────────────────────────────────────────────
# WebSocket clients
# ──────────────────────────────────────────────
clients = set()


def build_state_msg():
    with state.lock:
        return json.dumps({
            "x": round(state.x, 3),
            "y": round(state.y, 3),
            "theta": round(state.theta, 3),
            "blocked": state.blocked,
            "block_reason": state.block_reason,
            "goal_reached": state.goal_reached,
            "auto_mode": state.auto_mode,
            "trajectory": state.trajectory[-100:],  # last 100 points
            "obstacles": OBSTACLES,
            "start": list(START_POS),
            "goal": list(GOAL_POS),
            "goal_radius": GOAL_RADIUS,
            "world_min": WORLD_MIN,
            "world_max": WORLD_MAX,
        })


async def ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    clients.add(ws)
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                mtype = data.get("type", "")

                if mtype == "command":
                    with state.lock:
                        if not state.goal_reached and not state.auto_mode:
                            state.linear  = float(data.get("linear",  0.0))
                            state.angular = float(data.get("angular", 0.0))

                elif mtype == "stop":
                    with state.lock:
                        if not state.auto_mode:
                            state.linear  = 0.0
                            state.angular = 0.0

                elif mtype == "auto":
                    with state.lock:
                        state.auto_mode = not state.auto_mode
                        state.linear  = 0.0
                        state.angular = 0.0
                    if state.auto_mode:
                        get_explorer().reset()

                elif mtype == "reset":
                    if ros_node:
                        ros_node.reset()
                    explorer_instance and explorer_instance.reset()

            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
    finally:
        clients.discard(ws)
    return ws


async def index_handler(request):
    html_path = Path(__file__).parent / "index.html"
    return web.FileResponse(html_path)


async def broadcast_loop():
    """Push state to all WebSocket clients at 10 Hz."""
    while True:
        await asyncio.sleep(0.1)
        if clients:
            msg = build_state_msg()
            dead = set()
            for ws in clients:
                try:
                    await ws.send_str(msg)
                except Exception:
                    dead.add(ws)
            clients -= dead


async def auto_explorer_loop():
    """Run auto-explorer at ~10 Hz when auto_mode is on."""
    while True:
        await asyncio.sleep(0.1)
        with state.lock:
            auto = state.auto_mode
            goal = state.goal_reached
            s = {
                "x": state.x, "y": state.y,
                "theta": state.theta,
                "blocked": state.blocked,
            }
        if auto and not goal:
            try:
                exp = get_explorer()
                linear, angular = exp.decide(s)
                with state.lock:
                    state.linear  = linear
                    state.angular = angular
            except Exception as e:
                print(f"[Explorer error] {e}")


def ros_spin_thread():
    rclpy.spin(ros_node)


async def main():
    global ros_node
    rclpy.init()
    ros_node = TurtleBridge()

    # Run ROS2 spin in background thread
    t = threading.Thread(target=ros_spin_thread, daemon=True)
    t.start()

    app = web.Application()
    app.router.add_get("/",    index_handler)
    app.router.add_get("/ws",  ws_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

    print("=" * 50)
    print(" Turtle Web Bridge started!")
    print(" Open on phone: http://<Tailscale_IP>:8080")
    print("=" * 50)

    await asyncio.gather(
        broadcast_loop(),
        auto_explorer_loop(),
    )


if __name__ == "__main__":
    asyncio.run(main())
