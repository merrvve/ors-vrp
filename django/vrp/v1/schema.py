from datetime import date, datetime
from ninja import Schema
from typing import List

class OrderItemSchema(Schema):
    order: int
    item: int
    quantity: int

class OrderIn(Schema):
    items: List[int]
    email: str
    address: str
    location: List[float]
    delivery_time: datetime
    required_skills: List[int]
    order_items: List[OrderItemSchema]

class OrderOut(Schema):
    id: int
    items: List[int]
    email: str
    address: str
    location: List[float]
    delivery_time: datetime
    required_skills: List[int]
    order_items: List[OrderItemSchema]

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