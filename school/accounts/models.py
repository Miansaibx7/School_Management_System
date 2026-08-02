from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser, BaseUserManager

# ====================================== CUSTOM USER MANAGER =================================================================
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        try:
            user.save(using=self._db)
        except IntegrityError:
            raise ValueError("A user with this email already exists.")
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)    

    
#============================ USER MODEL ===================================================================================
class User(AbstractUser):
    """Custom User model using email as username"""
    username = None
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Role flags for dashboard access control
    is_admin = models.BooleanField(default=False)
    is_accountant = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    @property
    def role(self):
        """ Single source of truth for display role — use this everywhere instead of 
        re-deriving is_admin/is_accountant logic in views/templates."""
        if self.is_superuser:
            return "Super Administrator"
        elif self.is_admin:
            return "Administrator"
        elif self.is_accountant:
            return "Accountant"
        return "Staff User"