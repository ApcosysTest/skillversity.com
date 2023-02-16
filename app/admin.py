from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Register)

@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    ordering = ['name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    ordering = ['name']

admin.site.register(Category)
admin.site.register(Language)
admin.site.register(Contact)
admin.site.register(Investor)
admin.site.register(Instructor)
admin.site.register(Currency)
