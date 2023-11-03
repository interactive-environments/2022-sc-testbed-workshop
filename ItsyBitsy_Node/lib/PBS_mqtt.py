# Write your code here :-)
from adafruit_esp32spi import adafruit_esp32spi_socket as socket
from adafruit_minimqtt import adafruit_minimqtt as miniMQTT
class PBSMQTT():
    def __init__(self, esp, settings, noise):
        self.settings = settings
        self.esp = esp
        self.noise = noise
        miniMQTT.set_socket(socket, self.esp)
        self.mqtt_client = miniMQTT.MQTT(
            broker=self.settings["broker"], port=1883, client_id = self.settings["clientid"]
        )

        self.mqtt_client.on_connect = self.connected
        self.mqtt_client.on_disconnect = self.disconnected
        self.mqtt_client.on_message = self.message

        print("Connecting to MQTT broker...")
        self.mqtt_client.connect()
        self.mqtt_client.publish("names", self.settings["displayname"] + "-" + settings["clientid"])

    def message(self, client, topic, message):
#         print(topic, message)
        if topic == "influences_2/sky":
            self.noise.setSkyParams([message])

    ### MQTT connection functions ###
    def connected(self, client, userdata, flags, rc):
        print("Connected to MQTT broker! Listening for topic changes on %s" % "influences_2/sky")
        client.subscribe("influences_2/sky")

    def disconnected(self, client, userdata, rc):
        print("Disconnected from MQTT Broker!")

    def loop(self):
        self.mqtt_client.loop(timeout=0.01)
