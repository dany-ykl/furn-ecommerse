from django.test import TestCase

from cart.forms import CartOrderForm


class CartFormTestCase(TestCase):

    def test_contains_form(self):
        form = CartOrderForm()
        self.assertTrue(form.fields['email'])
        self.assertTrue(form.fields['number'])
        self.assertTrue(form.fields['full_name'])
        self.assertTrue(form.fields['address'])
        self.assertTrue(form.fields['delivery'])

    def test_form_is_valid(self):
        data = {
            'email': 'test@mail.com',
            'number': 123412312,
            'full_name': 'Test Testovich',
            'address': 'Test address',
            'delivery': ('free')
        }

        form = CartOrderForm(data=data)
        self.assertTrue(form.is_valid())