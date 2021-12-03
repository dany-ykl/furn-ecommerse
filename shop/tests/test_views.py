from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware


from shop import shop_service
from accounts.models import CustomUser
from shop.models import Category, Product

service = shop_service

class ShopViewsTestCase(TestCase):


    def setUp(self):
        self.client = Client()

        sofa_category = Category.objects.create(name='Sofa')
        table_category = Category.objects.create(name='Table')
        chair_category = Category.objects.create(name='Chair')
        bed_category = Category.objects.create(name='Bed')
        decore_category = Category.objects.create(name='Decore')

        sofa = Product.objects.create(
            category=Category.objects.get(name='Sofa'),
            name='Sofa Vika',
            description='Description for the Sofa Vika',
            image=SimpleUploadedFile(name='sofa_3.jpg', content=b'', content_type='image/jpeg'),
            price=5000.00,
            stock=10,
            slug='sofa-vika'
        )

        self.factory = RequestFactory()
        self.user = CustomUser.objects.create(
            email='test@mail.com',
            first_name='test',
            password='test!rtek[1111')

        
    def test_redirect_in_shop(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 301)
        self.assertTemplateUsed('shop/base.html')

    
    def test_get_method_view_home(self):
        response = self.client.get('/shop/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('shop/base.html')

    
    def test_get_method_view_detail_product(self):
        response = self.client.get('/shop/sofa-vika/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('shop/product_detail.html')


    def test_get_product_list_in_view_home_for_user(self):
        request = self.factory.get('/shop/')
        request.user = self.user
        response = service.get_products_list(request)
        self.assertIsInstance(response, dict)


    def test_get_product_list_in_view_home_for_anonym_user(self):
        request = self.factory.get('/shop/')
        request.user = AnonymousUser()

        #add session for anonymos user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        
        response = service.get_products_list(request)
        self.assertIsInstance(response, dict)
