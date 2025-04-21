from django.contrib import admin
from .models import Procedure, CategoryProcedure


# Register your models here.

class CategoryProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)


class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'id')
    search_fields = ('name', 'price')


admin.site.register(CategoryProcedure, CategoryProcedureAdmin)
admin.site.register(Procedure, ProcedureAdmin)
