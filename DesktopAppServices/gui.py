import PySimpleGUI as sg
import time
import paho.mqtt.client as paho
from paho import mqtt
from PIL import Image
import io 
from copy import copy 

image_viewer_column = [
    [sg.Text("This person is trying to access to your Home")],
    [sg.Image(key="IMAGE",filename="placeholder.png")],
    [sg.Button("Allowed"),sg.Button("Not Allowed")],
]
image_viewer_column2 = [
    [sg.Image(key="-IMAGE-",filename="sabri2.png")],
]


# ----- Full layout -----
layout = [
    [
        sg.Column(image_viewer_column),
    ]
    
]

# Create the window
window = sg.Window("Secure Home", layout)



# setting callbacks for different events to see if it works, print the message etc.
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


filename = 'unknown.png'


while True:
    event, values = window.read(timeout=10)
    # End program if user closes window or
    # presses the OK button
    if event == "Allowed":
        client.publish("control", payload=str("Allowed"), qos=1)
        client.loop_start()
        client.loop_stop()
    elif event == "Not Allowed":
        client.publish("control", payload=str("Not Allowed"), qos=1)
        client.loop_start()
        client.loop_stop()
    # Try except show another image OSError: image file is truncated
    elif event == sg.WIN_CLOSED :
    	break
    try:
    	image = Image.open(filename)
    	with io.BytesIO() as bio:
    		image.save(bio, format="PNG")
    		bytes_image = bio.getvalue()
    except Exception as e :
    	image = Image.open("placeholder.png")
    	with io.BytesIO() as bio:
    		image.save(bio, format="PNG")
    		bytes_image = bio.getvalue()
    		
    window['IMAGE'].update(bytes_image)
    print('updated')

    time.sleep(1)

window.close()
