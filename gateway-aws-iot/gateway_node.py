from aws_mqtt import AWSMQTT
import serial
import time
import json

com_port = '/dev/ttyACM0'
# com_port = '/dev/ttyACM1'
baudrate = 9600
MESSAGE_FIELDS = ['sensorID', 'lat', 'lng', 'force', 'gyroscope_x', 'gyroscope_y', 'gyroscope_z']

class GateWaysNode():
    def __init__(self, clientId, publish_topic):
        self.debug('Init GateWaysNode')
        self.utm_mqtt = AWSMQTT(clientId)
        self.utm_mqtt.setCallbacks(self.mqttCallback)                
        self._publish_topic = publish_topic
        self._serial_com = serial.Serial(com_port, baudrate)
        self._gateway_id = clientId

    def mqttCallback(self, client, userdata, message):
        str = message.payload
        # self.debug(str)
        try:
            dict = json.loads(str)
            # parse json msg here            
        except:
            self.debug("mqttCallback: Parse json error")

    def config(self):
        self.debug("Configure mqtt")
        self.utm_mqtt = self.utm_mqtt.config()
    
    def start(self):
        self.debug('Start GatewayNode')
        if not self.utm_mqtt.start():
            self.debug('MQTT error')
        while(True):
            self.debug("-------------------------------")
            self.debug('Reading serial data')
            try:
                values = self.read_serial_data()
                self.clear_serial_buffer()
                self.debug(values)
                if not self.validate_data(values):
                    self.debug('Invalid received data')
                else:
                    msg = self.create_mqtt_message(values)
                    topic = msg['sensorID'] + '/tsunamiSensor'
                    self.send(topic, msg)
                        
            except Exception as e:
                self.debug(e)
                pass
            
            # data = self.read_serial_data()
            # self.debug(data)
            
            time.sleep(0.5)

    def listen(self, topic):
        self.utm_mqtt.subscribe(topic)

    def send(self, topic, message):
        self.debug('Sending message')
        if self.utm_mqtt.publish(topic, json.dumps(message)):
            self.debug('Mesage sent')
        else:
            self.debug('Failed to send')
    
    def read_serial_data(self):
        return self._serial_com.readline() 
    
    def clear_serial_buffer(self):
        # From v3.0
        # self._serial_com.reset_input_buffer()
        # self._serial_com.reset_input_buffer()

        #For older verion       
	    self._serial_com.flushInput()
    
    def create_mqtt_message(self, values_in_str):
        self.debug('create_mqtt_message')
        splited_values = values_in_str.split('_')        
        # for s in splited_values:
            # print(s)
            # if s.isdigit():
            # values.append(float(s))
            # else:
                # self.debug('Not digit only')
        # self.debug(values)
        json_msg = {}
        for field in MESSAGE_FIELDS:
            # self.debug(field)
            json_msg.update({
                field: splited_values[MESSAGE_FIELDS.index(field)]
            })
        # Reformat
        return_mqtt_msg = {
            'gyroscope': {}
        }
        for key in json_msg:
            if key == 'lat' or key == 'lng' or key == 'force':
                # print(type(json_msg[key]))
                # return_mqtt_msg[key] = float(json_msg[key])
                # print(repr(json_msg[key]))
                # return_mqtt_msg[key] = map(float, json_msg[key].strip().split('\r\n'))[0]
                return_mqtt_msg[key] = float(json_msg[key].rstrip('\x00'))
            elif key == 'gyroscope_x' or key == 'gyroscope_y' or key == 'gyroscope_z':
                # print(repr(json_msg[key]))
                json_msg[key] = json_msg[key].strip().split('\r\n')[0]
                json_msg[key] = json_msg[key].rstrip('\x00')
                # print(repr(json_msg[key]))
                return_mqtt_msg['gyroscope'].update({                   
                        key: float(json_msg[key])
                })
            else:
                return_mqtt_msg[key] = json_msg[key]
        
        # Add gateway id
        return_mqtt_msg['gatewayId'] = self._gateway_id
        
        self.debug(return_mqtt_msg)
        return return_mqtt_msg

    def validate_data(self, values_in_str):
        values_in_str = values_in_str.split('_')
        if len(values_in_str) != len(MESSAGE_FIELDS):
            self.debug('Invalid format')
            return False
        return True

    def debug(self, data):
        print('[GateWaysNode]['+ str(time.time()) + ']: ' +  str(data))        
