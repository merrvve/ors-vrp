from django.contrib import admin
from .models import Vehicle, Order, OrderItem, Skill, Item

admin.site.register(Vehicle)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Skill)
admin.site.register(Item)