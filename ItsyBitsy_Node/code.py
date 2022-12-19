import time
import board
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_requests as requests
from settings import settings
from SimpleOSC import SimpleOSCParser
from PBS_OSC import PBSOSC
from PBSNoise import PBSNoise
from PBS_mqtt import PBSMQTT
import p9813

noise = PBSNoise()

parser = SimpleOSCParser()

# Chainable RGB
pin_clk = board.D13
pin_data = board.D10
num_leds = 1
leds = p9813.P9813(pin_clk, pin_data, num_leds)

# PyPortal or similar; edit pins as needed
spi = board.SPI()
esp32_cs = DigitalInOut(board.D9)
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D12)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, settings)
print("Connecting to Wifi")
wifi.connect()

print("IP Address", esp.pretty_ip(esp.ip_address))
#
socket.set_interface(esp)

button = DigitalInOut(board.D7)
# shiftr = PBSMQTT(esp, settings)
OSCCommunicator = PBSOSC(esp, socket, parser)

a = "/touchPoint"
b = "iiiiififf"
c = [-2686, -906, 2800, 80, 200, 0.5001, 1000, 1.0001, 0.5001]
# This is the hardcoded touchpoint message



lightOn = True
def OSCMessage(topic, dataTypes, output):
    global lightOn
    global noise
    print(topic)
    print(dataTypes)
    print(output)

    if topic == "/skyClock":
        noise.setSkyClock(output)

    if topic == "/skyClock2":
        noise.setSkyClock2(output)

    if topic == "/skyParams":
        noise.setSkyParams(output)

    if topic == "/blinkFlag":
        if output[0] == 0:
            lightOn = False
        elif output[0] == 1:
            lightOn = True
        elif output[0] == -1:
            lightOn = not lightOn



noise.setSkyParams(['{"nw":49,"ww":48,"tb":"2.70","it":"2.80","cn":"0.43"}']) # Add some standard values so it doesnt crash
noise.setSkyClock2([84729]) # Add some standard values so it doesnt crash
noise.setXY(-468, 250)
pressed = False
while True:
    OSCCommunicator.loop(OSCMessage)
    curNoise = noise.generateNoise()
    if curNoise > 0:
        leds.fill((0, int(255 * curNoise), 0))
        leds.write()
    else:
        leds.fill((0, 0, 0))
        leds.write()
    if button.value:
        if not pressed:
            OSCCommunicator.sendMessage(parser.writeOSC(a, b, c))
            pressed = True
    else:
        pressed = False


