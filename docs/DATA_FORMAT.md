# 数据格式定义 (Data Format Definitions)

本文件定义了餐厅信息和菜单信息的 JSON 格式。

### 1. 餐厅信息 (`restaurant_info.json`)
```json
{
  "restaurant_id": "string",      // 唯一标识符
  "name": "string",               // 餐厅名称
  "address": "string",            // 截图中出现的地址
  "rating": "float"               // 评分
}
```

### 2. 菜单信息 (`menu_info.json`)
```json
{
  "restaurant_id": "string",      // 关联的餐厅 ID
  "categories": [                 // 菜单分类
    {
      "category_name": "string",
      "dishes": [
        {
          "dish_name": "string",  // 菜名
          "price": "float",       // 价格
          "description": "string" // 菜品描述
        }
      ]
    }
  ],
  "last_updated": "string"        // 数据采集时间
}
```
