from django.contrib import admin
from crm_app.models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Order)