from config import *

class Bulb:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.is_on = False

    def isOn(self):
        return self.is_on

    def turnOn(self):
        self.mqtt_client.publish(CMD_BEDROOM_BULB, BULB_OPEN)
        self.is_on = True
    
    def turnOff(self):
        self.mqtt_client.publish(CMD_BEDROOM_BULB, BULB_CLOSE)
        self.is_on = False

class LighSensor:
    def __init__(self):
        self.mqtt_client = mqtt_client
        self.status_changed = False
        self.dark = False

    def statusChanged(self):
        if self.status_changed:
            self.status_changed = False
            return True
        else:
            return False

    def update(self, topic, payload):
        if topic == SENSOR_BEDROOM_LIGHT and int(payload) < LIGHT_SENSOR_THRESHOLD and self.dark == False:
            self.dark = True
            self.statusChanged = True

        if topic == SENSOR_BEDROOM_LIGHT and int(payload) >= LIGHT_SENSOR_THRESHOLD and self.dark:
            self.dark = False
            self.statusChanged = True
    
    def isDark(self):
        return self.dark

class MotionSensor:
    def __init__(self):
        self.mqtt_client = mqtt_client
        self.status_changed = False
        self.persons_detected = 0

    def statusChanged(self):
        if self.status_changed:
            self.status_changed = False
            return True
        else:
            return False

    def update(self, topic, payload):
        if topic == SENSOR_BEDROOM_MOTION and payload == MOTION_INWARD:
            self.persons_detected += 1:
            self.statusChanged = True

        if topic == SENSOR_BEDROOM_MOTION and payload) == MOTION_OUTWARD:
            self.persons_detected += 1
            self.persons_detected = max(self.persons_detected, 0)
            self.statusChanged = True
    
    def personsDetected(self):
        return self.persons_detected

class Bedroom:
    def __init__(self, mqtt_client):
        self.bulb = Bulb(mqtt_client)
        self.light_sensor = LighSensor()
        self.motion_sensor = MotionSensor()

    def handle(self, topic, payload):
        self.light_sensor.update(topic, payload)
        self.motion_sensor.update(topic, payload)

        if self.light_sensor.statusChanged():
            if self.light_sensor.isDark() and self.motion_sensor.personsDetected() and not self.bulb.isOn(): self.bulb.turnOn()

        if self.motion_sensor.statusChanged():
            if self.motion_sensor.personsDetected() == 0 and bulb.isOn(): self.bulb.turnOff()
            if self.motion_sensor.personsDetected() and self.light_sensor.isDark() not self.bulb.isOn(): self.bulb.turnOn()
