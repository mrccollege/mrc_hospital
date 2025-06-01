from django.contrib import admin
from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_type', 'mobile', 'district', 'state__name', 'created_at', 'id')
    list_filter = ('username', 'user_type', 'mobile', 'district', 'state__name', 'created_at', 'id')
    search_fields = ('username', 'user_type', 'mobile', 'district', 'state__name', 'created_at', 'id')


admin.site.register(User, UserAdmin)
