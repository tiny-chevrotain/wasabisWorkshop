from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models import Count


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

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class SpotifyToken(models.Model):
    user_auth_token = models.CharField(max_length=50, unique=True)
    created_at = models.DateField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)


class Wasabia(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)

    songs = models.ManyToManyField(
        'Song',
        related_name='wasabias',
    )

    user = models.ForeignKey(
        User,
        related_name='wasabias',
        on_delete=models.CASCADE,
    )

    @property
    def votes(self):
        return Score.objects.filter(wasabia=self).aggregate(models.Sum('votes_total'))


class Artist(models.Model):
    id = models.CharField(max_length=22, unique=True, primary_key=True)
    name = models.CharField(max_length=50)


class Song(models.Model):
    id = models.CharField(max_length=22, unique=True, primary_key=True)
    name = models.CharField(max_length=50)
    image_640_url = models.CharField(max_length=64)
    image_300_url = models.CharField(max_length=64)
    image_64_url = models.CharField(max_length=64)

    artists = models.ManyToManyField(
        Artist,
        related_name='songs',
    )


class Upvote(models.Model):
    score = models.ForeignKey(
        'Score',
        related_name='upvotes',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='upvotes',
        on_delete=models.CASCADE,
    )


class Downvote(models.Model):
    score = models.ForeignKey(
        'Score',
        related_name='downvotes',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='downvotes',
        on_delete=models.CASCADE,
    )


class Score(models.Model):
    upvotes_count = models.IntegerField(default=0)
    downvotes_count = models.IntegerField(default=0)
    votes_total = models.IntegerField(default=0)
    song = models.ForeignKey(
        Song,
        related_name='scores',
        on_delete=models.CASCADE,
    )
    wasabia = models.ForeignKey(
        Wasabia,
        related_name='scores',
        on_delete=models.CASCADE,
    )

    def upvote(self, user):
        downvote = self.downvotes.filter(user=user)
        if downvote.exists():
            downvote.delete()
        upvote = self.upvotes.filter(user=user)
        if not upvote.exists():
            Upvote.objects.create(score=self, user=user)
        self.save()

    def downvote(self, user):
        upvote = self.upvotes.filter(user=user)
        if upvote.exists():
            upvote.delete()
        downvote = self.downvotes.filter(user=user)
        if not downvote.exists():
            Downvote.objects.create(score=self, user=user)
        self.save()

    def unvote(self, user):
        upvote = self.upvotes.filter(user=user)
        if upvote.exists():
            upvote.delete()
        downvote = self.downvotes.filter(user=user)
        if downvote.exists():
            downvote.delete()
        self.save()

    def vote(self, user, value):
        value = int(value)
        if value == 1:
            self.upvote(user)
        elif value == -1:
            self.downvote(user)
        elif value == 0:
            self.unvote(user)

    def save(self, *args, **kw):

        upvotes = Upvote.objects.filter(score=self)
        downvotes = Downvote.objects.filter(score=self)

        upvotes_count = upvotes.count() if upvotes.exists() else 0
        downvotes_count = downvotes.count() if downvotes.exists() else 0

        self.upvotes_count = upvotes_count
        self.downvotes_count = downvotes_count
        self.votes_total = upvotes_count - downvotes_count
        super(Score, self).save(*args, **kw)
