from django.db import models


# Create your models here.
class DiagnosisDiseaseName(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'diagnosis_disease_name'


class DiagnosisPosition(models.Model):
    name = models.ForeignKey(DiagnosisDiseaseName, on_delete=models.CASCADE, null=True, blank=True)
    position = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.position

    class Meta:
        db_table = 'diagnosis_position'


class DiagnosisType(models.Model):
    position = models.ForeignKey(DiagnosisPosition, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'diagnosis_type'
