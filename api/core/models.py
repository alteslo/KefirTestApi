from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    user = models.ForeignKey(User, on_delete=models.CASCADE)



{
  "first_name": "string",
  "last_name": "string",
  "other_name": "string",
  "email": "string",
  "phone": "string",
  "birthday": "2022-04-08",
  "city": 0,
  "additional_info": "string",
  "is_admin": true,
  "password": "string"
}