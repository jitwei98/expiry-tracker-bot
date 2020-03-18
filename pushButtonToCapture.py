import RPi.GPIO as GPIO
import datetime
from time import sleep
from picamera import PiCamera
import requests

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
camera = PiCamera()
camera.resolution = (1900, 1080)
#camera.ISO = 1
#camera.shutter_speed = 2000
camera.framerate = 16.7
#date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
while True:
    date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    input_state_for_sign_in = GPIO.input(16)
    input_state_for_sign_out = GPIO.input(18)
    if input_state_for_sign_in == False:
        print("Sign in button was pushed!")
        #sleep(2)
        #camera = PiCamera()
        #camera.resolution = (2592, 1944)
        #camera.framerate = 15
        camera.start_preview(alpha=225)
        sleep(1)
        #camera.stop_preview()
        camera.capture('/home/pi/Documents/Hack For Good/SigningIn/' +'in' + '.jpg')
        camera.stop_preview()
    elif input_state_for_sign_out == False:
        print("Sign out button was pushed!")
        #sleep(2)
        #camera = PiCamera()
        #camera.resolution = (2592, 1944)
        #camera.framerate = 15
        camera.start_preview(alpha=225)
        sleep(1)
        #camera.stop_preview()
        camera.capture('/home/pi/Documents/Hack For Good/SigningOut/' + 'out' + '.jpg')
        camera.stop_preview()

