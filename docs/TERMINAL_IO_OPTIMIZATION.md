# 终端 IO 最小化优化文档（Crawler 组件）

> 目标：尽可能减少终端输出（print / OCR DEBUG），以降低 IO 开销、提升跑批稳定性。
> 原则：
> 1) **错误/异常信息必须打印**（便于定位与回溯）；
> 2) 非关键流程日志默认不打印；
> 3) 所有 debug/verbose 日志必须可关闭；
> 4) OCR 框架自身的 DEBUG 日志默认关闭。

---

## 1. 需要重点处理的“噪声来源”清单

### 1.1 `components/adb_utils.py`：必现频繁 print（强烈建议默认关闭）

文件：`d:/crawler/components/adb_utils.py`

当前存在的会频繁刷屏/带来 IO 开销的打印包括：

1) `tap`
- 当前：`print(f"Executing tap at {x}, {y}")`
- 建议：改为 `DEBUG` 日志，默认关闭。

2) `swipe`
- 当前：`print(f"Executing swipe from ({x1}, {y1}) to ({x2}, {y2})")`
- 建议：改为 `DEBUG` 日志，默认关闭。

3) `input_text`
- 当前：`print(f"正在发送 Base64 编码内容: {text}")`
- 问题：传入 `text` 可能很长，终端 IO 成本高。
- 建议：
  - 默认关闭（DEBUG 才允许）；
  - 或只打印长度：`len(text)`，避免明文输出。

4) `press_keyevent`
- 当前：`print(f"Executing keyevent: {keyevent}")`
- 建议：DEBUG 日志，默认关闭。

5) `screenshot(filename)`
- 当前：`print(f"Screenshot saved to {filename}")`
- 建议：
  - 如果 filename 不为空才打印；
  - 默认关闭或降级到 DEBUG。

6) `run_adb()` 的错误打印
- 当前：`print(f"ADB Error: {result.stderr}")`
- 建议：保留为**错误级**输出（只在 returncode != 0 时打印），这符合“报错信息必须打印”。

---

### 1.2 OCR 框架 Debug：`ppocr DEBUG: dt_boxes num : ...`

你观察到的形如：
`[2026/03/31 14:57:50] ppocr DEBUG: dt_boxes num : 31, elapsed : ...`

这通常来自 PaddleOCR 内部日志输出。

当前代码中 PaddleOCR 初始化参数：
- `components/restaurant_detector.py`
- `components/menu_detector.py`
- `components/element_detector.py`

它们目前是：
```py
PaddleOCR(use_angle_cls=True, lang='ch')
```

建议改为：
```py
PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
```

这样可直接关闭 PaddleOCR 的日志（包含 dt_boxes 等 DEBUG）。

---

### 1.3 `components/workflow_manager.py`：流程日志过多

文件：`d:/crawler/components/workflow_manager.py`

当前存在较多 `print`，包括：

1) 总体流程
- `print("Workflow started...")`
- `print(f"Plan: city={city}, districts={len(districts)}")`
- `print("Workflow finished.")`

建议：
- 保留“必要级别”例如：每个 district/area 开始与结束（INFO）
- 其余改 DEBUG。

2) 餐厅列表识别
- `print(f"Loaded {len(restaurants)} restaurants from detector.")`
- 你新增的“调试输出餐厅列表”：
  - `[Debug] Detected restaurant list:`
  - 每条 `- name | address | rating | is_main_dish`

建议：
- 默认关闭（DEBUG）
- 只保留：
  - 当前页面识别到多少家（INFO 可选）
  - 或只在失败/为空时打印（ERROR/WARN）

3) 每家餐厅的“逐步动作”日志
- `[Skip] Restaurant #... already visited ...`
- `[Start] Restaurant #...`
- `[Action] Tap restaurant entry ...`
- `[Step] Searching for target element: 菜品`
- `[Found]/[Miss]`、`[RestaurantType]`、`[Found]/[Fallback]`（查看全部/网友推荐）
- `[Step] Collecting menu data ...`
- `[Action] Swipe ...`
- `[Done] Menu items collected ...`
- `[Write] Appending ...`
- 返回逻辑：`[Action] Backing out ...`

