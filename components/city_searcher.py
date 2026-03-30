"""city_searcher.py

输入：城市名
输出：该城市 top5 区/县，以及每个区/县下的 top5 商圈名

用于驱动 workflow_manager 的“先选区/县，再选商圈，进入餐厅列表页后采集菜单”。
"""

import json
from dataclasses import dataclass
from typing import List, Dict

from components.config_manager import config_manager


@dataclass
class DistrictAreas:
    district: str
    areas: List[str]


class CityDistrictAreaSearcher:
    def __init__(self) -> None:
        self.client = config_manager.get_client()

    def search(self, city: str, top_district: int = 5, top_area_per_district: int = 5) -> List[Dict]:
        """调用 LLM 生成结构化检索结果。

        返回格式示例：
        [
          {"district": "徐汇区", "areas": ["徐家汇商圈", "衡山路商圈", ...]},
          {"district": "...", "areas": ["...", ...]}
        ]
        """

        prompt = f"""
你是美团/外卖商圈数据规划助手。
请根据城市名，输出该城市中：
1) top{top_district} 个常见的区/县（行政区口径），
2) 对于每个区/县，给出该区/县内 top{top_area_per_district} 个“本地特色突出”的区域/地点名称。

要求：
- 只输出名称，不要输出解释。
- district/areas 去重。
- areas 不限于“商圈”，也可以是：
  - 片区/街区/路段（如：XX路、XX街道、XX片区）
  - 地标周边（如：XX广场、XX公园、XX交通枢纽）
  - 热门生活圈/园区（如：XX科创园、XX大学城周边）
  - 若确实以“商圈”称呼为主，也允许用“XX商圈”。
- areas 需要满足：在美团搜索栏可直接输入并触发对应区域餐厅列表。
- 输出必须是严格 JSON（不能包含 ``` 包裹）。

城市：{city}

输出 JSON 形式：
[
  {{"district": "...", "areas": ["...", "..."]}},
  {{"district": "...", "areas": ["...", "..."]}}
]
"""

        response = self.client.chat.completions.create(
            model="google/gemini-3.1-flash-lite-preview",
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content
        content = content.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(content)

        # 最简单的结构校验/清洗
        cleaned: List[Dict] = []
        for item in parsed[:top_district]:
            district = str(item.get("district", "")).strip()
            areas = item.get("areas", [])
            if not district:
                continue
            if not isinstance(areas, list):
                areas = []
            area_names = [str(a).strip() for a in areas if str(a).strip()]
            cleaned.append({"district": district, "areas": area_names[:top_area_per_district]})
        return cleaned


city_district_area_searcher = CityDistrictAreaSearcher()
