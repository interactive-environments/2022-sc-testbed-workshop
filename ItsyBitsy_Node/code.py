############Imports used for regular things############
import board
from digitalio import DigitalInOut
import p9813

########Imports required for PBS communication#########
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
from adafruit_esp32spi import adafruit_esp32spi_socket as socket
from settings import settings
from SimpleOSC import SimpleOSCParser
from PBS_OSC import PBSOSC
from PBSNoise import PBSNoise
from PBS_mqtt import PBSMQTT
###########Setup required for regular things###########
# Chainable RGB
pin_clk = board.D13
pin_data = board.D10
num_leds = 1
leds = p9813.P9813(pin_clk, pin_data, num_leds)

button = DigitalInOut(board.D7)
pressed = False
##########Setup required for PBS communication#########
noise = PBSNoise()
parser = SimpleOSCParser()
spi = board.SPI()
esp32_cs = DigitalInOut(board.D9)
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D12)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, settings)
print("Connecting to Wifi")
wifi.connect()
print("IP Address", esp.pretty_ip(esp.ip_address))
socket.set_interface(esp)
shiftr = PBSMQTT(esp, settings, noise)
OSCCommunicator = PBSOSC(esp, socket, parser)
lightOn = True

def OSCMessage(topic, dataTypes, output):
    global lightOn
    global noise
#     print(topic)
#     print(dataTypes)
#     print(output)

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
# OSCCommunicator.sendMessage(parser.writeOSC("/reportNodeID", "sss", ["JustinTest", "2B6C4A", esp.pretty_ip(esp.ip_address)]))

while True:
    ##########Code required for PBS communication##########
    OSCCommunicator.loop(OSCMessage)
    shiftr.loop()
    curNoise = noise.generateNoise() # Generates a number

    #############Code using PBS communication##############
    leds.fill((0, int(255 * curNoise), 0)) # Using the noise to change the LED to green
    leds.write() # Write the color to the LED
    if button.value: # If the button is pressed
        if not pressed: # And this code hasnt already ran
            a = "/sendTouch" # sendTouch, aka send a touchpoint. Do not change this.
            b = "iiiiififf" # this is telling the server what types are being send, i = int, f = float. Also do not change this
            c = [-2686, -906, 2800, 80,   200,  0.5001, 1000,     1.0001,   0.5001] # These are the parameters, you can test these on the website
            #   [X    , Y   , Z   , core, size, speed,  lifespan, strength, fadeRatio]
            # You can test these numbers on the website to see the differences between these values.

            OSCCommunicator.sendMessage(parser.writeOSC(a, b, c)) # Send the message to the server
            pressed = True # Make sure the code is only ran once per button press
    else:
        pressed = False # Make sure the code is only ran once per button press


