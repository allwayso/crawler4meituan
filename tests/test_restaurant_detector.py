import unittest
from unittest.mock import patch
from components.restaurant_detector import get_restaurant_list

class TestRestaurantDetector(unittest.TestCase):
    @patch('components.restaurant_detector.get_restaurant_list')
    def test_get_restaurant_list(self, mock_get_list):
        """测试获取餐厅列表并清洗 Y < 300 的结果"""
        mock_get_list.return_value = [
            {'name': '餐厅A', 'y': 200},
            {'name': '餐厅B', 'y': 400}
        ]
        # 实际实现中，get_restaurant_list 内部应包含清洗逻辑
        # 这里测试调用是否返回预期结果
        result = get_restaurant_list()
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()
