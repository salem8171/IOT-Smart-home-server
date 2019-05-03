#!/usr/bin/python3
import paho.mqtt.client as mqtt
import smtplib

SENSOR_KITCHEN_GAS = "sensor/kitchen/gas"
SENSOR_BEDROOM_MOTION = "sensor/bedroom/motion"
SENSOR_BEDROOM_LIGHT = "sensor/bedroom/light"
SENSOR_LIVINGROOM_TEMPERATURE = "sensor/livingroom/temperature"

CMD_KITCHEN_WINDOW = "cmd/kitchen/window"
CMD_BEDROOM_BULB = "cmd/bedroom/bulb"
CMD_LIVINGROOM_FAN = "cmd/living/room"

WINDOW_OPEN = "open"
WINDOW_CLOSE = "close"

BULB_OPEN = "open"
BULB_CLOSE = "close"

FAN_OPEN = "open"
FAN_CLOSE = "close"

GAS_SENSOR_THRESHOLD = 100

def on_message(client, userdata, message):
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))

    if (topic == SENSOR_KITCHEN_GAS):
        if (int(payload) > GAS_SENSOR_THRESHOLD):
            client.publish(CMD_KITCHEN_WINDOW, WINDOW_OPEN)
            msg = "PANIC! GAS LEAK DETECTED"
            sendmail(msg)
        if (int(payload) < GAS_SENSOR_THRESHOLD): client.publish(CMD_KITCHEN_WINDOW, WINDOW_CLOSE)


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
