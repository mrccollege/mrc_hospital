from django.db import models

from account.models import User


# Create your models here.
class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    specialist = models.CharField(max_length=100, null=True)
    degree = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        db_table = 'doctor'
