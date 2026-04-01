"""main.py

仿照 tests/workflow_run_test.py 的真实 ADB WorkflowManager 流程：
1) 抓取并生成中间产物到 D:\\crawler\\data\\unclean_<city>.json
   （扩展名为 .json，但内容是“每行一个 JSON 对象”的 JSONL-like 格式）
2) 调用 clean_data.py 进行清洗：输出 D:\\crawler\\data\\<city>.jsonl
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("city", nargs="?", default="上海", help="城市名")
    parser.add_argument(
        "--top-district",
        type=int,
        default=int(os.environ.get("TOP_DISTRICT", "5")),
        help="top_district（区/县数量）",
    )
    parser.add_argument(
        "--top-area-per-district",
        type=int,
        default=int(os.environ.get("TOP_AREA", "5")),
        help="top_area_per_district（每个区的商圈数量）",
    )
    parser.add_argument(
        "--skip-clean",
        action="store_true",
        help="只跑抓取 workflow，不跑 clean_data",
    )
    args = parser.parse_args()

    # 兼容在 d:\crawler 下直接运行的场景
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "")))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    from components.workflow_manager import WorkflowManager

    out_dir = r"D:\\crawler\\data"
    os.makedirs(out_dir, exist_ok=True)

    city = args.city
    unclean_path = os.path.join(out_dir, f"unclean_{city}.json")
    clean_path = os.path.join(out_dir, f"{city}.jsonl")

    # 清空中间产物文件
    with open(unclean_path, "w", encoding="utf-8") as f:
        f.write("")

    wm = WorkflowManager(output_file=unclean_path)
    print(
        f"[main] start city={city}, top_district={args.top_district}, top_area_per_district={args.top_area_per_district}"
    )

    wm.run(
        city=city,
        top_district=args.top_district,
        top_area_per_district=args.top_area_per_district,
        districts=None,
        dry_run=False,
    )
    print(f"[main] workflow done. unclean_output={unclean_path}")

    if args.skip_clean:
        return

    # 调用 clean_data.py：输出文件名直接为 <city>.jsonl
    clean_script = os.path.join(os.path.dirname(__file__), "clean_data.py")
    cmd = [
        sys.executable,
        clean_script,
        "--input",
        unclean_path,
        "--output",
        clean_path,
    ]
    print(f"[main] cleaning... cmd={' '.join(cmd)}")
    subprocess.check_call(cmd)
    print(f"[main] cleaning done. clean_output={clean_path}")


if __name__ == "__main__":
    main()
