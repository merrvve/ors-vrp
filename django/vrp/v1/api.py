from ninja import Router
from .models import *
from .schema import *
from typing import List
from v1 import routeoptimizer
from django.forms.models import model_to_dict
router = Router()

""" Vehicle CRUD """
@router.post("/vehicles")
def create_vehicle(request, payload: VehicleIn):
    skills = Skill.objects.filter(id__in=payload.skills)
    vehicle = Vehicle.objects.create()
    vehicle.skills.set(skills)
    vehicle.capacity = payload.capacity
    vehicle.save()
    return {"id": vehicle.id}

@router.get("/vehicles/{vehicle_id}", response=VehicleOut)
def get_vehicle(request, vehicle_id: int):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    return vehicle

@router.get("/vehicles", response=List[VehicleOut])
def list_vehicles(request):
    qs = Vehicle.objects.all()
    return qs

@router.put("/vehicles/{vehicle_id}")
def update_vehicle(request, vehicle_id: int, payload: VehicleIn):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    skills = Skill.objects.filter(id__in=payload.skills)
    vehicle.skills.set(skills)
    vehicle.capacity = payload.capacity
    vehicle.save()
    return {"success": True}

@router.delete("/vehicles/{vehicle_id}")
def delete_vehicle(request, vehicle_id: int):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    vehicle.delete()
    return {"success": True}

""" Skills CRUD """

@router.post("/skills")
def create_skill(request, payload: SkillIn):
    skill = Skill.objects.create(**payload.dict())
    return {"id": skill.id}

@router.get("/skills/{skill_id}", response=SkillOut)
def get_skill(request, skill_id: int):
    skill = get_object_or_404(Skill, id=skill_id)
    return skill

@router.get("/skills", response=List[SkillOut])
def list_skills(request):
    qs = Skill.objects.all()
    return qs

@router.put("/skills/{skill_id}")
def update_skill(request, skill_id: int, payload: SkillIn):
    skill = get_object_or_404(skill, id=skill_id)
    skills = Skill.objects.filter(id__in=payload.skills)
    skill.skills.set(skills)
    skill.capacity = payload.capacity
    skill.save()
    return {"success": True}

@router.delete("/skills/{skill_id}")
def delete_skill(request, skill_id: int):
    skill = get_object_or_404(Skill, id=skill_id)
    skill.delete()
    return {"success": True}

""" Orders CRUD """
@router.post("/orders")
def create_order(request, payload: OrderIn):
    items = Item.objects.filter(id__in=payload.items)
    skills = Skill.objects.filter(id__in=payload.required_skills)

    order = Order.objects.create(
        email=payload.email,
        address=payload.address,
        location=payload.location,
        delivery_time=payload.delivery_time
    )

    for item_data in payload.order_items:
        item = Item.objects.get(id=item_data['item']['id'])
        OrderItem.objects.create(order=order, item=item, quantity=item_data['quantity'])

    order.required_skills.set(skills)
    order.save()

    return {"id": order.id}

@router.get("/orders/{order_id}", response=OrderOut)
def get_order(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    return order

@router.get("/orders", response=List[OrderOut])
def list_orders(request):
    qs = Order.objects.all()
    return qs

@router.put("/orders/{order_id}")
def update_order(request, order_id: int, payload: OrderIn):
    order = get_object_or_404(Order, id=order_id)

    # Update Order fields
    order.email = payload.email
    order.address = payload.address
    order.location = payload.location
    order.delivery_time = payload.delivery_time

    # Clear existing order items
    OrderItem.objects.filter(order=order).delete()

    # Add new order items
    for item_data in payload.order_items:
        item = Item.objects.get(id=item_data['item']['id'])
        OrderItem.objects.create(order=order, item=item, quantity=item_data['quantity'])

    # Update required skills
    skills = Skill.objects.filter(id__in=payload.required_skills)
    order.required_skills.set(skills)

    order.save()

    return {"success": True}

@router.delete("/orders/{order_id}")
def delete_order(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return {"success": True}

def serialize_vehicle(vehicle):
    vehicle_dict=model_to_dict(vehicle)
    vehicle_dict['skills']=[model_to_dict(skill)['id'] for skill in vehicle_dict['skills']]
    return vehicle_dict

"""  Optimize Routes for given vehicles and orders  """
@router.post("/optimize-routes")
def optimize_routes(request, payload: RouteRequestSchema):
    vehicles = Vehicle.objects.filter(id__in=payload.vehicle_ids)
    vehicles_list=[serialize_vehicle(vehicle) for vehicle in vehicles]
    data = routeoptimizer.setData(vehicles=vehicles_list)
    optimized_routes = routeoptimizer.optimize_routes(data)

    return optimized_routes

@router.get("/optimize-routes-test")
def optimize_routes_test(request):
    data = routeoptimizer.setData()
    optimized_routes = routeoptimizer.optimize_routes(data)

    return optimized_routes


"""  Get Routes By Vehicle Id """
@router.get("/route-by-vehicle/{vehicle_id}")
def get_route_by_vehicle():
    pass

"""  Get Routes By Id """
@router.get("/route-by-id/{route_id}")
def get_route_by_id():
    pass



