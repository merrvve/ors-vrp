import environ
import datetime
import openrouteservice as ors
from openrouteservice import convert
from .models import *
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
ORS_API_KEY=env('ORS_API_KEY')


def generate_pickup_delivery_locations(order_ids):
    result_dict = {}

    for order_id in order_ids:
        order = Order.objects.get(pk=order_id)

        pickup_delivery_dict = {'pickup': {'location': []}, 'delivery': {'location': []}}

        for order_item in order.orderitem_set.all():
            # Set delivery location as Order's location
            pickup_delivery_dict['delivery']['location'].append(order.location)

            # Find the first warehouse with the ordered item and set pickup location
            warehouses_with_item = Warehouse.objects.filter(items=order_item.item)
            if warehouses_with_item.exists():
                warehouse = warehouses_with_item.first()
                pickup_delivery_dict['pickup']['location'].append(warehouse.location)

        result_dict[order_id] = pickup_delivery_dict

    return result_dict


def setData(vehicles = None):
    data = {} 
    data['start_time']= datetime.datetime.now()
    
    #�rnek lokasyonlar
    locations= [ 
        [41.034949993918524, 29.031396215507783], #0-kuzguncuk bostan� 
        [41.034415862984325, 29.02950794048176], #1-mente� sokak, �sk�dar
        [41.030531143952444, 29.025430983215802], #2-fethipa�a korusu
        [41.02918762529382, 29.02817756507183], #3-�sk�dar lisesi
        [41.02106118095182, 29.038412874048447], #4-capitol avm
        [41.021903010548584, 29.048970048761184], #5-altunizade metro
        [41.01430996561763, 29.046652620337948], #6-valideba� korusu
        [40.99170373971553, 29.021525686851778], #7-kad�k�y meydan�
        [40.99693495276592, 29.018714731983497], #8-haydarpa�a gar�
    ]
    
    #google maps lokasyonlar�n�n hesaplama �ncesi ters �evrilmesi gerekiyor
    for loc in locations:
        loc.reverse()
    
    # skills
    # ara�lar�n �zellikleri, belirli �zellikleri gerektiren i�ler yaln�zca o belirli �zelli�i olan araca verilir
    # 0 - b�y�k paket ta��ma
    # 1 - xl paket ta��ma
    # 2 - xxl paket ta��ma
        
    # �r�n tipleri
    # ��in miktar� ve arac�n kapasitesi integer list olarak verilir. listenin her bir indeksi bir �r�ni temsil eder
    # �rnek �r�n tipleri
    # 0 - k���k paket
    # 1 - b�y�k paket
    if vehicles is None:
        data['vehicles_list'] =[
          { 
            "id":1, 
           "start": locations[0], 
           "end": locations[0], 
           "capacity": [10,0],
              "skills": [0],
              "time_window": [0,10800]
          },
             { 
            "id":2, 
           "start": locations[1], 
           "end": locations[1], 
           "capacity": [15,10],
                 "skills": [0,1],
              "time_window": [0,10800]
          },
            { 
            "id":3, 
           "start": locations[2], 
           "end": locations[2], 
           "capacity": [15,0],
                "skills":[0,1,2],
              "time_window": [0,10800]
          },
        ]
        
    else:
        data['vehicles_list']=vehicles

    data['num_vehicles']=len(data['vehicles_list'])
    data['shipment_list'] = [
      {
        "pickup": { "location": locations[1], "service": 600,"time_windows":[[0,7200]]},
        "delivery": { "location": locations[4], "service": 600,"time_windows":[[0,7200]]},
          "amount": [10,10],
          "skills": [0],
          "priority": 0,
      },
      {
        "pickup": { "location": locations[3], "service": 600,"time_windows":[[0,7200]]}, 
       "delivery": { "location": locations[6], "service": 600,"time_windows":[[0,7200]]},
          "amount": [5,0],
          "skills": [2],
          "priority": 0,
      },
        {
        "pickup": { "location": locations[2], "service": 600,"time_windows":[[0,7200]]}, 
       "delivery": { "location": locations[8], "service": 600,"time_windows":[[0,7200]]},
          "amount": [2,0],
          "skills": [1,2],
          "priority": 0,
      },
        {
        "pickup": { "location": locations[4], "service": 600,"time_windows":[[0,7200]]}, 
       "delivery": { "location": locations[7], "service": 600,"time_windows":[[0,7200]]},
          "amount": [2,0],
          "skills": [0],
          "priority": 0,
      },
         {
        "pickup": { "location": locations[0], "service": 600,"time_windows":[[0,7200]]}, 
       "delivery": { "location": locations[6], "service": 600,"time_windows":[[0,7200]]},
          "amount": [3,0],
          "skills": [0],
          "priority": 0,
      },
    ]

    return data

def setOrsRequest(data):
    request={}
    request['vehicles']=[ors.optimization.Vehicle(**vehicle) for vehicle in data['vehicles_list']]
    
    request['shipments'] = []
    for idx, shipment in enumerate(data['shipment_list']):
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

        request['shipments'].append(ors.optimization.Shipment(
            pickup=pickup_step,
            delivery=delivery_step,
            amount=shipment['amount'],
            skills=shipment['skills'],
            priority=shipment['priority'],
            
        ))

    return request

def optimize_routes(data):
    client = ors.Client(key=ORS_API_KEY)
    orsrequest=setOrsRequest(data)
    optimized_results = client.optimization( vehicles=orsrequest['vehicles'], shipments=orsrequest['shipments'], geometry=True)
    return optimized_results