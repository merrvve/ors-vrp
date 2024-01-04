
import openrouteservice as ors
from openrouteservice import convert
from dotenv import load_dotenv
import os
import datetime
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
    data['start_time']= datetime.datetime.now()
    
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
    
    # skills
    # araçların özellikleri, belirli özellikleri gerektiren işler yalnızca o belirli özelliği olan araca verilir
    # 0 - büyük paket taşıma
    # 1 - xl paket taşıma
    # 2 - xxl paket taşıma
        
    # ürün tipleri
    # İşin miktarı ve aracın kapasitesi integer list olarak verilir. listenin her bir indeksi bir ürüni temsil eder
    # örnek ürün tipleri
    # 0 - küçük paket
    # 1 - büyük paket
        
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
    print("Görev başlangıcı: ", data['start_time'])
    print('INPUT:\n\n', 'Vehicles:')
    time_change1=datetime.timedelta(seconds=0)
    time_change2=datetime.timedelta(seconds=0)
    
    for vehicle in data['vehicles_list']:
        print('----\n Vehicle id ',vehicle['id'])
        print('  - 0 nolu ürün (örn. küçük paket) için araç kapasitesi ',vehicle['capacity'][0])
        print('  - 1 nolu ürün (örn. büyük paket) için araç kapasitesi ',vehicle['capacity'][1])
        print('   Vehicle start loc: ',vehicle['start'],)
        print('   Vehicle end loc: ',vehicle['end'])
        time_change1=datetime.timedelta(seconds=vehicle['time_window'][0])
        time_change2=datetime.timedelta(seconds=vehicle['time_window'][1])
        print('   Çalıştığı zaman aralığı: ',data['start_time']+time_change1,'-',data['start_time']+time_change2)
        print('   Vehicle skills: ',vehicle['skills'])
    print('\n Pickup and deliveries: ')
    for pad in data['shipment_list']:
        print('----\n','  Pickup loc: ', pad['pickup']['location'])
        print('  İşin gerçekleşmesi gereken zaman aralığı: ',pad['pickup']['time_windows'])
        print('  Delivery loc: ', pad['delivery']['location'])
        print('  İşin gerçekleşmesi gereken zaman aralığı: ',pad['delivery']['time_windows'])
        print('  0 nolu ürün (örn. küçük paket) miktarı: ',pad['amount'][0])
        print('  1 nolu ürün (örn. büyük paket) miktarı: ',pad['amount'][1])
       
        print('  Required skills: ',pad['skills'])
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

def print_results(results,start_time):
    time_change=datetime.timedelta(seconds=0)
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
                print('- Setup time (sec): ', step['setup'])
                print('- Service time (sec): ', step['service'])
                print('- Waiting time (sec): ', step['waiting_time'])
                print('- Arrival (sec): ', step['arrival'])
                time_change= datetime.timedelta(seconds=step['arrival'])
                print('- Varış zamanı: ',start_time+time_change)
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
    print_results(optimized_results,data['start_time'])
main()