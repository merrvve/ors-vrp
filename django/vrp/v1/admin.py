from django.contrib import admin
from .models import Vehicle, Order, OrderItem, Skill, Item , Warehouse, WarehouseItem

admin.site.register(Vehicle)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Skill)
admin.site.register(Item)
admin.site.register(Warehouse)
admin.site.register(WarehouseItem)