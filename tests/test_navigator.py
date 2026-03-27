import unittest
from components.navigator import get_next_restaurant_y, AllRestaurantsVisitedException

class TestNavigator(unittest.TestCase):
    def test_get_next_restaurant_y_success(self):
        """测试成功获取下一个餐厅 Y 坐标"""
        restaurants = [{'name': '餐厅A', 'visited': False, 'y': 400}]
        y = get_next_restaurant_y(restaurants)
        self.assertEqual(y, 400)

    def test_get_next_restaurant_y_all_visited(self):
        """测试所有餐厅已访问抛出异常"""
        restaurants = [{'name': '餐厅A', 'visited': True, 'y': 400}]
        with self.assertRaises(AllRestaurantsVisitedException):
            get_next_restaurant_y(restaurants)

if __name__ == '__main__':
    unittest.main()
