import math
import time


class SimpleRobot:
    """简易二维机器人运动仿真"""

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

    def move(self, linear_velocity, angular_velocity, dt):
        self.x += linear_velocity * math.cos(self.theta) * dt
        self.y += linear_velocity * math.sin(self.theta) * dt
        self.theta += angular_velocity * dt

    def print_state(self):
        print(
            f"x: {self.x:.2f}, "
            f"y: {self.y:.2f}, "
            f"theta: {self.theta:.2f}"
        )


def main():
    robot = SimpleRobot()

    linear_velocity = 0.2
    angular_velocity = 0.5
    dt = 0.1

    print("开始简易机器人运动仿真...")

    for _ in range(50):
        robot.move(linear_velocity, angular_velocity, dt)
        robot.print_state()
        time.sleep(dt)

    print("仿真结束")


if __name__ == "__main__":
    main()
