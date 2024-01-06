from django.db import models
from datetime import date, datetime
from ninja import Schema
from typing import List


from django.contrib.postgres.fields import ArrayField



class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    skills = models.ManyToManyField(Skill)
    capacity = ArrayField(models.IntegerField())

    def __str__(self):
        return f"Vehicle {self.id}"

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(Item, through='OrderItem')
    email = models.EmailField()
    address = models.CharField(max_length=255)
    location = ArrayField(models.FloatField(), size=2)
    delivery_time = models.DateTimeField()
    required_skills = models.ManyToManyField(Skill)

    def __str__(self):
        return f"Order {self.id}"

class OrderItemSchema(Schema):
    id: int
    item: int
    quantity: int

class OrderIn(Schema):
    items: List[int]
    email: str
    address: str
    location: List[float]
    delivery_time: datetime
    required_skills: List[int]
    order_items: List[int]

class OrderOut(Schema):
    id: int
    items: List[int]
    email: str
    address: str
    location: List[float]
    delivery_time: datetime
    required_skills: List[int]
    order_items: List[int]

class RouteRequestSchema(Schema):
    vehicle_ids: List[int]
    order_ids: List[int]

class SkillIn(Schema):
    description: str

class SkillOut(Schema):
    id: int
    description: str

class VehicleIn(Schema):
    skills: List[int]
    capacity: List[int]

class VehicleOut(Schema):
    id: int
    skills: List[SkillOut]
    capacity: List[int]