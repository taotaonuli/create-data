#!/usr/bin/env python3
"""
create_desktop_folder_by_date.py

功能：
  在桌面上自动创建一个以当天日期命名的文件夹（默认格式：YYYY-MM-DD）。
  若桌面不存在，会自动使用用户主目录。
  如果文件夹已存在，不会报错。

可选参数：
  --date YYYY-MM-DD   指定日期（默认：今天）
  --format "%Y%m%d"   自定义日期格式
  --dry-run           只打印要创建的路径，不实际创建

示例：
  python create_desktop_folder_by_date.py
  python create_desktop_folder_by_date.py --date 2025-11-04
  python create_desktop_folder_by_date.py --format "%Y%m%d"
"""

import argparse
import datetime
import os
from pathlib import Path

# 常见桌面路径（多语言兼容）
COMMON_DESKTOP_DIRS = [
    Path.home() / "D:\桌面",
]


def find_desktop_path() -> Path:
    """自动检测桌面路径"""
    for p in COMMON_DESKTOP_DIRS:
        if p.exists():
            return p
    return Path.home()  # 找不到就退回用户主目录


def make_folder_for_date(target_dir: Path, date: datetime.date, fmt: str, dry_run: bool):
    """创建日期文件夹"""
    folder_name = date.strftime(fmt)
    folder_path = target_dir / folder_name

    if dry_run:
        print(f"[dry-run] 将创建文件夹: {folder_path}")
        return folder_path

    folder_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ 文件夹已创建（或已存在）: {folder_path}")
    return folder_path


def main():
    parser = argparse.ArgumentParser(description="在桌面上创建一个以日期命名的文件夹")
    parser.add_argument("--date", "-d", help="指定日期 (YYYY-MM-DD)", default=None)
    parser.add_argument("--format", "-f", help="日期格式（默认：%%m.%%d）", default="%m.%d")
    parser.add_argument("--dry-run", action="store_true", help="只显示路径，不实际创建")
    args = parser.parse_args()

    # 确定桌面路径
    desktop_path = find_desktop_path()

    # 解析日期
    if args.date:
        try:
            date_obj = datetime.datetime.strptime(args.date, "%m.%d").date()
        except ValueError:
            print("❌ 日期格式错误，应为 YYYY-MM-DD")
            return
    else:
        date_obj = datetime.date.today()

    # 创建文件夹
    make_folder_for_date(desktop_path, date_obj, fmt=args.format, dry_run=args.dry_run)


if __name__ == "__main__":
    main()