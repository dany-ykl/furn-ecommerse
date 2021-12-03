from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from .accounts_service import _validate_email


class RegisterPage(generic.FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('shop:home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        return super(RegisterPage, self).get(*args, **kwargs)


def validate_email(request):
    return _validate_email(request)


class LoginPage(auth_views.LoginView):
    template_name = 'registration/login.html'
   
    def get_success_url(self):
        return reverse_lazy('shop:home')


class LogoutPage(auth_views.LogoutView):
    next_page = 'shop:home'

class CustomPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'registration/custom_password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')

class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'registration/custom_password_change_done.html'

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/custom_password_reset_form.html'
    email_template_name = 'registration/custom_password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/custom_password_reset_done.html'
    

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/custom_password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/custom_password_reset_complete.html'