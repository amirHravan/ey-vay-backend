from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseUserManager(BaseUserManager):
    """
    Manager for the BaseUser model.
    """

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('The Phone Number must be provided'))
        extra_fields.setdefault('is_active', True)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)


# class BaseUser(AbstractBaseUser, PermissionsMixin):
#     """
#     Abstract base user model with phone_number as the unique identifier.
#     """
#     first_name = models.CharField(max_length=50, blank=True)
#     last_name = models.CharField(max_length=50, blank=True)
#     phone_number = models.CharField(max_length=15, unique=True)
#     email = models.EmailField(blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = BaseUserManager()

#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = []

#     class Meta:
#         abstract = True

#     def __str__(self):
#         return self.phone_number

class BaseUser(AbstractBaseUser, PermissionsMixin):
    """
    Abstract base user model with phone_number as the unique identifier.
    """
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('provider', 'Provider'),
    ]

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    objects = BaseUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.phone_number} ({self.role})"


# class CustomerUser(BaseUser):
#     """
#     Customer-specific user model inheriting from BaseUser.
#     """
#     date_of_birth = models.DateField(blank=True, null=True)
#     national_id = models.CharField(max_length=10, blank=True, null=True)

#     class Meta:
#         verbose_name = "Customer User"
#         verbose_name_plural = "Customer Users"



class VerificationCode(models.Model):
    """
    Model to store verification codes for phone number verification.
    """
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Code {self.code} for {self.phone_number}"


class TokenBlacklist(models.Model):
    """
    Model to store invalidated refresh tokens.
    """
    token = models.TextField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blacklisted token {self.token[:10]}..."

class CustomerProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name="customer_profile")
    date_of_birth = models.DateField(blank=True, null=True)
    national_id = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Customer: {self.user.phone_number}"


class ProviderProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name="provider_profile")
    business_name = models.CharField(max_length=100)
    business_contact = models.CharField(max_length=15)
    website_url = models.URLField()

    def __str__(self):
        return f"Provider: {self.user.phone_number} ({self.business_name})"


# class ProviderUser(BaseUser):
#     """
#     Provider-specific user model inheriting from BaseUser.
#     """
#     business_name = models.CharField(max_length=100)
#     business_contact = models.CharField(max_length=15)
#     website_url = models.URLField()

#     class Meta:
#         verbose_name = "Provider User"
#         verbose_name_plural = "Provider Users"