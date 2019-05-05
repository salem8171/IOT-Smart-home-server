import config
from mail_client import sendmail

class Window:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.is_open = False

    def isOpen(self):
        return self.is_open

    def open(self):
        self.mqtt_client.publish(config.CMD_KITCHEN_WINDOW, config.WINDOW_OPEN)
        self.is_open = True
    
    def close(self):
        self.mqtt_client.publish(config.CMD_KITCHEN_WINDOW, config.WINDOW_CLOSE)
        self.is_open = False

class GasSensor:
    def __init__(self):
        self.status_changed = False
        self.leak_detected = False

    def statusChanged(self):
        if self.status_changed:
            self.status_changed = False
            return True
        else:
            return False

    def update(self, topic, payload):
        if topic == config.SENSOR_KITCHEN_GAS and int(payload) >= config.GAS_SENSOR_THRESHOLD and self.leak_detected == False:
            self.leak_detected = True
            self.status_changed = True

        if topic == config.SENSOR_KITCHEN_GAS and int(payload) < config.GAS_SENSOR_THRESHOLD and self.leak_detected:
            self.leak_detected = False
            self.status_changed = True
    
    def isLeakDetected(self):
        return self.leak_detected

class Kitchen:
    def __init__(self, mqtt_client):
        self.window = Window(mqtt_client)
        self.gas_sensor = GasSensor()

    def handle(self, topic, payload):
        self.gas_sensor.update(topic, payload)

        if self.gas_sensor.statusChanged():
            if self.gas_sensor.isLeakDetected():
                sendmail("PANIC! GAS LEAK DETECTED")
                if not self.window.isOpen(): self.window.open()

        if topic == config.REQ_KITCHEN_WINDOW and payload == config.WINDOW_OPEN and not self.window.isOpen(): self.window.open()
        if topic == config.REQ_KITCHEN_WINDOW and payload == config.WINDOW_CLOSE and self.window.isOpen(): self.window.close()