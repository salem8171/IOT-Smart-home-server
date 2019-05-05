#!/usr/bin/python3
import paho.mqtt.client as mqtt
import smtplib
from kitchen import Kitchen
from bedroom import Bedroom
from livingroom import Livingroom
import config

def on_message(client, userdata, message):
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))

    kitchen.handle(topic, payload)    
    bedroom.handle(topic, payload)
    livingroom.handle(topic, payload)


client = mqtt.Client()
client.on_message = on_message
client.connect("localhost")
client.loop_start()

client.subscribe(config.SENSOR_KITCHEN_GAS)
client.subscribe(config.SENSOR_BEDROOM_MOTION)
client.subscribe(config.SENSOR_BEDROOM_LIGHT)
client.subscribe(config.SENSOR_LIVINGROOM_TEMPERATURE)

client.subscribe(config.REQ_KITCHEN_WINDOW)
client.subscribe(config.REQ_BEDROOM_BULB)
client.subscribe(config.REQ_LIVINGROOM_FAN)

kitchen = Kitchen(client)
bedroom = Bedroom(client)
livingroom = Livingroom(client)

while True: pass
