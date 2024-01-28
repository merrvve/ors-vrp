import environ
from datetime import datetime
import openrouteservice as ors
from openrouteservice import convert
from .models import *
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
ORS_API_KEY=env('ORS_API_KEY')
from django.forms.models import model_to_dict


def create_shipments_from_fulfillments(fulfillment_ids):
    """ generates shipments list from fulfillment data for route optimizer function """
    shipments = []
    for fulfillment_id in fulfillment_ids:
        fulfillment = Fulfillment.objects.get(id=fulfillment_id)
        shipment_data = {
            "pickup": {
                "description": fulfillment_id,
                "location": [29.02817756507183,41.02918762529382],  # Default pickup location
                "service": 600, # Default service time, set later
                "time_windows": None # Pickup time window, not set yet
            },
            "delivery": {
                "description": fulfillment_id,
                "location": [ float(fulfillment.destination.longitude),float(fulfillment.destination.latitude)],  # Delivery location from destination
                "service": 600, # Default service time, set later
                "time_windows": None # Delivery time window, not set yet
            },
            "amount": [fulfillment.total_quantity],
            "skills": [],  # Not used yet
            "priority": 0,  # Not used yet
        }
        shipments.append(shipment_data)
    return shipments



def setOrsRequest(vehicles_list, shipments_list):
    """ Set vehicles and shipments as ors objects for route optimizer function """
    request={}
    request['vehicles']=[ors.optimization.Vehicle(**vehicle) for vehicle in vehicles_list]
    related_ids = {}
    request['shipments'] = []
    for idx, shipment in enumerate(shipments_list):
        pickup_step = ors.optimization.ShipmentStep(
            id=idx,
            location=shipment["pickup"]["location"],
            service=shipment["pickup"]["service"],  
            time_windows=shipment["pickup"]['time_windows']
        )
        delivery_step = ors.optimization.ShipmentStep(
            id=idx,
            location=shipment["delivery"]["location"],
            service=shipment["delivery"]["service"], 
            time_windows=shipment["delivery"]['time_windows']
        )
        # save related fulfillment and shipment ids
        related_ids[idx]= shipment["pickup"]["description"]
        
        request['shipments'].append(ors.optimization.Shipment(
            pickup=pickup_step,
            delivery=delivery_step,
            amount=shipment['amount'],
            skills=shipment['skills'],
            priority=shipment['priority'],
            
        ))
    request['related_ids']=related_ids #save fulfillment and shipment ids

    return request


def saveRoutes(optimized_routes, planned_date):
    """ Retrieves routes from ORS response and saves to db. returns saved routes as a list """
    route_data_list = []

    # Retrieve necessary fields for each route
    for route in optimized_routes['routes']:
        route_data = {}
        route_data['vehicle'] = Vehicle.objects.get(id=route['vehicle']) 
        route_data['job_date'] = planned_date
        ids_set= set()
        route_data['fulfillment_ids'] = []
        route_data['steps'] = []
        route_data['googlelink'] = ""  # empty for now, set later
        for step in route['steps']:
            route_data['steps'].append(step['location'])
            if step['type'] != 'start' and step['type'] != 'end':
                ids_set.add(optimized_routes['related_ids'][step['id']])
        route_data['fulfillment_ids']=list(ids_set)
        route_data_list.append(route_data)
    
        # Create and save Route object
        route_db = Route(**route_data)
        route_db.save()

    return route_data_list



def optimize_routes(vehicles, shipments):
    """  Main route optimizer function. Creates optimized routes for given vehicles and shipments. returns optimized routes dictionary """
    client = ors.Client(key=ORS_API_KEY) # Create ors client
    ors_request=setOrsRequest(vehicles, shipments) # Create objects for ors request
    optimized_results = client.optimization( vehicles=ors_request['vehicles'], shipments=ors_request['shipments'], geometry=True) #main function
    optimized_results['related_ids']=ors_request['related_ids']
    return optimized_results