import unittest
from unittest.mock import patch
from components.element_detector import find_element, ElementNotFoundException

class TestElementDetector(unittest.TestCase):
    @patch('components.element_detector.find_element')
    def test_find_element_success(self, mock_find):
        """测试成功找到元素"""
        mock_find.return_value = (100, 100)
        coord = find_element('菜品')
        self.assertEqual(coord, (100, 100))

    @patch('components.element_detector.find_element')
    def test_find_element_not_found(self, mock_find):
        """测试未找到元素抛出异常"""
        mock_find.side_effect = ElementNotFoundException
        with self.assertRaises(ElementNotFoundException):
            find_element('不存在')

if __name__ == '__main__':
    unittest.main()
