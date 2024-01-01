from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(AdministratorPostSession)
class AdminAdministratorPostSession(admin.ModelAdmin):
    pass

