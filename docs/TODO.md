# TODO: v2.0 城市→区县→商圈采集改造

## 目标
在保持现有 `workflow_manager` 入口“餐厅列表页采集逻辑”不变的前提下，增加：
1) `city` 输入参数
2) LLM 搜索生成 `区/县` 与 `商圈` 列表（top5 口径）
3) workflow 逐个区/县+商圈导航并复用菜单采集
4) 写入结果 `restaurants.json` 增加 `city` 字段

## 待办事项（先写清单，不执行）
- [x] Update 数据结构文档：在 `docs/DATA_FORMAT.md` 的 `restaurant_info.json` 增加 `city` 字段
- [x] 同步写入链路：确保写入 `D:/crawler/data/restaurants.json` 的每条记录都带上 `city`
- [x] 新增 `components/searcher` 组件（LLM）：
  - [ ] 输入：city（字符串）
  - [ ] 输出：`区/县` top5 + 每个区/县的 `商圈` top5
  - [ ] 只输出结构化 JSON，不输出解释
- [x] 新增（或完善）导航组件：
  - [ ] 组件接收 `district` + `area`，在美团“首页-美食”顶部搜索栏输入并跳转到对应列表页
  - [ ] 由于坐标依赖真机页面，先用占位坐标，后续通过探针确认
- [x] 修改 `workflow_manager`：
  - [ ] 接口增加入参 `city`（并允许区/县+商圈由 searcher 生成）
  - [ ] 对每个 district->area：调用导航组件后，复用现有餐厅列表采集逻辑
- [ ] 更新/新增测试（不执行，仅写出测试思路/脚本骨架）：
  - [ ] 测试 searcher：mock LLM 返回值，校验 JSON 解析与裁剪 top5
  - [ ] 测试 workflow_manager：mock location_navigator + restaurant_detector + menu_detector，校验调用顺序与 `city` 写入
- [ ] 联合测试（人工执行）：
  - [ ] 单 city 小范围（top1/top1）验证：city->区/县->商圈->餐厅列表->菜单识别->写入 restaurants.json
  - [ ] 再逐步扩展到 top5

## 备注
- 目前 `crawler` 侧工作流仍需在本地真机（ADB）上完成长任务触发；云函数端暂不直接承接 ADB 爬取。
