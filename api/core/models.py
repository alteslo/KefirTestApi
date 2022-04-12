from django.contrib.auth.models import AbstractUser
from django.db import models


class Cities(models.Model):
    name = models.CharField(max_length=120, verbose_name='City')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class MyUser(AbstractUser):
    first_name = models.CharField(verbose_name='First Name', max_length=150)
    last_name = models.CharField(verbose_name='Last Name', max_length=150)
    other_name = models.CharField(
        verbose_name='Other Name', max_length=150, blank=True
    )
    email = models.EmailField(verbose_name='Email')

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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
