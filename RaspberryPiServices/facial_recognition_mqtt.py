#! /usr/bin/python

# import the necessary packages
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import paho.mqtt.client as paho
from paho import mqtt
#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "/home/pi/server/encodings.pickle"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

# initialize the video stream and allow the camera sensor to warm up
# Set the ser to the followng
# src = 0 : for the build in single web cam, could be your laptop webcam
# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
#vs = VideoStream(src=2,framerate=10).start()
vs = WebcamVideoStream(src=0).start() 
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()


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





# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to 500px (to speedup processing)
	frame = vs.read()
	if( not isinstance(frame, type(None)) ):
		frame = imutils.resize(frame, width=1000)

		# Detect the fce boxes
		boxes = face_recognition.face_locations(frame)
		# compute the facial embeddings for each face bounding box
		encodings = face_recognition.face_encodings(frame, boxes)
		
		names = []
		# loop over the facial embeddings
		for encoding in encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"],
				encoding)
			name = "Unknown" #if face is not recognized, then print Unknown

			# check to see if we have found a match
			if True in matches:

				# find the indexes of all matched faces then initialize a
				# dictionary to count the total number of times each face
				# was matched
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}

				# loop over the matched indexes and maintain a count for
				# each recognized face face
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1

				# determine the recognized face with the largest number
				# of votes (note: in the event of an unlikely tie Python
				# will select first entry in the dictionary)
				name = max(counts, key=counts.get)
				if currentname != name:
					currentname = name
					print(currentname)
			names.append(name)
			print(names)

		# loop over the recognized faces
		for ((top, right, bottom, left), name) in zip(boxes, names):
			print(name)
# draw the predicted face name on the image - color is in BGR
			if name == "Unknown" :
			  filename = 'unknown.png'
			  cv2.imwrite(filename, frame)
			  f = open('unknown.png','rb') 
			  payload =  b''.join(f.readlines())
			  bts = bytearray()
			  bts += payload
			  client.publish("image", payload=payload, qos=1)
			  time.sleep(1)
			  f.close()
	# loop_forever for simplicity, here you need to stop the loop manually

	# you can also use loop_start and loop_s
			  client.loop_start()
			  client.loop_stop()

			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 255, 225), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				.8, (0, 255, 255), 2)

		# display the image to our screen
		#cv2.imshow("Facial Recognition is Running", frame)
		key = cv2.waitKey(1) & 0xFF

		# quit when 'q' key is pressed
		if key == ord("q"):
			break

		# update the FPS counter
		fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup

cv2.destroyAllWindows()
