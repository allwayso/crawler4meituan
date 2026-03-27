import unittest
from unittest.mock import patch
from components.restaurant_info_detector import detect_restaurant_info

class TestRestaurantInfoDetector(unittest.TestCase):
    @patch('components.restaurant_info_detector.detect_restaurant_info')
    def test_detect_restaurant_info(self, mock_detect):
        """测试餐厅信息识别功能"""
        mock_detect.return_value = '{"name": "餐厅A"}'
        result = detect_restaurant_info('res_1', 'path')
        self.assertEqual(result, '{"name": "餐厅A"}')

if __name__ == '__main__':
    unittest.main()
