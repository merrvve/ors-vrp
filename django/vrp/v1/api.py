from ninja import Router
from .models import *
from .schema import *
from typing import List
from v1 import routeoptimizer
from django.forms.models import model_to_dict
router = Router()


router = Router()

@router.post("/fulfillments", tags=["Fulfillments"])
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


@router.post("/fulfillments", response=FulfillmentOutSchema, tags=["Fulfillments"])
def create_fulfillment(request, payload: FulfillmentInSchema):
    """ Create fulfillment and return to the created fulfillment """
    destination = get_object_or_404(Destination, pk=payload.destination)
    fulfillment = Fulfillment.objects.create(destination=destination, **payload.dict())
    fulfillment.fulfillment_line_items.set(payload.fulfillment_line_items)
    return fulfillment

@router.get("/fulfillments/{fulfillment_id}", response=FulfillmentOutSchema, tags=["Fulfillments"])
def get_fulfillment(request, fulfillment_id: str):
    """ Get fulfillment by id  and return to the fulfillment or 404"""
    fulfillment = get_object_or_404(Fulfillment, pk=fulfillment_id)
    return fulfillment

@router.put("/fulfillments/{fulfillment_id}", response=FulfillmentOutSchema, tags=["Fulfillments"])
def update_fulfillment(request, fulfillment_id: str, payload: FulfillmentUpdateSchema):
    """ Update fulfillment and return to the updated fulfillment """
    fulfillment = get_object_or_404(Fulfillment, pk=fulfillment_id)
    for key, value in payload.dict().items():
        setattr(fulfillment, key, value)
    fulfillment.save()
    return fulfillment

@router.delete("/fulfillments/{fulfillment_id}", tags=["Fulfillments"])
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

@router.post("/optimize-routes", tags=["Routes"])
def optimize_routes(request, payload: RouteRequestSchema):
    """  Creates routes for specified vehicles, fulfillments and route date. 
    Saves routes to database and returns the optimized_routes response from ors """

    # Create vehicles and shipment objects for ors request
    vehicles = Vehicle.objects.filter(id__in=payload.vehicle_ids)
    vehicles_list=[serialize_vehicle(vehicle) for vehicle in vehicles]
    shipments_list = routeoptimizer.create_shipments_from_fulfillments(payload.fulfillment_ids)    
    
    # Optimize routes with ors client
    optimized_routes = routeoptimizer.optimize_routes(vehicles_list, shipments_list)

    # Retrieve routes from response and save to db
    routeoptimizer.saveRoutes(optimized_routes, payload.planned_date)

    return optimized_routes


"""  Get Routes By Vehicle Id """
@router.get("/route/{vehicle_id}/{job_date}", tags=["Routes"])
def get_route(request, vehicle_id: int, job_date: date):
    """ Get the route of the vehicle for the given job date or return 404 """
    route = get_object_or_404(Route, vehicle_id=vehicle_id, job_date=job_date)
    return route


@router.put("/update_delivery_status/{fulfillment_id}", tags=["Fulfillments"])
def update_delivery_status(request, fulfillment_id: str, delivered: bool, status: str):
    """ Update delivery status. return success or error message """
    try:
        fulfillment = Fulfillment.objects.get(id=fulfillment_id)
        fulfillment.delivered = delivered
        fulfillment.status = status
        fulfillment.delivered_at = datetime.now() if delivered else None  # Set delivered_at only if delivered is True
        fulfillment.updated_at = datetime.now()
        fulfillment.save()
        return {"message": "Delivery status updated successfully"}
    except Fulfillment.DoesNotExist:
        return {"error": f"Fulfillment with ID {fulfillment_id} does not exist"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/fulfillment_delivery_status/{fulfillment_id}", tags=["Fulfillments"])
def get_fulfillment_delivery_status(request, fulfillment_id: str):
    """ Gets delivery status of a fulfillment. returns delivery status data or error message """
    try:
        fulfillment = Fulfillment.objects.get(id=fulfillment_id)
        delivery_status = {
            "id": fulfillment.id,
            "delivered": fulfillment.delivered,
            "delivered_at": fulfillment.delivered_at,
            "status": fulfillment.status
        }
        return delivery_status
    except Fulfillment.DoesNotExist:
        return {"error": f"Fulfillment with ID {fulfillment_id} does not exist"}
    except Exception as e:
        return {"error": str(e)}

""" Skills CRUD """

@router.post("/skills", tags=["Skills"])
def create_skill(request, payload: SkillIn):
    skill = Skill.objects.create(**payload.dict())
    return {"id": skill.id}

@router.get("/skills/{skill_id}", response=SkillOut, tags=["Skills"])
def get_skill(request, skill_id: int):
    skill = get_object_or_404(Skill, id=skill_id)
    return skill

@router.get("/skills", response=List[SkillOut], tags=["Skills"])
def list_skills(request):
    qs = Skill.objects.all()
    return qs

@router.put("/skills/{skill_id}", tags=["Skills"])
def update_skill(request, skill_id: int, payload: SkillIn):
    skill = get_object_or_404(skill, id=skill_id)
    skills = Skill.objects.filter(id__in=payload.skills)
    skill.skills.set(skills)
    skill.capacity = payload.capacity
    skill.save()
    return {"success": True}

@router.delete("/skills/{skill_id}", tags=["Skills"])
def delete_skill(request, skill_id: int):
    skill = get_object_or_404(Skill, id=skill_id)
    skill.delete()
    return {"success": True}




""" Vehicle CRUD """


@router.post("/vehicles", tags=["Vehicles"])
def create_vehicle(request, vehicle_data: VehicleSchemaCreate):
    skills = Skill.objects.filter(id__in=vehicle_data.skills)
    vehicle = Vehicle.objects.create(
        capacity=vehicle_data.capacity,
        end=vehicle_data.end,
        start=vehicle_data.start,
        time_window=vehicle_data.time_window
    )
    vehicle.skills.set(skills)
    return vehicle


@router.get("/vehicles/{vehicle_id}", tags=["Vehicles"])
def read_vehicle(request, vehicle_id: int):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    return vehicle


@router.put("/vehicles/{vehicle_id}", tags=["Vehicles"])
def update_vehicle(request, vehicle_id: int, vehicle_data: VehicleSchemaUpdate):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    vehicle.capacity = vehicle_data.capacity
    vehicle.end = vehicle_data.end
    vehicle.start = vehicle_data.start
    vehicle.time_window = vehicle_data.time_window
    vehicle.save()
    vehicle.skills.clear()
    skills = Skill.objects.filter(id__in=vehicle_data.skills)
    vehicle.skills.set(skills)
    return vehicle


@router.delete("/vehicles/{vehicle_id}", tags=["Vehicles"])
def delete_vehicle(request, vehicle_id: int):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    vehicle.delete()
    return {"message": "Vehicle deleted successfully"}
