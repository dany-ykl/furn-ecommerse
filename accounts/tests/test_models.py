from django.test import TestCase

from accounts.models import CustomUser


class AccountsModelsTestCase(TestCase):

    def setUp(self):
        self.email = 'test@mail.com'
        self.email_two = 'test1@mail.com'
        self.first_name = 'Test'
        self.password = 'Wfwepof121!'
        self.user = CustomUser.objects.create_user(
            email=self.email,
            first_name=self.first_name,
            password=self.password
        )

        self.superuser = CustomUser.objects.create_superuser(
            email=self.email_two,
            first_name=self.first_name,
            password=self.password,
        )

    def test_models_user(self):
        self.assertIsInstance(self.user, CustomUser)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.first_name, self.first_name)
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.is_superuser, False)

    def test_models_superuser(self):
        self.assertIsInstance(self.superuser, CustomUser)
        self.assertEqual(self.superuser.email, self.email_two)
        self.assertEqual(self.superuser.first_name, self.first_name)
        self.assertEqual(self.superuser.is_active, True)
        self.assertEqual(self.superuser.is_staff, True)
        self.assertEqual(self.superuser.is_superuser, True)