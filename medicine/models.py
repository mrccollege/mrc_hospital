from django.db import models


# Create your models here.
class Medicine(models.Model):
    medicine_name = models.CharField(max_length=500, null=True)
    medicine_price = models.IntegerField(null=True)
    type = models.CharField(max_length=255, null=True)
    medicine_manufacturer = models.CharField(max_length=500, null=True)
    medicine_expiry = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.medicine_name

    class Meta:
        db_table = 'medicine'
