import unittest
from Order_Placement import UserProfile


class TestOrderHistory(unittest.TestCase):

    def setUp(self):
        self.user = UserProfile(delivery_address="123 Main St")

    # RED: no orders yet
    def test_empty_order_history(self):
        self.assertEqual(self.user.view_order_history(), [])

    # RED: add + retrieve orders
    def test_add_and_view_orders(self):
        self.user.add_order(
            "O1",
            ["Pizza"],
            20.0,
            "Delivered",
            "2026-01-01"
        )

        history = self.user.view_order_history()

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["order_id"], "O1")

    # RED: order details
    def test_order_details(self):
        self.user.add_order(
            "O2",
            ["Burger", "Fries"],
            15.5,
            "Pending",
            "2026-01-02"
        )

        order = self.user.get_order_details("O2")

        self.assertEqual(order["status"], "Pending")
        self.assertEqual(order["total"], 15.5)

    # RED: invalid order
    def test_invalid_order(self):
        self.assertIsNone(self.user.get_order_details("NOPE"))

    # RED: filter orders
    def test_filter_orders(self):
        self.user.add_order("A", ["Pizza"], 10, "Delivered", "2026-01-01")
        self.user.add_order("B", ["Burger"], 20, "Pending", "2026-01-02")

        result = self.user.filter_orders(status="Delivered")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["order_id"], "A")


if __name__ == "__main__":
    unittest.main()