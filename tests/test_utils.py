import unittest
from src.utils import get_agent

class TestUtils(unittest.TestCase):

    def test_get_agent(self):
        agent = get_agent("data/handbook.pdf")
        self.assertIsNotNone(agent)

if __name__ == "__main__":
    unittest.main()
