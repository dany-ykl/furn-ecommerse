from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('validate_email/', views.validate_email, name='validate_email'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', views.LogoutPage.as_view(), name='logout'),

    path('password_change/',
     views.CustomPasswordChangeView.as_view(),
     name='password_change'),

    path('password_change/done',
     views.CustomPasswordChangeDoneView.as_view(),
     name='password_change_done'),

    path('password_reset/',
     views.CustomPasswordResetView.as_view(),
     name='password_reset'),

    path('password_reset/done/',
     views.CustomPasswordResetDoneView.as_view(),
     name='password_reset_done'),
     
    path('reset/<uidb64>/<token>/',
     views.CustomPasswordResetConfirmView.as_view(),
     name='password_reset_confirm'),

    path('reset/done',
     views.CustomPasswordResetCompleteView.as_view(),
     name='password_reset_complete')
]