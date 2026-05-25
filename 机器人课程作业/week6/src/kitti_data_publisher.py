import os
import time

import cv2
import numpy as np


class KittiDataReader:
    """KITTI 图像和点云数据读取示例"""

    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.image_dir = os.path.join(dataset_path, "image_2")
        self.velodyne_dir = os.path.join(dataset_path, "velodyne")

    def read_image(self, index):
        image_path = os.path.join(self.image_dir, f"{index:06d}.png")
        image = cv2.imread(image_path)

        if image is None:
            print(f"图像读取失败: {image_path}")
            return None

        print(f"图像读取成功: {image_path}, shape={image.shape}")
        return image

    def read_pointcloud(self, index):
        point_path = os.path.join(self.velodyne_dir, f"{index:06d}.bin")

        if not os.path.exists(point_path):
            print(f"点云文件不存在: {point_path}")
            return None

        points = np.fromfile(point_path, dtype=np.float32).reshape(-1, 4)
        print(f"点云读取成功: {point_path}, points={points.shape[0]}")
        return points


def main():
    dataset_path = "KITTI"
    reader = KittiDataReader(dataset_path)

    print("开始读取 KITTI 数据...")

    for index in range(3):
        image = reader.read_image(index)
        points = reader.read_pointcloud(index)

        if image is not None:
            cv2.imwrite(f"output_image_{index:06d}.png", image)

        if points is not None:
            print("前 5 个点云数据:")
            print(points[:5])

        time.sleep(0.5)

    print("KITTI 数据读取示例运行结束")


if __name__ == "__main__":
    main()
