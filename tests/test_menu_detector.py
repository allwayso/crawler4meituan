import unittest
from unittest.mock import patch
from components.menu_detector import detect_menu

class TestMenuDetector(unittest.TestCase):
    @patch('components.menu_detector.detect_menu')
    def test_detect_menu(self, mock_detect):
        """测试菜单识别功能"""
        mock_detect.return_value = '{"menu": "data"}'
        result = detect_menu('res_1', 'path1', 'path2')
        self.assertEqual(result, '{"menu": "data"}')

if __name__ == '__main__':
    unittest.main()
