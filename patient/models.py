from django.db import models

from account.models import User


# Create your models here.
class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    patient_code = models.CharField(max_length=20, null=True, blank=True)
    patient_diseases = models.TextField(null=True, blank=True)
    patient_bp_min = models.IntegerField(null=True, blank=True)
    patient_bp_max = models.IntegerField(null=True, blank=True)
    patient_weight = models.IntegerField(null=True, blank=True)
    patient_age = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        db_table = 'patient'
