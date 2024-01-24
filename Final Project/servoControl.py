import BlynkLib
import RPi.GPIO as GPIO
from BlynkTimer import BlynkTimer
from time import sleep 
import time
import BlynkLib

servo_pin= 26
GPIO.setmode(GPIO.BCM)  # We are using the BCM pin numbering
#Declaring Servo Pins as output pins
GPIO.setup(servo_pin, GPIO.OUT)

BLYNK_AUTH_TOKEN = "wr1D2Ws8I1mgy71ELKP_7lxFQncToT02"


GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
p = GPIO.PWM(servo_pin, 50)
p.start(0)

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
p.ChangeDutyCycle(12.5)
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

#timer=BlynkTimer.timer()

#function to sync the data from virtual pins
@blynk.on("connected")
def blynk_connected():
    print("Raspberry Pi Connected to New Blynk") 


while True:
        blynk.run()
