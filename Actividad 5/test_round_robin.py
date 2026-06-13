import os
import tempfile
import unittest

from checkear_rutas import check_routes


class CheckRoutesRoundRobinTest(unittest.TestCase):
    def test_round_robin_uses_all_matching_routes(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as routes_file:
            routes_file.write("192.168.100.91/24 8881 8883 192.168.100.91 8881\n")
            routes_file.write("192.168.100.91/24 8881 8883 192.168.100.91 8882\n")
            temp_path = routes_file.name

        try:
            first = check_routes(temp_path, ("192.168.100.91", 8882))
            second = check_routes(temp_path, ("192.168.100.91", 8882))

            self.assertEqual(first, ("192.168.100.91", 8881))
            self.assertEqual(second, ("192.168.100.91", 8882))
        finally:
            os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
