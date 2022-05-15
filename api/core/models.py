from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class Cities(models.Model):
    '''Модель города'''
    city = models.CharField(max_length=120, verbose_name='City')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.city


class MyUserManager(UserManager):
    '''Кастомный UserManager не требующий username'''
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractUser):
    '''Кастомная модель User'''
    first_name = models.CharField(verbose_name='First Name', max_length=150)
    last_name = models.CharField(verbose_name='Last Name', max_length=150)
    other_name = models.CharField(
        verbose_name='Other Name', max_length=150, blank=True
    )
    email = models.EmailField(verbose_name='Email', unique=True)

    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-a-phone-number-in-django-models
    phone = models.CharField(verbose_name='Phone', max_length=12, blank=True)

    city = models.ForeignKey(
        Cities,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='City'
    )

    birthday = models.DateField(verbose_name='Birthday', null=True, blank=True)
    additional_info = models.TextField(
        verbose_name='Additional Info', blank=True
    )
    is_admin = models.BooleanField(verbose_name='Is Admin', null=True)
    password = models.CharField(verbose_name='Password', max_length=128)
    username = models.CharField(max_length=150, unique=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
