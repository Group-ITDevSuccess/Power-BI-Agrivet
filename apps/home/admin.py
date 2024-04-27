from django.contrib import admin

from apps.home.models import Hebdo


# Register your models here.
@admin.register(Hebdo)
class HebdoAdmin(admin.ModelAdmin):
    list_display = ('department', 'family', 'article')