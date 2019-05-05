import config

class Bulb:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.is_on = False

    def isOn(self):
        return self.is_on

    def turnOn(self):
        self.mqtt_client.publish(config.CMD_BEDROOM_BULB, config.BULB_ON)
        self.is_on = True
    
    def turnOff(self):
        self.mqtt_client.publish(config.CMD_BEDROOM_BULB, config.BULB_OFF)
        self.is_on = False

class LighSensor:
    def __init__(self):
        self.status_changed = False
        self.dark = False

    def statusChanged(self):
        if self.status_changed:
            self.status_changed = False
            return True
        else:
            return False

    def update(self, topic, payload):
        if topic == config.SENSOR_BEDROOM_LIGHT and int(payload) < config.LIGHT_SENSOR_THRESHOLD and self.dark == False:
            self.dark = True
            self.status_changed = True

        if topic == config.SENSOR_BEDROOM_LIGHT and int(payload) >= config.LIGHT_SENSOR_THRESHOLD and self.dark:
            self.dark = False
            self.status_changed = True
    
    def isDark(self):
        return self.dark

class MotionSensor:
    def __init__(self):
        self.status_changed = False
        self.persons_detected = 0

    def statusChanged(self):
        if self.status_changed:
            self.status_changed = False
            return True
        else:
            return False

    def update(self, topic, payload):
        if topic == config.SENSOR_BEDROOM_MOTION and payload == config.MOTION_INWARD:
            self.persons_detected += 1
            self.status_changed = True

        if topic == config.SENSOR_BEDROOM_MOTION and payload == config.MOTION_OUTWARD:
            self.persons_detected += 1
            self.persons_detected = max(self.persons_detected, 0)
            self.status_changed = True
    
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
            if self.motion_sensor.personsDetected() == 0 and self.bulb.isOn(): self.bulb.turnOff()
            if self.motion_sensor.personsDetected() and self.light_sensor.isDark() and not self.bulb.isOn(): self.bulb.turnOn()

        if topic == config.REQ_BEDROOM_BULB and payload == config.BULB_ON and not self.bulb.isOn(): self.bulb.turnOn()
        if topic == config.REQ_BEDROOM_BULB and payload == config.BULB_OFF and self.bulb.isOn(): self.bulb.turnOff()
