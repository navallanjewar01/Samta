# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_tenants.models import TenantModel
from django_tenants.utils import schema_context
from django.core.validators import RegexValidator
from django_tenants.models import TenantMixin


class CustomUserManager(models.Manager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        """
        Create and return a regular user with an email and phone number.
        """
        if not email:
            raise ValueError('The Email field must be set')
        if not phone_number:
            raise ValueError('The Phone Number field must be set')

        with schema_context(TenantModel.objects.get(schema_name='public')):
            user = self.model(email=self.normalize_email(email), phone_number=phone_number, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and phone number.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, phone_number, password, **extra_fields)

class CustomUser(TenantModel, AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, validators=[
        RegexValidator(regex=r'^[\d\s()+-]+$', message='Phone number must contain only numeric, "+", "-", "(", ")", and space characters.')
    ])

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        """
        Override the save method to enforce uniqueness for email and phone number combination.
        """
        with schema_context(self.tenant):
            if CustomUser.objects.filter(email=self.email, phone_number=self.phone_number).exists():
                raise ValueError('A user with the same email and phone number combination already exists')
            super().save(*args, **kwargs)

class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    domain_url = models.CharField(max_length=100, unique=True)
    schema_name = models.CharField(max_length=100, unique=True)