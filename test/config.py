import unittest

from src.tools.config import Config


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)  # add assertion here

    def test_config(self):
        config = Config()
        n2n_edge_config = config.get_cur_n2n_edge_config()
        n2n_edge_config.edge_ip = "100"
        n2n_edge_config = config.get_cur_n2n_edge_config()
        config.save()
        self.assertEqual(n2n_edge_config.edge_ip, "100")

if __name__ == '__main__':
    unittest.main()
