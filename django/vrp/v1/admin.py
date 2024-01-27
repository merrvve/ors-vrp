from django.contrib import admin
from .models import Vehicle, Skill , Warehouse, Route

admin.site.register(Vehicle)
admin.site.register(Skill)
admin.site.register(Warehouse)
admin.site.register(Route)