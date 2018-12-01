import time
import boto3
from boto3.session import Session
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


cognitoIdentityPoolID = 'us-west-2:6edcd2e6-3900-4caa-adf4-2b082359d4fa'
host = 'a3n0rmdkx656cj.iot.us-west-2.amazonaws.com'

port = "443"
region = 'us-west-2'
rootCAPath = '/home/pi/certs/root-CA.crt'


class AWSMQTT(AWSIoTMQTTClient):
    def __init__(self, clientId):
        AWSIoTMQTTClient.__init__(self, clientId, useWebsocket=True)
        print 'init AWSMQTT'
        self.clientId = clientId            

    def setCallbacks(self, mqttCallback):
        self.mqttCallback = mqttCallback
        
    def config(self):
        print('Configure MQTT')
        # Cognito auth
        identityPoolID = cognitoIdentityPoolID
        cognitoIdentityClient = boto3.client('cognito-identity', region_name=region)

        temporaryIdentityId = cognitoIdentityClient.get_id(IdentityPoolId=identityPoolID)
        identityID = temporaryIdentityId["IdentityId"]

        temporaryCredentials = cognitoIdentityClient.get_credentials_for_identity(IdentityId=identityID)
        AccessKeyId = temporaryCredentials["Credentials"]["AccessKeyId"]
        SecretKey = temporaryCredentials["Credentials"]["SecretKey"]
        SessionToken = temporaryCredentials["Credentials"]["SessionToken"]

        # AWSIoTMQTTClient configuration
        AWSIoTMQTTClient.configureEndpoint(self, host, port)
        AWSIoTMQTTClient.configureCredentials(self, rootCAPath)
        AWSIoTMQTTClient.configureIAMCredentials(self, AccessKeyId, SecretKey, SessionToken)
        AWSIoTMQTTClient.configureAutoReconnectBackoffTime(self, 1, 32, 20)
        AWSIoTMQTTClient.configureOfflinePublishQueueing(self, -1)  # Infinite offline Publish queueing
        AWSIoTMQTTClient.configureDrainingFrequency(self, 2)  # Draining: 2 Hz
        AWSIoTMQTTClient.configureConnectDisconnectTimeout(self, 10)  # 10 sec
        AWSIoTMQTTClient.configureMQTTOperationTimeout(self, 5)  # 5 sec
        print('Configure MQTT done')
        return self

    def start(self):
        # Connect and subscribe to AWS IoT
        try:
            if AWSIoTMQTTClient.connect(self) == True:
                print("Connected to MQTT broker")
                time.sleep(2)
                return True
            else:
                print('Connection failed')
                return False
        except:
            print('Connection error')
            

    def subscribe(self, topic):
        return AWSIoTMQTTClient.subscribe(self, topic, 1, self.mqttCallback)

    def publish(self, topic, message):
        return AWSIoTMQTTClient.publish(self, topic, message, 1)
