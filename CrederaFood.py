#!/usr/bin/env python

from slackclient import SlackClient
from signal import pause
from time import sleep
from gpiozero import Buzzer
from picamera import PiCamera

buzzer = Buzzer(17, active_high=False)
camera = PiCamera()

# Set camera parameters
camera.rotation = 270
camera.sensor_mode = 2
imgoutputpath = '/home/pi/Desktop/FoodApp/imgcapture/img.jpg'

# Set slack parameters 
slack_token = 'insert_slack_api_token'
sc = SlackClient(slack_token)
slack_channel = 'insert_slack_channel_name'

## <!channel> is interpreted as @channel by slack, <!here> can also be used
slack_message = "<!channel> There is food in the large kitchen!"

# Capture image
def capture_image ():
    sleep (5)
    camera.start_preview()
    buzzer.beep(on_time=.10, off_time=.50, n=3, background=False)
    buzzer.beep(on_time=.25, off_time=.75, n=1, background=False)
    sleep(1)
    camera.capture(imgoutputpath)
    camera.stop_preview()
    print ("Imaged Captured!")
    sleep (3)

# Post message and image to slack
def post_to_slack ():
    print ("Posting to Slack...")
    print ("...posting message...")
    sc.api_call(
        "chat.postMessage",
        channel= slack_channel,
        text= slack_message
    )
    print ("...message posted...")
    print ("...posting image...")
    sc.api_call(
        "files.upload",
        filename='ifyoupostittheywillcome.png',
        channels= slack_channel,
        file = ( imgoutputpath , open(imgoutputpath, 'rb'))
    )
    print ("...image posted...")
    print ("...done")
    
def capture_and_post():
    print ("Button Pressed!")
    capture_image()
    post_to_slack()
    buzzer.beep(on_time=.10, off_time=.5, n=3, background=False)
    print ("Done!")
    print ("If you post it, they will come")

capture_and_post() 

