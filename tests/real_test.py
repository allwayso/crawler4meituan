import sys
import os
import time

# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from components.location_navigator import LocationNavigator
from components.city_searcher import city_district_area_searcher


def main():
    """city_searcher + location_navigator 联合测试：
    1) 输入 city，调用 LLM 得到结构化 JSON（district + areas）
    2) 从 JSON 清洗出一条 {district, area}
    3) 调用 location_navigator.search(district, area)

    你可在命令行传参：
      python tests/real_test.py 上海
    """

    import sys

    city = sys.argv[1] if len(sys.argv) > 1 else "上海"
    top_district = 5
    top_area_per_district = 5

    print(f"正在执行 city_searcher + location_navigator 联合测试... city={city}")

    # 1) city_searcher 输出 JSON 计划
    plan = city_district_area_searcher.search(
        city=city,
        top_district=top_district,
        top_area_per_district=top_area_per_district,
    )
    print("\n[city_searcher] raw plan:")
    print(plan)

    if not plan:
        raise RuntimeError("city_searcher 返回为空，无法进行 location navigator 测试")

    # 2) 遍历 city_searcher 的 JSON 计划：district + areas
    #    每次导航之间 sleep(1)
    nav = LocationNavigator()
    for i, item in enumerate(plan):
        district = str(item.get("district", "")).strip()
        areas = item.get("areas", [])
        if not district:
            continue
        if not isinstance(areas, list):
            continue

        for j, area_raw in enumerate(areas):
            area = str(area_raw).strip()
            if not area:
                continue

            print(f"\n[loop {i}-{j}] district={district}, area={area}")

            nav.search(
                district=district,
                area=area,
                select_first=False,
            )

            time.sleep(1)

    print("\n测试完成。")


if __name__ == '__main__':
    main()
