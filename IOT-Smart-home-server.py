#!/usr/bin/python3
import paho.mqtt.client as mqtt
import smtplib
import kitchen
from config import *

dark = False
persons_in_bedroom = 0

def on_message(client, userdata, message):
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))

    # Kitchen
    if (topic == SENSOR_KITCHEN_GAS):
        if (int(payload) > GAS_SENSOR_THRESHOLD):
            client.publish(CMD_KITCHEN_WINDOW, WINDOW_OPEN)
            msg = "PANIC! GAS LEAK DETECTED"
            sendmail(msg)
        if (int(payload) < GAS_SENSOR_THRESHOLD): client.publish(CMD_KITCHEN_WINDOW, WINDOW_CLOSE)

    if (topic == REQ_KITCHEN_WINDOW):
        client.publish(CMD_KITCHEN_WINDOW, payload)

    # Bedroom
    if (topic == SENSOR_BEDROOM_LIGHT):
        dark = (int(payload) < LIGHT_SENSOR_THRESHOLD)
        if (dark and persons_in_bedroom > 0): client.publish(CMD_BEDROOM_BULB, BULB_OPEN)
        else: client.publish(CMD_BEDROOM_BULB, BULB_CLOSE)
    
    if (topic == SENSOR_BEDROOM_MOTION):
        if (payload == MOTION_INWARD): persons_in_bedroom += 1
        if (payload == MOTION_OUTWARD): persons_in_bedroom -= 1
        if (dark and persons_in_bedroom > 0): client.publish(CMD_BEDROOM_BULB, BULB_OPEN)
        else: client.publish(CMD_BEDROOM_BULB, BULB_CLOSE)

client = mqtt.Client()
def sendmail(msg):
    try:
        mail_server = smtplib.SMTP('smtp.gmail.com', 587)
        # mail_server.connect('smtp.gmail.com', 465)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.login("s28260962@gmail.com", "M$K28260962")
        mail_server.sendmail("s28260962@gmail.com", "yosr.benhamida@enis.tn", msg)
        mail_server.close()
    except:
        print("mail not send")

client.on_message = on_message
client.connect("localhost")
client.loop_start()

client.subscribe(SENSOR_KITCHEN_GAS)
client.subscribe(SENSOR_BEDROOM_MOTION)
client.subscribe(SENSOR_BEDROOM_LIGHT)
client.subscribe(SENSOR_LIVINGROOM_TEMPERATURE)

while True:
    pass
