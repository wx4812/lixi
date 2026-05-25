import math


class TwoLinkArm:
    """二维两连杆机械臂运动学计算"""

    def __init__(self, link1=1.0, link2=1.0):
        self.link1 = link1
        self.link2 = link2

    def forward_kinematics(self, theta1_deg, theta2_deg):
        theta1 = math.radians(theta1_deg)
        theta2 = math.radians(theta2_deg)

        x = self.link1 * math.cos(theta1) + self.link2 * math.cos(theta1 + theta2)
        y = self.link1 * math.sin(theta1) + self.link2 * math.sin(theta1 + theta2)

        return x, y

    def inverse_kinematics(self, x, y):
        distance = math.sqrt(x ** 2 + y ** 2)

        cos_theta2 = (
            (distance ** 2 - self.link1 ** 2 - self.link2 ** 2)
            / (2 * self.link1 * self.link2)
        )

        if cos_theta2 < -1 or cos_theta2 > 1:
            return None

        theta2 = math.acos(cos_theta2)

        k1 = self.link1 + self.link2 * math.cos(theta2)
        k2 = self.link2 * math.sin(theta2)

        theta1 = math.atan2(y, x) - math.atan2(k2, k1)

        return math.degrees(theta1), math.degrees(theta2)


def main():
    arm = TwoLinkArm(link1=1.0, link2=1.0)

    theta1 = 30
    theta2 = 45

    print("二维两连杆机械臂运动学验证")
    print(f"输入关节角度: theta1={theta1}°, theta2={theta2}°")

    x, y = arm.forward_kinematics(theta1, theta2)

    print(f"正运动学计算结果: x={x:.3f}, y={y:.3f}")

    ik_result = arm.inverse_kinematics(x, y)

    if ik_result is None:
        print("逆运动学求解失败: 目标点超出机械臂工作空间")
    else:
        ik_theta1, ik_theta2 = ik_result
        print(f"逆运动学验证结果: theta1={ik_theta1:.3f}°, theta2={ik_theta2:.3f}°")


if __name__ == "__main__":
    main()
