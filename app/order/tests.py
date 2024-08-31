from django.test import TestCase
from django.urls import reverse

from catalog.models import Product
from .forms import OrderCreateForm
from .models import Order, OrderItem


class OrderModelTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=10)

        self.order = Order.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            address="123 Street",
            postal_code="12345",
            city="City",
        )
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, price=self.product.price, quantity=2
        )

    def test_order_str_method(self):
        # Ensure that the __str__ method returns the expected string representation.
        self.assertEqual(str(self.order), f"Order {self.order.id}")

    def test_order_get_total_cost(self):
        """
        Test the get_total_cost method of the Order model.

        Ensure that the get_total_cost method returns the expected total cost
        """

        # Assuming you have an OrderItem model with a get_cost method
        expected_total_cost = self.order_item.price * self.order_item.quantity
        self.assertEqual(self.order.get_total_cost(), expected_total_cost)


class OrderCreateViewTest(TestCase):
    order_url = reverse("cart:cart_detail")

    valid_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "address": "123 Street",
        "postal_code": "12345",
        "city": "City",
    }

    def test_order_form_valid(self):
        form = OrderCreateForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_order_form_not_valid(self):
        # not email
        not_valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "address": "123 Main St",
            "postal_code": "12345",
            "city": "City",
        }
        form = OrderCreateForm(data=not_valid_data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, "email", "Это поле обязательно для заполнения.")

    def test_order_post(self):
        self.client.post(self.order_url, self.valid_data, follow=True)
        self.assertTrue(Order.objects.filter(email=self.valid_data["email"]).exists())
