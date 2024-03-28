import unittest

from src.tools.config import Config, N2NEdgeConfig


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)  # add assertion here

    def test_config(self):
        config = Config()
        n2n_edge_config = config.get_cur_n2n_edge_config()
        n2n_edge_config.edge_ip = "100"
        n2n_edge_config = config.get_cur_n2n_edge_config()
        # config.save()
        self.assertEqual(n2n_edge_config.edge_ip, "100")

    def test_switch_config(self):
        config = Config()
        n2n_edge_config = config.get_cur_n2n_edge_config()
        n2n_edge_config.edge_ip = "127.0.0.1"
        n2n_edge_config.edge_community = "test"
        n2n_edge_config.supernode = "127.0.0.1:10000"
        n2n_edge_config.name = "test1"

        s = n2n_edge_config.serialize()
        config.add_n2n_edge_config(s)

        # config.save()
        self.assertEqual(len(config.n2n_edge_configs), 2)
        self.assertEqual(n2n_edge_config.name, "test1")

        n2n_edge_config.name = "test"
        # config.del_n2n_edge_config(0)

        # self.assertEqual(len(config.n2n_edge_configs), 1)
        self.assertEqual(n2n_edge_config.name, "test")
        config.save()

if __name__ == '__main__':
    unittest.main()
