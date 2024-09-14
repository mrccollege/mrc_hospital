from django.db import models

from account.models import User


# Create your models here.
class OtherReference(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'other_reference'


class SocialMediaReference(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'social_media_reference'


class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    social_media = models.ForeignKey(SocialMediaReference, on_delete=models.CASCADE, null=True, blank=True)
    other_reference = models.ForeignKey(OtherReference, on_delete=models.CASCADE, null=True, blank=True)
    patient_code = models.CharField(max_length=20, null=True, blank=True)
    reference_by_patient = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        db_table = 'patient'
