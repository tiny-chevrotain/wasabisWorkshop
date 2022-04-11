from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse

# Create your models here.


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of names.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('User must have an email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    name = models.CharField(
        verbose_name="name", max_length=60)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    # for now, will assume user only has 1 account to link to:
    # spotify_token = models.OneToOneField(
    #     'workshop.SpotifyToken',
    #     on_delete=models.CASCADE,
    # )

    # assuming user can have many accounts, this could be handy:

    # spotify_tokens = models.ForeignKey(
    #     Wasabia,
    #     on_delete=models.CASCADE,
    # )

#     # library_analysises = models.ForeignKey(
#     #     LibraryAnalysis,
#     #     on_delete=models.CASCADE,
#     # )

#     # wasabias = models.ForeignKey(
#     #     Wasabia,
#     #     on_delete=models.CASCADE,
#     # )

#     # votes = models.ForeignKey(
#     #     Votes,
#     #     on_delete=models.CASCADE,
#     # )

#     def __str__(self):
#         return self.name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class SpotifyToken(models.Model):
    session_id = models.CharField(max_length=50, unique=True)
    created_at = models.DateField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)
