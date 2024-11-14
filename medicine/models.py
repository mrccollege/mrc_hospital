from django.db import models


# Create your models here.
class MedicineCategory(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'medicine_category'


class Medicine(models.Model):
    name = models.CharField(max_length=500, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    category = models.ForeignKey(MedicineCategory, on_delete=models.CASCADE, null=True)
    desc = models.TextField(null=True, blank=True)
    video_link = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='medicine_image/', null=True, blank=True)
    manufacture = models.CharField(max_length=500, null=True)
    mobile = models.CharField(max_length=500, null=True)
    recom_to_doctor = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'medicine'
