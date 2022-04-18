from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class Cities(models.Model):
    city = models.CharField(max_length=120, verbose_name='City')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.city


class MyUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    first_name = models.CharField(verbose_name='First Name', max_length=150)
    last_name = models.CharField(verbose_name='Last Name', max_length=150)
    other_name = models.CharField(
        verbose_name='Other Name', max_length=150, blank=True
    )
    email = models.EmailField(verbose_name='Email', unique=True)

    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-a-phone-number-in-django-models
    phone = models.CharField(verbose_name='Phone', max_length=12, blank=True)

    city = models.ForeignKey(
        Cities, models.SET_NULL, blank=True, null=True)
    birthday = models.DateField(verbose_name='Birthday', blank=True, null=True)
    additional_info = models.TextField(
        verbose_name='Additional Info', blank=True
    )
    is_admin = models.BooleanField(verbose_name='Is Admin', default=True)
    password = models.CharField(verbose_name='Password', max_length=128)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
