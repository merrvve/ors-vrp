from django.db import models
from datetime import date, datetime
from pytz import timezone
from django_jsonform.models.fields import ArrayField
ist= timezone('Europe/Istanbul')

class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    skills = models.ManyToManyField(Skill)
    capacity = ArrayField(models.IntegerField())
    end = ArrayField(models.FloatField(), size=2, default=list)  # Provide a default array of floats
    start = ArrayField(models.FloatField(), size=2, default=list)  # Provide a default array of floats
    time_window = ArrayField(models.IntegerField(), size=2,  default=list)

    def __str__(self):
        return f"Vehicle {self.id}"

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=datetime.now)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(default=datetime.now)
    items = models.ManyToManyField(Item, through='OrderItem')
    email = models.EmailField()
    address = models.CharField(max_length=255)
    location = ArrayField(models.FloatField(), size=2)
    required_skills = models.ManyToManyField(Skill)
    delivery_time_window = ArrayField(models.IntegerField(), size=2, default=list)
    def __str__(self):
        return f"Order {self.id}"


class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = ArrayField(models.FloatField(), size=2)
    items=models.ManyToManyField(Item, through= 'WarehouseItem')
    def __str__(self):
        return f"Warehuse {self.name} {self.id}"

class WarehouseItem(models.Model):
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
	



