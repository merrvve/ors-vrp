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
                "location": [0.0, 0.0],  # Default pickup location
                "service": 600, # Default service time, set later
                "setup": 600, # Default setup time in seconds, set later
                "time_windows": None # Pickup time window, not set yet
            },
            "delivery": {
                "description": fulfillment_id,
                "location": [float(fulfillment.destination.longitude), float(fulfillment.destination.latitude)],  # Delivery location from destination
                "service": 600, # Default service time, set later
                "setup": 600, # Default setup time in seconds, set later
                "time_windows": None # Delivery time window, not set yet

            },
            "amount": fulfillment.total_quantity,
            "skills": [],  # Not used yet
            "priority": 0,  # Not used yet
        }
        shipments.append(shipment_data)
    return shipments



def setOrsRequest(vehicles_list, shipments_list):
    """ Set vehicles and shipments as ors objects for route optimizer function """
    request={}
    request['vehicles']=[ors.optimization.Vehicle(**vehicle) for vehicle in vehicles_list]
    
    request['shipments'] = []
    for idx, shipment in enumerate(shipment_list):
        pickup_step = ors.optimization.ShipmentStep(
            id=idx,
            description=shipment["pickup"]["description"],
            location=shipment["pickup"]["location"],
            service=shipment["pickup"]["service"],  
            setup=shipment["pickup"]["setup"],  
            time_windows=shipment["pickup"]['time_windows']

        )
        delivery_step = ors.optimization.ShipmentStep(
            id=idx,
            description=shipment["delivery"]["description"],
            location=shipment["delivery"]["location"],
            service=shipment["delivery"]["service"], 
            setup=shipment["delivery"]["setup"], 
            time_windows=shipment["delivery"]['time_windows']
        )

        request['shipments'].append(ors.optimization.Shipment(
            pickup=pickup_step,
            delivery=delivery_step,
            amount=shipment['amount'],
            skills=shipment['skills'],
            priority=shipment['priority'],
            
        ))

    return request

def optimize_routes(vehicles, shipments):
    """  Main route optimizer function. Creates optimized routes for given vehicles and shipments. returns optimized routes dictionary """
    client = ors.Client(key=ORS_API_KEY) # Create ors client
    ors_request=setOrsRequest(vehicles, shipments) # Create objects for ors request
    optimized_results = client.optimization( vehicles=ors_request['vehicles'], shipments=ors_request['shipments'], geometry=True) #main function
    return optimized_results