from django.contrib import admin
from .models import Patient, SocialMediaReference, OtherReference

# Register your models here.
admin.site.register(SocialMediaReference)
admin.site.register(OtherReference)
admin.site.register(Patient)
