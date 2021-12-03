from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'first_name')

    def save(self):
        user = super(CustomUserCreationForm, self).save()
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('email', 'first_name',)