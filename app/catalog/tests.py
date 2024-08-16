from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Brand, Category, Product


class CatalogModelViewTestCase(TestCase):
    def test_brand(self):
        brand = Brand.objects.create(name="Brand")
        count = Brand.objects.all().count()
        path = reverse("catalog:brand", kwargs={"slug": brand.slug})
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(count, 1)
        self.assertIn(brand.slug, brand.get_absolute_url())

    def test_category(self):
        category = Category.objects.create(name="Category")
        count = Category.objects.all().count()
        path = reverse("catalog:category", kwargs={"slug": category.slug})
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(count, 1)
        self.assertIn(category.slug, category.get_absolute_url())

    def test_product(self):
        product = Product.objects.create(name="Product")
        count = Product.objects.all().count()
        path = reverse("catalog:product", kwargs={"slug": product.slug})
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(count, 1)
        self.assertIn(product.slug, product.get_absolute_url())
