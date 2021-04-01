# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from datetime import datetime

def helloworld(self, params, packet):
    print('Topic: {}'.format(packet.topic))
    print('Payload: {}'.format(packet.payload))


ENDPOINT = "a1gubz9fjm577v-ats.iot.ap-northeast-1.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERT = "certificates/466fc5c4a0-certificate.pem.crt"
PATH_TO_KEY = "certificates/466fc5c4a0-private.pem.key"
PATH_TO_ROOT = "certificates/root.pem"
TOPIC = "home/helloworld"


myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe('home/helloworld', 1, helloworld)


while True:
    t.sleep(2)

    print('Begin Publish')

    for i in range(20):
        data = "hello at {}".format(datetime.now())
        message = {"message" : data}
        myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 1) 
        print('Published')
        t.sleep(1)
    print('Publish End')


myAWSIoTMQTTClient.disconnect()
