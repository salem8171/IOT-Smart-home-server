from config import *

class Fan:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.is_on = False

    def isOn(self):
        return self.is_on

    def turnOn(self):
        self.mqtt_client.publish(CMD_LIVINGROOM_FAN, FAN_OPEN)
        self.is_on = True
    
    def turnOff(self):
        self.mqtt_client.publish(CMD_LIVINGROOM_FAN, FAN_CLOSE)
        self.is_on = False

class TemperatureSensor:
    def __init__(self):
        self.mqtt_client = mqtt_client
        self.status_changed = False
        self.is_hot = False

    def statusChanged(self):
        if self.status_changed:
            self.status_changed = False
            return True
        else:
            return False

    def update(self, topic, payload):
        if topic == SENSOR_LIVINGROOM_TEMPERATURE and int(payload) >= TEMPERATURE_SENSOR_THRESHOLD and self.is_hot == False:
            self.is_hot = True
            self.statusChanged = True

        if topic == SENSOR_LIVINGROOM_TEMPERATURE and int(payload) < TEMPERATURE_SENSOR_THRESHOLD and self.is_hot:
            self.is_hot = False
            self.statusChanged = True
    def isHot(self):
        return self.is_hot

class Livingroom:
    def __init__(self, mqtt_client):
        self.fan = Fan(mqtt_client)
        self.temperature_sensor = TemperatureSensor()
    
    def handle(self, topic, payload):
        self.temperature_sensor.update(topic, payload)

        if self.temperature_sensor.statusChanged():
            if self.temperature_sensor.isHot() and not self.fan.isOn(): self.fan.turnOn()
            if not self.temperature_sensor.isHot() and self.fan.isOn(): self.fan.turnOff()