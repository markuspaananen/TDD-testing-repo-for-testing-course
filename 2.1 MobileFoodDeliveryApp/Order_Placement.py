import unittest
from unittest import mock


# =========================
# CART ITEM
# =========================
class CartItem:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def update_quantity(self, new_quantity):
        self.quantity = new_quantity

    def get_subtotal(self):
        return self.price * self.quantity


# =========================
# CART
# =========================
class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity):
        for item in self.items:
            if item.name == name:
                item.update_quantity(item.quantity + quantity)
                return f"Updated {name} quantity to {item.quantity}"

        self.items.append(CartItem(name, price, quantity))
        return f"Added {name} to cart"

    def calculate_total(self):
        subtotal = sum(i.get_subtotal() for i in self.items)
        tax = subtotal * 0.10
        delivery_fee = 5.00
        total = subtotal + tax + delivery_fee
        return {
            "subtotal": subtotal,
            "tax": tax,
            "delivery_fee": delivery_fee,
            "total": total
        }

    def view_cart(self):
        return [
            {
                "name": i.name,
                "quantity": i.quantity,
                "subtotal": i.get_subtotal()
            }
            for i in self.items
        ]


# =========================
# ORDER HISTORY (REFACTOR RESULT)
# =========================
class OrderHistory:
    def __init__(self):
        self.orders = []

    def add_order(self, order_id, items, total, status, date):
        self.orders.append({
            "order_id": order_id,
            "items": items,
            "total": total,
            "status": status,
            "date": date
        })

    def get_all_orders(self):
        return self.orders

    def get_order(self, order_id):
        for o in self.orders:
            if o["order_id"] == order_id:
                return o
        return None

    def filter_orders(self, status=None, date=None):
        return [
            o for o in self.orders
            if (status is None or o["status"] == status)
            and (date is None or o["date"] == date)
        ]


# =========================
# USER PROFILE (UPDATED)
# =========================
class UserProfile:
    def __init__(self, delivery_address):
        self.delivery_address = delivery_address
        self.order_history = OrderHistory()

    # wrapper methods (keeps compatibility with your app)
    def add_order(self, order_id, items, total, status, date):
        self.order_history.add_order(order_id, items, total, status, date)

    def view_order_history(self):
        return self.order_history.get_all_orders()

    def get_order_details(self, order_id):
        return self.order_history.get_order(order_id)

    def filter_orders(self, status=None, date=None):
        return self.order_history.filter_orders(status, date)


# =========================
# MENU
# =========================
class RestaurantMenu:
    def __init__(self, available_items):
        self.available_items = available_items

    def is_item_available(self, item_name):
        return item_name in self.available_items


# =========================
# ORDER PLACEMENT
# =========================
class OrderPlacement:
    def __init__(self, cart, user_profile, restaurant_menu):
        self.cart = cart
        self.user_profile = user_profile
        self.restaurant_menu = restaurant_menu

    def validate_order(self):
        if not self.cart.items:
            return {"success": False, "message": "Cart is empty"}

        for item in self.cart.items:
            if not self.restaurant_menu.is_item_available(item.name):
                return {"success": False, "message": f"{item.name} is not available"}

        return {"success": True, "message": "Order is valid"}

    def proceed_to_checkout(self):
        return {
            "items": self.cart.view_cart(),
            "total_info": self.cart.calculate_total(),
            "delivery_address": self.user_profile.delivery_address
        }

    def confirm_order(self, payment_method):
        if not self.validate_order()["success"]:
            return {"success": False, "message": "Order validation failed"}

        total = self.cart.calculate_total()["total"]
        payment_success = payment_method.process_payment(total)

        if payment_success:
            return {
                "success": True,
                "message": "Order confirmed",
                "order_id": "ORD123456",
                "estimated_delivery": "45 minutes"
            }

        return {"success": False, "message": "Payment failed"}


# =========================
# PAYMENT METHOD (SIMPLIFIED)
# =========================
class PaymentMethod:
    def process_payment(self, amount):
        return amount > 0


# =========================
# UNIT TESTS (INCLUDING ORDER HISTORY)
# =========================
class TestOrderPlacement(unittest.TestCase):

    def setUp(self):
        self.menu = RestaurantMenu(["Pizza", "Burger"])
        self.user = UserProfile("123 Main St")
        self.cart = Cart()
        self.order = OrderPlacement(self.cart, self.user, self.menu)

    def test_empty_order_history(self):
        self.assertEqual(self.user.view_order_history(), [])

    def test_add_and_view_orders(self):
        self.user.add_order("O1", ["Pizza"], 20, "Delivered", "2023-01-01")
        history = self.user.view_order_history()

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["order_id"], "O1")

    def test_get_order_details(self):
        self.user.add_order("O2", ["Burger"], 15, "Pending", "2023-01-02")
        order = self.user.get_order_details("O2")

        self.assertEqual(order["status"], "Pending")

    def test_filter_orders(self):
        self.user.add_order("A", ["Pizza"], 10, "Delivered", "2023-01-01")
        self.user.add_order("B", ["Burger"], 20, "Pending", "2023-01-02")

        result = self.user.filter_orders(status="Delivered")
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()