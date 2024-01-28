from django.contrib import admin
from .models import Vehicle, Skill , Warehouse, Route, Destination, FulfillmentLineItem, Fulfillment

admin.site.register(Vehicle)
admin.site.register(Skill)
admin.site.register(Warehouse)
admin.site.register(Route)
admin.site.register(Destination)
admin.site.register(FulfillmentLineItem)
admin.site.register(Fulfillment)