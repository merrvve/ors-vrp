from django.db import models
from datetime import date
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