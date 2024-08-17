from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator, validate_email

class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """

    def create_user(self, username=None, email=None, phone_number=None, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given username or email and password.
        """
        if not username and not email:
            raise ValueError("Either username or email is required.")

        email = self.normalize_email(email) if email else None
        username = self.model.normalize_username(username) if username else None

        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email=None, phone_number=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username or email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model.
    """

    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True, validators=[validate_email])
    phone_number = models.CharField(max_length=15, null=True, blank=True,
                                    validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                                               message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_registered_at = models.DateTimeField(auto_now_add=True)
    
    is_trade_service_user = models.BooleanField(default=False)
    is_food_service_user = models.BooleanField(default=False)
    is_cafe_entrepreneurship_user = models.BooleanField(default=False)
    
    otp = models.CharField(max_length=4, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username' if email else 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"id: {self.id}, {self.username or self.email}"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class UserProfile(models.Model):
    SUBSCRIPTION_TYPE = [
        ('lite', 'Lite'),
        ('pro', 'Pro'),
        ('none', 'None'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    subscription_type = models.CharField(max_length=4, choices=SUBSCRIPTION_TYPE, default='none', blank=True, null=True)
    

    def __str__(self):
        return self.user.username