# websites/admin.py

from django.contrib import admin
from .models import *


class IndexAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Index._meta.get_fields()]


admin.site.register(Index, IndexAdmin)


class IndexCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_order_num',)


admin.site.register(IndexCategory, IndexCategoryAdmin)


class ToDoTaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ToDoTask._meta.get_fields()]


admin.site.register(ToDoTask, ToDoTaskAdmin)
