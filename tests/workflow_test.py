"""workflow_test.py

目的：真实测试 WorkflowManager._collect_for_current_restaurant_list

使用方式：
  1) 确保手机端已经进入“某个城市/区/商圈”的餐厅列表页（即可开始点“餐厅->菜品->菜单->写入”）
  2) 运行：
       python tests/workflow_test.py 上海

注意：该测试会执行真实 ADB 操作（会写入 restaurants.json / 指定输出文件）。
"""

import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.workflow_manager import WorkflowManager


def main():
    city = sys.argv[1] if len(sys.argv) > 1 else "上海"
    output_file = "D:/crawler/data/restaurants_test.json"

    # 可选：先清空输出文件，避免混入旧数据
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("")
    except Exception:
        # 不影响主流程
        pass

    wm = WorkflowManager(output_file=output_file)

    print(f"[workflow_test] start _collect_for_current_restaurant_list, city={city}")
    wm._collect_for_current_restaurant_list(city=city)
    print("[workflow_test] done")


if __name__ == "__main__":
    main()
