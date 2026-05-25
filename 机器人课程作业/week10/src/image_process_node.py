from pathlib import Path

import cv2


def process_image(input_path, output_path):
    image = cv2.imread(str(input_path))

    if image is None:
        print(f"图像读取失败: {input_path}")
        return False

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    cv2.imwrite(str(output_path), edges)

    print(f"图像读取成功: {input_path}")
    print(f"处理结果已保存: {output_path}")
    return True


def main():
    root = Path(__file__).resolve().parents[1]
    input_path = root / "img" / "input.png"
    output_path = root / "img" / "result.png"

    process_image(input_path, output_path)


if __name__ == "__main__":
    main()
