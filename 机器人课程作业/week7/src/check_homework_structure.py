from pathlib import Path


def check_week_folder(week_path):
    print(f"\n检查目录: {week_path}")

    readme = week_path / "README.md"
    img_dir = week_path / "img"
    src_dir = week_path / "src"

    if readme.exists():
        print("[OK] README.md 存在")
    else:
        print("[缺失] README.md 不存在")

    if img_dir.exists():
        images = list(img_dir.glob("*"))
        print(f"[OK] img 目录存在，包含 {len(images)} 个文件")
    else:
        print("[缺失] img 目录不存在")

    if src_dir.exists():
        src_files = list(src_dir.glob("*"))
        print(f"[OK] src 目录存在，包含 {len(src_files)} 个文件")
    else:
        print("[提示] src 目录不存在")


def main():
    root = Path(".")

    week_folders = sorted(
        path for path in root.iterdir()
        if path.is_dir() and path.name.startswith("week")
    )

    if not week_folders:
        print("未找到 week 目录，请在课程作业根目录运行本脚本")
        return

    print("开始检查课程作业目录结构...")

    for week_path in week_folders:
        check_week_folder(week_path)

    print("\n检查完成")


if __name__ == "__main__":
    main()
