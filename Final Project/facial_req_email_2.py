#! /usr/bin/python

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import requests
from flask import Flask, render_template_string, request  # Importing the Flask modules required for this project
# import RPi.GPIO as GPIO  # Importing the GPIO library to control GPIO pins of Raspberry Pi
from time import sleep

import BlynkLib
import RPi.GPIO as GPIO
from BlynkTimer import BlynkTimer
from time import sleep
import time
import BlynkLib
servo_pin = 26

			
GPIO.setmode(GPIO.BCM)  # We are using the BCM pin numbering
			# Declaring Servo Pins as output pins
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(4, GPIO.OUT) 		#led out

BLYNK_AUTH_TOKEN = "wr1D2Ws8I1mgy71ELKP_7lxFQncToT02"

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
p = GPIO.PWM(servo_pin, 50)
p.start(0)

#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"
#use this xml file
cascade = "haarcascade_frontalface_default.xml"

#function for setting up emails
def send_message(name):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxf0768c693bb647ab89629b73c75fbf22.mailgun.org/messages",
        auth=("api", "d983be43b6b16fbd5bc2001be571c09a-30344472-f9b16d3c"),
        files = [("attachment", ("image.jpg", open("image.jpg", "rb").read()))],
        data={"from": "Mailgun Sandbox <postmaster@sandboxf0768c693bb647ab89629b73c75fbf22.mailgun.org>",
            "to": "Akhil <drstrange5940@gmail.com>",
            "subject": "Some one is there at your doorstep!!",
            "text":  name +  ". "+ "If you want to permit , you have 30 seconds . Navigate to your Blynk app and proceed!" })

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())
detector = cv2.CascadeClassifier(cascade)

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
#vs = VideoStream(src=0).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()
counu =0
counk = 0

# loop over frames from the video file stream
while True:
	i=GPIO.input(11)
	if i==0:                 #When output from motion sensor is LOW
		#print ("No intruders",i)
		GPIO.output(4, 0)  #Turn OFF LED
		time.sleep(0.1)
	elif i==1:               #When output from motion sensor is HIGH
		#print ("Intruder detected",i)
		GPIO.output(4, 1)  #Turn ON LED
		time.sleep(0.1)
	# grab the frame from the threaded video stream and resize it
	# to 500px (to speedup processing)
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	
	# convert the input frame from (1) BGR to grayscale (for face
	# detection) and (2) from BGR to RGB (for face recognition)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# detect faces in the grayscale frame
	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)

	# OpenCV returns bounding box coordinates in (x, y, w, h) order
	# but we need them in (top, right, bottom, left) order, so we
	# need to do a bit of reordering
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

	# compute the facial embeddings for each face bounding box
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []

	# loop over the facial embeddings
	for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown"

		# check to see if we have found a match
		if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}
			counu =counu - 1
			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
			name = max(counts, key=counts.get)
			counk += 1
			print("yeye")
			#If someone in your dataset is identified, print their name on the screen
			if (counk==6):
				print(name)
				#Take a picture to send in the email
				img_name = "image.jpg"
				cv2.imwrite(img_name, frame)
				print('Taking a picture of recognised .')
				#
				#Now send me an email to let me know who is at the door
				request = send_message(name)
				print ('Status Code: '+format(request.status_code)) #200 status code means email sent successfully
				print('Opening the Door')
				counk=0
				p.ChangeDutyCycle(4.5)
				sleep(0.1)
				p.ChangeDutyCycle(0)
				print('SERVO CONTROL')
				sleep(2)
				p.ChangeDutyCycle(12.5)
				sleep(0.1)
				p.ChangeDutyCycle(0)

		else:
			counk = counk-1
			counu +=1
			print("ammooo...")

			if(counu==6):
				img_name = "image.jpg"
				cv2.imwrite(img_name, frame)
				print('Taking a picture of unknown .')
				#Now send me an email to let me know who is at the door
				request = send_message(name)
				print('Status Code: ' + format(request.status_code))  # 200 status code means email sent successfully
				counu=0

			

			# Initialize Blynk
				blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)


				# Led control through V0 virtual pin
				@blynk.on("V0")
				def v0_write_handler(value):
					#    global led_switch
					if int(value[0]) != 0:
						p.ChangeDutyCycle(4.5)
						sleep(0.1)
						p.ChangeDutyCycle(0)
						print('SERVO LOW')
						sleep(2)
						p.ChangeDutyCycle(12.5)
						sleep(0.1)
						p.ChangeDutyCycle(0)

			# function to sync the data from virtual pins
				@blynk.on("connected")
				def blynk_connected():
					print("Raspberry Pi Connected to New Blynk")


				t_end = time.time() + 30 * 1
				while time.time() < t_end:
					blynk.run()

			


		# update the list of names
		names.append(name)

	# loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		# draw the predicted face name on the image - color is in BGR
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 225), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			.8, (0, 255, 255), 2)

	# display the image to our screen
	cv2.imshow("Facial Recognition is Running", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
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
vs.stop()
