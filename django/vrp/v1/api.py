from ninja import Router
from .models import *
from .schema import *
from typing import List
from v1 import routeoptimizer
from django.forms.models import model_to_dict
router = Router()


router = Router()

@router.post("/fulfillments")
def create_fulfillments(request, fulfillments: List[FulfillmentSchema]):
    """    Recieves multiple fulfillments and adds to database.     Returns the created fulfillments"""
    created_fulfillments = []
    for fulfillment_data in fulfillments:
        destination_data = fulfillment_data.pop("destination")
        fulfillment_line_items_data = fulfillment_data.pop("fulfillment_line_items")
        
        # Create destination object
        destination = Destination.objects.create(**destination_data)
        
        # Create fulfillment object
        fulfillment = Fulfillment.objects.create(destination=destination, **fulfillment_data)
        
        # Create fulfillment line items
        for line_item_data in fulfillment_line_items_data:
            FulfillmentLineItem.objects.create(fulfillment=fulfillment, **line_item_data)
        
        created_fulfillments.append(fulfillment)
    
    return created_fulfillments


@router.post("/fulfillments", response=FulfillmentOutSchema)
def create_fulfillment(request, payload: FulfillmentInSchema):
    """ Create fulfillment and return to the created fulfillment """
    destination = get_object_or_404(Destination, pk=payload.destination)
    fulfillment = Fulfillment.objects.create(destination=destination, **payload.dict())
    fulfillment.fulfillment_line_items.set(payload.fulfillment_line_items)
    return fulfillment

@router.get("/fulfillments/{fulfillment_id}", response=FulfillmentOutSchema)
def get_fulfillment(request, fulfillment_id: str):
    """ Get fulfillment by id  and return to the fulfillment or 404"""
    fulfillment = get_object_or_404(Fulfillment, pk=fulfillment_id)
    return fulfillment

@router.put("/fulfillments/{fulfillment_id}", response=FulfillmentOutSchema)
def update_fulfillment(request, fulfillment_id: str, payload: FulfillmentUpdateSchema):
    """ Update fulfillment and return to the updated fulfillment """
    fulfillment = get_object_or_404(Fulfillment, pk=fulfillment_id)
    for key, value in payload.dict().items():
        setattr(fulfillment, key, value)
    fulfillment.save()
    return fulfillment

@router.delete("/fulfillments/{fulfillment_id}")
def delete_fulfillment(request, fulfillment_id: str):
    """ Delete fulfillment and return true or 404 """
    fulfillment = get_object_or_404(Fulfillment, pk=fulfillment_id)
    fulfillment.delete()
    return {"success": True}


def serialize_vehicle(vehicle):
    """ Convert vehicle object to json-friendly dict for route optimizer function """
    vehicle_dict=model_to_dict(vehicle)
    vehicle_dict['skills']=[model_to_dict(skill)['id'] for skill in vehicle_dict['skills']]
    return vehicle_dict

@router.post("/optimize-routes")
def optimize_routes(request, payload: RouteRequestSchema):
    """  Creates routes for given vehicle ids, 
    given fulfillment ids and route date. 
    Saves route to database and returns the created route object  """

    vehicles = Vehicle.objects.filter(id__in=payload.vehicle_ids)
    vehicles_list=[serialize_vehicle(vehicle) for vehicle in vehicles]
    shipments_list = routeoptimizer.create_shipments_from_fulfillments(payload.fulfillment_ids)    
    
    optimized_routes = routeoptimizer.optimize_routes(vehicles_list, shipments_list)

    return vehicles


"""  Get Routes By Vehicle Id """
@router.get("/route-by-vehicle/{vehicle_id}")
def get_route_by_vehicle():
    pass

"""  Get Routes By Id """
@router.get("/route-by-id/{route_id}")
def get_route_by_id():
    pass







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


