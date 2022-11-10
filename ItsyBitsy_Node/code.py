import time
import board
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import adafruit_requests as requests
from settings import settings
from SimpleOSC import SimpleOSCParser
from PBS_OSC import PBSOSC
from PBSNoise import PBSNoise
noise = PBSNoise()

parser = SimpleOSCParser()

# PyPortal or similar; edit pins as needed
spi = board.SPI()
esp32_cs = DigitalInOut(board.D9)
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D12)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

print("Connecting to Wifi")
#esp.connect(settings)

print("IP Address", esp.pretty_ip(esp.ip_address))
#print("Server ping", esp.ping(HOST), "ms")
socket.set_interface(esp)


OSCCommunicator = PBSOSC(esp, socket, parser)

a = "test"
b = "s"
c = ["test"]


lightOn = True
def OSCMessage(topic, dataTypes, output):
    global lightOn
    global noise
    print(topic)
    print(dataTypes)
    print(output)
    OSCCommunicator.sendMessage(parser.writeOSC(topic, dataTypes, output))

    if topic == "/skyClock":
        noise.setSkyClock(output)

    if topic == "/skyParams":
        noise.setSkyParams(output)

    if topic == "/blinkFlag":
        if output[0] == 0:
            lightOn = False
        elif output[0] == 1:
            lightOn = True
        elif output[0] == -1:
            lightOn = not lightOn



noise.setSkyParams(['{"nw":"0", "ww":"0", "tb":"0", "it":"1.5", "cn":"0.89"}'])
noise.setSkyClock([2708775, 8673])
noise.setXY(33.8, -106.8)
while True:
#     OSCCommunicator.loop(OSCMessage)
#     OSCCommunicator.sendMessage(parser.writeOSC(a, b, c))
    print(noise.generateNoise())
    time.sleep(1)


