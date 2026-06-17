#!/usr/bin/env python3
"""
Week 14 - Auto Explorer: Right-Hand Wall Follower
For a perfect maze (single solution path), the right-hand rule always reaches the goal.

How it works:
  1. Try to turn RIGHT and move forward → if not blocked, do it
  2. Else try to move FORWARD → if not blocked, do it
  3. Else try to turn LEFT and move forward
  4. Else turn AROUND (blocked on all sides)

State machine: FORWARD → CHECK_RIGHT → TURN_LEFT → TURN_BACK
"""

import math
import time


MOVE_SPEED   = 2.0    # m/s — must match bridge
TURN_SPEED   = 1.8    # rad/s
CELL_SIZE    = 2.5    # approx corridor width in turtlesim coords

# How long (seconds) to execute each phase
TURN_90_TIME  = (math.pi / 2) / TURN_SPEED     # ~0.87 s
TURN_180_TIME = math.pi / TURN_SPEED            # ~1.74 s
FORWARD_TIME  = CELL_SIZE / MOVE_SPEED          # ~1.25 s


class WallFollower:
    """
    Right-hand wall follower.
    Call decide(state) at ~10 Hz; returns (linear, angular).
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self._phase      = "check_right"   # check_right | turn_right | forward | turn_left | turn_back
        self._phase_start = time.time()
        self._stuck_count = 0
        self._last_pos    = None
        self._blocked_streak = 0

    # ── Public API ──────────────────────────────────
    def decide(self, robot_state: dict):
        """
        Parameters
        ----------
        robot_state : dict with keys x, y, theta, blocked

        Returns
        -------
        (linear, angular)  values to send to bridge
        """
        now     = time.time()
        elapsed = now - self._phase_start
        blocked = robot_state.get("blocked", False)

        linear  = 0.0
        angular = 0.0

        # ── Phase: check_right ─────────────────────
        if self._phase == "check_right":
            # Start turning right to probe
            self._go_to("turn_right", now)

        # ── Phase: turn_right ──────────────────────
        elif self._phase == "turn_right":
            angular = -TURN_SPEED   # turn right (CW = negative angular in ROS)
            if elapsed >= TURN_90_TIME:
                self._go_to("forward_right_probe", now)

        # ── Phase: forward_right_probe ─────────────
        elif self._phase == "forward_right_probe":
            linear = MOVE_SPEED
            if blocked:
                # Right side blocked → undo right turn (turn left back)
                self._go_to("undo_right_turn", now)
            elif elapsed >= FORWARD_TIME * 0.3:
                # Right is open → commit and keep going right
                self._go_to("forward", now)

        # ── Phase: undo_right_turn ─────────────────
        elif self._phase == "undo_right_turn":
            angular = TURN_SPEED    # turn left to undo
            if elapsed >= TURN_90_TIME:
                self._go_to("forward", now)

        # ── Phase: forward ─────────────────────────
        elif self._phase == "forward":
            linear = MOVE_SPEED
            if blocked:
                self._blocked_streak += 1
                if self._blocked_streak > 3:
                    # Truly stuck — turn left
                    self._go_to("turn_left", now)
                    self._blocked_streak = 0
                else:
                    self._go_to("check_right", now)
            else:
                self._blocked_streak = 0
                if elapsed >= FORWARD_TIME:
                    # After moving one cell, check right again
                    self._go_to("check_right", now)

        # ── Phase: turn_left ───────────────────────
        elif self._phase == "turn_left":
            angular = TURN_SPEED
            if elapsed >= TURN_90_TIME:
                self._go_to("forward", now)

        # ── Phase: turn_back (180°) ────────────────
        elif self._phase == "turn_back":
            angular = TURN_SPEED
            if elapsed >= TURN_180_TIME:
                self._go_to("check_right", now)

        return (linear, angular)

    # ── Helpers ─────────────────────────────────────
    def _go_to(self, phase, now):
        self._phase       = phase
        self._phase_start = now