建议：
- 这类属于**高频日志**，默认全部改 DEBUG。
- 仅保留：
  - 每个 district/area 的开始/结束
  - 失败原因（例如 菜品/查看全部 未找到：ERROR/WARN + 少量上下文）

---

### 1.4 `components/menu_detector.py`：解析失败时才应打印

文件：`d:/crawler/components/menu_detector.py`

当前打印：
- `print(f"[MenuDetector] LLM返回内容无法解析为 JSON..." )`

建议：
- 保留，但降级为 ERROR/WARN（解析失败确实需要知道内容前 80 字符方便排查）。
- 其它“调试”输出目前较少，不是主要噪声来源。

---

### 1.5 `components/restaurant_detector.py`：解析失败 + 数据跳过日志

文件：`d:/crawler/components/restaurant_detector.py`

当前打印包括：
1) LLM JSON 解析失败
- `print(f"LLM 返回内容无法解析为 JSON: {content}")`
- 建议：保留为 ERROR/WARN。

2) 跳过条目
- `print(f"[RestaurantDetector] skip item without is_main_dish: {item}")`
- `print(f"[RestaurantDetector] invalid is_main_dish value: {is_main_dish!r}, item skipped")`
- `print(f"[RestaurantDetector] invalid is_main_dish type: {type(is_main_dish)}, item skipped")`

建议：
- 这些是“频繁出现但不一定是致命错误”的日志，默认改为 DEBUG。
- 仅在“跳过数量占比过高”或“完全没解析出来”时升级为 WARN。

---

## 2. 建议的实现方案（可复用、可统一开关）

### 2.1 引入统一 logger/开关（强烈建议）

建议新增（或复用）一个简单的日志工具：
- 日志级别：`ERROR / WARN / INFO / DEBUG`
- 默认策略：
  - ERROR/WARN：保留
  - INFO：保留少量关键流程（如 district/area 开始/结束）
  - DEBUG：默认关闭

开关建议：
- 环境变量 `CRAWLER_DEBUG=1` 时开启 DEBUG
- 其它情况下默认关闭。

接口示例（思路，不强制实现细节）：
- `log_debug(msg)`
- `log_info(msg)`
- `log_warn(msg)`
- `log_error(msg)`

### 2.2 改动范围（最小化）

1) `adb_utils.py`：把 tap/swipe/keyevent/input_text/screenshot saved 等改为 DEBUG。
2) OCR 初始化：所有 `PaddleOCR(...)` 加 `show_log=False`。
3) `workflow_manager.py`：高频餐厅级别日志降为 DEBUG，空/失败时升级为 WARN/ERROR。
4) `restaurant_detector.py`：跳过条目日志降为 DEBUG，解析失败保留。

---

## 3. 你可以先确认的一个关键点（决定实现方式）

你希望 debug/verbose 开关用哪种？（建议 1）

1) **环境变量**：`CRAWLER_DEBUG=1` 开启
2) 代码常量：`DEBUG=True/False`
3) 两者都支持（优先环境变量）

你回复选项编号即可。我后续会按你选的方式把“可注释/可关”的日志统一收敛，并把该文档中的策略落到代码。

---

## 4. 本文档覆盖的“具体可注释项”快速索引

- `components/adb_utils.py`
  - `Executing tap at ...`
  - `Executing swipe from ...`
  - `正在发送 Base64 编码内容: ...`
  - `Executing keyevent: ...`
  - `Screenshot saved to ...`

- `components/workflow_manager.py`
  - 所有 `[Debug] / [Skip] / [Start] / [Action] / [Step] / [Found] / [Miss] / [Done] / [Write]`（默认 DEBUG）
  - 只保留 district/area 最少量 INFO；空结果/异常 WARN/ERROR

- `components/restaurant_detector.py`
  - LLM JSON 解析失败：保留（WARN/ERROR）
  - skip/invalid is_main_dish：默认 DEBUG

- `components/menu_detector.py`
  - JSON 解析失败：保留（WARN/ERROR）

- OCR `PaddleOCR` 初始化
  - 三处增加 `show_log=False`：消灭 `ppocr DEBUG: dt_boxes num...`
