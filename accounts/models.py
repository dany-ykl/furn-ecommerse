from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.is_superuser = False
        user.is_staff = False
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        email = self.normalize_email(email)
        user = self.create_user(email=email, password=password, **other_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def get_by_natural_key(self, email_):
        return self.get(email=email_)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    EMAIL_FIELD = 'email'

    objects = CustomUserManager()

    def get_full_name(self):
        return self.first_name

    @classmethod
    def get_email_field_name(self):
        return self.EMAIL_FIELD

    def __str__(self):
        return self.email


