from django.contrib import admin
from .models import ServiceOrder, Service

# Register your models here.
admin.site.register(ServiceOrder)
admin.site.register(Service)