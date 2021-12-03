from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes 
from django.utils.http import urlsafe_base64_encode

from accounts.models import CustomUser
from accounts import views


class AccountsViewsTestCase(TestCase):

    def setUp(self):
        token_generator = PasswordResetTokenGenerator()
        self.email = 'test@mail.com'
        self.first_name = 'Test'
        self.password = 'Wfwepof121!'
        self.data = {
            'email': self.email,
            'first_name': self.first_name,
            'password1': self.password,
            'password2': self.password
        }
        
        self.client = Client()
        self.factory = RequestFactory()

        self.user = CustomUser.objects.create_user(
            email='test2@mail.com',
            first_name='Test',
            password=self.password
        )
        self.user.save()

        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = token_generator.make_token(self.user)

    def test_view_register_page(self):
        request = self.factory.post('', data=self.data)

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        response = views.RegisterPage.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.get(email=self.email).email, self.email)
        
    def test_view_login_page(self):
        response = self.client.login(email='test2@mail.com', password=self.password)
        self.assertTrue(response)
    
    def test_view_logout(self):
        request = self.factory.get('')
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = views.LogoutPage.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('shop/base.html')

    def test_viev_validate_email(self):
        request = self.factory.get('')
        request.GET = {'email': 'test2@mail.com'}
        response = views.validate_email(request)
        request_false = self.factory.get('')
        request_false.GET = {'email': 'test1231@mail.com'}
        response_false = views.validate_email(request_false)
        self.assertJSONEqual(response.content, {'is_taken': True})
        self.assertJSONEqual(response_false.content, {'is_taken': False})  

    def test_view_custom_password_change(self):
        request = self.factory.get('')
        request.user = self.user
        response =views.CustomPasswordChangeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
    def test_view_custom_password_change_done(self):
        request = self.factory.get('')
        request.user = self.user
        response =views.CustomPasswordChangeDoneView.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    def test_view_custom_password_change_reset(self):
        request = self.factory.get('')
        request.user = self.user
        response =views.CustomPasswordResetView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
    def test_view_custom_password_change_reset(self):
        request = self.factory.get('', content_type="application/x-www-form-urlencoded")
        request.user = self.user
        response = views.CustomPasswordResetDoneView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_view_custom_reset_confirm(self):
        request = self.factory.post('')
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        kwargs = {
            'uidb64': self.uid,
            'token': self.token
        }
        response = views.CustomPasswordResetConfirmView.as_view()(request, **kwargs)
        self.assertEqual(response.status_code, 302)

    def test_view_custom_password_reset_complete(self):
        request = self.factory.get('')
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = views.CustomPasswordResetCompleteView.as_view()(request)
        self.assertEqual(response.status_code, 200)