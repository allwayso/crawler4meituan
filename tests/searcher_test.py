import sys
import os
import json


# 添加项目根目录到 sys.path（确保能 import components/*）
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.city_searcher import city_district_area_searcher


def main():
    # 允许传参：python tests/searcher_test.py 上海
    city = sys.argv[1] if len(sys.argv) > 1 else "武汉"
    print(f"[searcher_test] city={city}")

    result = city_district_area_searcher.search(city=city, top_district=5, top_area_per_district=5)
    print("[searcher_test] raw result:")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
