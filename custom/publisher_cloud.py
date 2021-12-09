import paho.mqtt.client as mqtt
from .config import CLOUD_OPTION

class Publisher_cloud:

    def __init__(self):
        self._set_client()

    def _set_client(self):
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = self._on_connect
        self.mqttc.on_disconnect = self._on_disconnect
        self.mqttc.on_publish = self._on_publish

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Publisher connected")
        else:
            print("Bad connection Returned code=", rc)

    def _on_disconnect(self, client, userdata, flags, rc=0):
        print(str(rc))

    def _on_publish(self, client, userdata, mid):
        #print("Publish success, callback mid= ", mid)
        test = 'good'

    def start(self):
        self.mqttc.connect(CLOUD_OPTION['broker_address'], CLOUD_OPTION['broker_port'])
        self.mqttc.loop_start()

    def stop(self):
        self.mqttc.loop_stop()
        self.mqttc.disconnect()

    def publish(self, topic, data):
        self.mqttc.publish(topic, data, 1)
