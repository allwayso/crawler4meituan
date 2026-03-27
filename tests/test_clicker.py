import unittest
from unittest.mock import patch
from components.clicker import click

class TestClicker(unittest.TestCase):
    @patch('components.clicker.tap')
    def test_click(self, mock_tap):
        """测试点击功能是否正确调用了底层 tap"""
        click(100, 200)
        mock_tap.assert_called_once_with(100, 200)

if __name__ == '__main__':
    unittest.main()
