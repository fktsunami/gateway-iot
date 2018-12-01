from aws_mqtt import AWSMQTT
import json
import time

gateway_id = 'gateway001'
gateway_sim_mqtt = AWSMQTT(gateway_id)

sensor_ids = ['TSUNAMI069' , 'TSUNAMI096']
lats = [16.004468, 16.005782]
lngs = [108.342568, 108.387031]

if __name__ == '__main__':
    while(True):
        gateway_sim_mqtt.config()
        gateway_sim_mqtt.start()
        while(True):
            for index in range(0, len(lats)):
                msg = {
                    'force': 100.1,
                    'gatewayId' : 'GateWay69',
                    'lat': lats[index],
                    'lng': lngs[index],
                    'sensorID': sensor_ids[index],
                    'gyroscope': {
                        'gyroscope_x': 69.69,
                        'gyroscope_z': 96.96,
                        'gyroscope_y': 35.35,
                    }        
                }
                print(msg)
                topic = sensor_ids[index] + '/tsunamiSensor'
                if not gateway_sim_mqtt.publish(topic, json.dumps(msg)):
                    print('Publish failed')
                time.sleep(0.5)               
        