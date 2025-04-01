from django.db import models

from account.models import User


# Create your models here.
class MenuPurpose(models.Model):
    title = models.CharField(max_length=100, null=True)
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'menu_purpose'


class MenuCategory(models.Model):
    cat_title = models.CharField(max_length=100, null=True)
    cat_desc = models.TextField(null=True, blank=True)
    menu_purpose = models.ForeignKey(MenuPurpose, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.cat_title

    class Meta:
        db_table = 'menu_category'


class MenuMaster(models.Model):
    menu_category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, null=True)
    menu_title = models.CharField(max_length=256, null=True)
    menu_url = models.CharField(max_length=500, null=True)
    menu_desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.menu_title

    class Meta:
        db_table = 'menu_master'


class MenuUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(MenuMaster, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.menu.menu_title)

    class Meta:
        db_table = 'menu_user'
