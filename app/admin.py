"""
admin.py
^^^^^^^^^
Register models with the django admin utility.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/ref/contrib/admin/
"""
from django.contrib import admin
from app.models import Array, Comment, Family, Oligo, Population, Population_total

class OligoAdmin(admin.ModelAdmin):
    ordering = ['primer']

class PopulationAdmin(admin.ModelAdmin):
    ordering = ['primer', 'name']

class Population_totalAdmin(admin.ModelAdmin):
    ordering = ['order']

class ArrayAdmin(admin.ModelAdmin):
    ordering = ['name']
	
class FamilyAdmin(admin.ModelAdmin):
    ordering = ['name']
	
class CommentAdmin(admin.ModelAdmin):
    ordering = ['primer']

admin.site.register(Oligo, OligoAdmin)
admin.site.register(Population, PopulationAdmin)
admin.site.register(Population_total, Population_totalAdmin)
admin.site.register(Array, ArrayAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Comment, CommentAdmin)
