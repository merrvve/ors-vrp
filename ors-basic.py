###
#   openrouteservice ve vroom kullanarak
#   Birden çok ve farklı kapasitelerde araç
#   Birden çok ve farklı miktarlarda pickup ve delivery işleri
#   Mümkün olan en kısa sürede, en az araç ve en kısa mesafe ile
#
##


import openrouteservice as ors
from openrouteservice import convert
from dotenv import load_dotenv
import os
load_dotenv()
ORS_API_KEY=os.getenv('ORS_API_KEY')


def loc_to_string(location):
    #hesaplama sonrası haritada işaretleme için lokasyonların ters çevrilmesi gerekiyor
    return (str(location[1]) + ',' + str(location[0]))

def create_googlemaps_link(steps):
    step_num=len(steps)
    googlelink="https://www.google.com/maps/dir/?api=1&travelmode=driving&origin="+ loc_to_string(steps[0]['location']) +'&destination='+ loc_to_string(steps[step_num-1]['location'])+'&waypoints='
    for i in range(1,step_num-1):
        googlelink+=loc_to_string(steps[i]['location'])+'|'
    return googlelink[:-1]

def setData():
    
    data = {} 
    
    #örnek lokasyonlar

    locations= [ 
        [41.034949993918524, 29.031396215507783], #0-kuzguncuk bostanı 
        [41.034415862984325, 29.02950794048176], #1-menteş sokak, üsküdar
        [41.030531143952444, 29.025430983215802], #2-fethipaşa korusu
        [41.02918762529382, 29.02817756507183], #3-üsküdar lisesi
        [41.02106118095182, 29.038412874048447], #4-capitol avm
        [41.021903010548584, 29.048970048761184], #5-altunizade metro
        [41.01430996561763, 29.046652620337948], #6-validebağ korusu
        [40.99170373971553, 29.021525686851778], #7-kadıköy meydanı
        [40.99693495276592, 29.018714731983497], #8-haydarpaşa garı
    ]
    #google maps lokasyonlarının hesaplama öncesi ters çevrilmesi gerekiyor
    for loc in locations:
        loc.reverse()
    
    data['vehicles_list'] =[
      { 
        "id":1, 
       "start": locations[0], 
       "end": locations[0], 
       "capacity": [10]
      },
         { 
        "id":2, 
       "start": locations[1], 
       "end": locations[1], 
       "capacity": [15]
      },
        { 
        "id":3, 
       "start": locations[2], 
       "end": locations[2], 
       "capacity": [15]
      },
    ]
    data['num_vehicles']=len(data['vehicles_list'])
    data['shipment_list'] = [
      {
        "pickup": { "location": locations[1], "service": 600},
        "delivery": { "location": locations[4], "service": 600},
          "amount": [10],
          "skills": [],
          "priority": 0

      },
      {
        "pickup": { "location": locations[3], "service": 600}, 
       "delivery": { "location": locations[6], "service": 600},
          "amount": [5],
          "skills": [],
          "priority": 0
      },
        {
        "pickup": { "location": locations[2], "service": 600}, 
       "delivery": { "location": locations[8], "service": 600},
          "amount": [2],
          "skills": [],
          "priority": 0
      },
        {
        "pickup": { "location": locations[4], "service": 600}, 
       "delivery": { "location": locations[7], "service": 600},
          "amount": [2],
          "skills": [],
          "priority": 0
      },
         {
        "pickup": { "location": locations[0], "service": 600}, 
       "delivery": { "location": locations[6], "service": 600},
          "amount": [3],
          "skills": [],
          "priority": 0
      },
    ]
    print('INPUT:\n\n', 'Vehicles:')
    for vehicle in data['vehicles_list']:
        print('----\n Vehicle id ',vehicle['id'])
        print('  Vehicle capacity: ',vehicle['capacity'])
        print('   Vehicle start loc: ',vehicle['start'],)
        print('   Vehicle end loc: ',vehicle['end'])
    print('\n Pickup and deliveries: ')
    for pad in data['shipment_list']:
        print('----\n','  Pickup loc: ', pad['pickup']['location'])
        print('  Delivery loc: ', pad['delivery']['location'])
        print('  Amount: ',pad['amount'])
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

        )
        delivery_step = ors.optimization.ShipmentStep(
            id=idx,
            location=shipment["delivery"]["location"],
            service=shipment["delivery"]["service"],  
        )

        request['shipments'].append(ors.optimization.Shipment(
            pickup=pickup_step,
            delivery=delivery_step,
            amount=shipment['amount'],
            skills=shipment['skills'],
            priority=shipment['priority']
        ))

    return request

def print_results(results):
    if not results:
        print('No results')
        return
    print('\n RESULTS SUMMARY: \n\n')
    codes=['No error raised','Internal error','Input error','Routing error']
    print(codes[results['code']])
    print('\n')
    print('Total cost (one hour of travel time with one vehicle defaults to 3600): ', results['summary']['cost'])
    print('Number of routes in the solution: ', results['summary']['routes'])
    unassigned=results['summary']['unassigned']
    print('Number of tasks that could not be served: ', unassigned)
    if(results['summary']['unassigned']>0):
        for unassigned_task in results['unassigned']:
            print('- Unassigned task id: ',unassigned_task['id'],', type: ', unassigned_task['type'],', location: ', unassigned_task['location'])
    print('Total setup time for all routes (sec): ', results['summary']['setup'])
    print('Total service time for all routes (sec): ', results['summary']['service'])
    print('Total travel time for all routes (sec): ', results['summary']['duration'])
    print('Total waiting time for all routes (sec): ', results['summary']['waiting_time'])
    print('Total priority sum for all assigned tasks: ', results['summary']['priority'])
    print('Total delivery for all routes: ', results['summary']['delivery'])
    print('Total pickup for all routes: ', results['summary']['pickup'])
    print('Total distance for all routes (m): ', results['summary']['distance'])
    print('Array of violation objects for all routes (Kural ihlalleri (varsa)):', results['summary']['violations'])
    print('\n RESULTING ROUTES: \n\n')
    for idr, route in enumerate(results['routes']):
        print('ROUTE (ID ',idr,') info:\n', 'VEHICLE ID: ',route['vehicle'])
        print('Number of deliveries: ',route['delivery'])
        print('Number of pickups: ',route['pickup'])
        print('Setup time (sec): ',route['setup'])
        print('Service time (sec): ',route['service'])
        print('Duration (sec): ',route['duration'])
        print('Waiting time (sec): ',route['waiting_time'])
        print('Priority: ',route['priority'])
        print('Distance (m): ',route['distance'])
        print('STEPS: ', )
        print('Google maps link: ', create_googlemaps_link(route['steps']))
        for ids, step in enumerate(route['steps']):
            print('----- Step ',ids,'------')
            print('- Step type: ', step['type'])
            print('- Step location: ', step['location'])
            if(step['type'] != 'start' and  step['type']!='end'):
                print('- Arrival time: ', step['arrival'])
                print('- Setup time (sec): ', step['setup'])
                print('- Service time (sec): ', step['service'])
                print('- Waiting time (sec): ', step['waiting_time'])
                print('- Loads: ', step['load'])
                print('- Duration (sec): ', step['duration'])
                print('- Distance (m)', step['distance'])
                print('- Violations', step['violations'])
                #print('- ID of the job', step['id'])
def main():
    client = ors.Client(key=ORS_API_KEY)
    data=setData()
    request=setOrsRequest(data)
    optimized_results = client.optimization( vehicles=request['vehicles'], shipments=request['shipments'], geometry=True)
    print_results(optimized_results)
main()