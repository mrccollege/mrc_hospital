from django.db import models


# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=50, null=True)
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True)
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.country.name + ' ' + self.name)
