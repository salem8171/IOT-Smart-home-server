import config

class Fan:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.is_on = False

    def isOn(self):
        return self.is_on

    def turnOn(self):
        self.mqtt_client.publish(config.CMD_LIVINGROOM_FAN, config.FAN_ON)
        self.is_on = True
    
    def turnOff(self):
        self.mqtt_client.publish(config.CMD_LIVINGROOM_FAN, config.FAN_OFF)
        self.is_on = False

class TemperatureSensor:
    def __init__(self):
        self.status_changed = False
        self.is_hot = False

    def statusChanged(self):
        if self.status_changed:
            self.status_changed = False
            return True
        else:
            return False

    def update(self, topic, payload):
        if topic == config.SENSOR_LIVINGROOM_TEMPERATURE and int(payload) >= config.TEMPERATURE_SENSOR_THRESHOLD and self.is_hot == False:
            self.is_hot = True
            self.status_changed = True

        if topic == config.SENSOR_LIVINGROOM_TEMPERATURE and int(payload) < config.TEMPERATURE_SENSOR_THRESHOLD and self.is_hot:
            self.is_hot = False
            self.status_changed = True
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

        if topic == config.REQ_LIVINGROOM_FAN and payload == config.FAN_ON and not self.fan.isOn(): self.fan.turnOn()
        if topic == config.REQ_LIVINGROOM_FAN and payload == config.FAN_OFF and self.fan.isOn(): self.fan.turnOff()