from django.db.models.query import QuerySet
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from shop.models import Category, Product


class ShopModelsTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Sofa')
        self.product = Product.objects.create(
            category=self.category,
            name='Sofa V',
            description='Description for the Sofa V',
            image=SimpleUploadedFile(name='sofa_3.jpg', content=b'', content_type='image/jpeg'),
            price=5000.00,
            stock=10,
            slug='sofa-v'
        )


    def test_get_absolute_url_product(self):
        self.assertEqual(self.product.get_absolute_url(), '/shop/sofa-v/')    


    def test_method_save_product(self):
        self.assertTrue(self.product.available)
        self.product.stock = 0
        self.product.save()
        self.assertEqual(self.product.stock, 0)
        self.assertFalse(self.product.available)


    def test_count_category(self):
        self.assertEqual(self.category.count(), 1)


    def test_get_product_category(self):
        self.assertIsInstance(self.category.get_products(), QuerySet)