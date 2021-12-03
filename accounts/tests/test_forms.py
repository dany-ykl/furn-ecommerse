from django.test import TestCase

from accounts import forms

class AccountsFormTestCase(TestCase):

    def test_form_user_creation(self):
        form = forms.CustomUserCreationForm()
        self.assertTrue(form.fields['email'])
        self.assertTrue(form.fields['first_name'])
        self.assertTrue(form.fields['password1'])
        self.assertTrue(form.fields['password2'])

    def test_form_user_change_form(self):
        form = forms.CustomUserChangeForm()
        self.assertTrue(form.fields['email'])
        self.assertTrue(form.fields['first_name'])
        self.assertTrue(form.fields['password'])