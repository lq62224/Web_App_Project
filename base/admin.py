from django.contrib import admin

# Register your models here.

from .models import Client, Topic, Message, Order

admin.site.register(Client)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Order)
