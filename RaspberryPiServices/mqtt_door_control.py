import time
import paho.mqtt.client as paho
from paho import mqtt
import RPi.GPIO as GPIO

RED_PIN = 17 
GREEN_PIN = 27 

GPIO.setmode(GPIO.BCM)

GPIO.setup(RED_PIN,GPIO.OUT)
GPIO.setup(GREEN_PIN,GPIO.OUT) 



pic_filename = "/home/pi/Documents/application/images/sabri.png"

#setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print(type(msg.payload))
    print(str(msg.payload))
    if(msg.payload.decode("utf-8") =="Allowed"):
      GPIO.output(GREEN_PIN,GPIO.HIGH)
      time.sleep(3)
      GPIO.output(GREEN_PIN,GPIO.LOW)
    elif(msg.payload.decode("utf-8") == "Not Allowed") :
      GPIO.output(RED_PIN,GPIO.HIGH)
      time.sleep(3)
      GPIO.output(RED_PIN,GPIO.LOW)
# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("sabrimahmoud​", "Smlove1234")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("64d5b1153332478697d43513819c8286.s2.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish
# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("control/#", qos=1)
# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()
