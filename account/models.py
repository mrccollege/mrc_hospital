from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=500, unique=True, null=True)
    user_type = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    mobile = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    Care_of = models.CharField(max_length=256, null=True, blank=True)
    sex = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    house_flat = models.CharField(max_length=50, null=True, blank=True)
    street_colony = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    district = models.CharField(max_length=256, null=True, blank=True)
    pin = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
