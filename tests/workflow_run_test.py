"""workflow_run_test.py

目的：真实ADB测试 WorkflowManager.run()。

会执行：
1) city_district_area_searcher（LLM）生成 city -> district -> areas 计划
2) 通过 LocationNavigator 在美团首页输入 district + area，进入对应“餐厅列表页”
3) 调用 _collect_for_current_restaurant_list()，抓取每家餐厅的菜单并写入输出文件

强烈建议：为了避免跑太久/写入太多数据，默认限制 top_district=1、top_area_per_district=1。

运行方式（真机 + ADB + 美团首页可输入）：
  python tests/workflow_run_test.py 上海
"""

import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.workflow_manager import WorkflowManager


def main():
    city = sys.argv[1] if len(sys.argv) > 1 else "上海"

    # 为了避免和其他测试混写，单独建一个文件
    output_file = "D:/crawler/data/restaurants_workflow_run_test.json"

    # 完整流程：5 个区 x 5 个 areas
    top_district = 5
    top_area_per_district = 5

    # 可选：允许通过环境变量覆盖
    #   TOP_DISTRICT=2 TOP_AREA=3 python tests/workflow_run_test.py 上海
    top_district = int(os.environ.get("TOP_DISTRICT", top_district))
    top_area_per_district = int(os.environ.get("TOP_AREA", top_area_per_district))

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("")

    wm = WorkflowManager(output_file=output_file)

    print(f"[workflow_run_test] start city={city}, top_district={top_district}, top_area_per_district={top_area_per_district}")
    wm.run(
        city=city,
        top_district=top_district,
        top_area_per_district=top_area_per_district,
        districts=None,
        dry_run=False,
    )
    print(f"[workflow_run_test] done. output={output_file}")


if __name__ == "__main__":
    main()
