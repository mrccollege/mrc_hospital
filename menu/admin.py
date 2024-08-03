from django.contrib import admin
from .models import MenuCategory, MenuMaster, MenuUser


# Register your models here.
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_title', 'cat_desc', 'created_at', 'id')


class MenuMasterAdmin(admin.ModelAdmin):
    list_display = ('menu_title', 'menu_url', 'created_at', 'id')


class MenuUserAdmin(admin.ModelAdmin):
    list_display = ('menu', 'user', 'created_at', 'id')


admin.site.register(MenuCategory, MenuCategoryAdmin)
admin.site.register(MenuMaster, MenuMasterAdmin)
admin.site.register(MenuUser, MenuUserAdmin)
