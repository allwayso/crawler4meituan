import unittest
from unittest.mock import patch
from components.scroller import scroll

class TestScroller(unittest.TestCase):
    @patch('components.scroller.scroll')
    def test_scroll(self, mock_scroll):
        """测试向上滑动功能"""
        scroll(500)
        mock_scroll.assert_called_once_with(500)

if __name__ == '__main__':
    unittest.main()
