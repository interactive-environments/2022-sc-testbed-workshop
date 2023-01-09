import json
import time
from simplersimplexnoise import Simplex3D
class PBSNoise:

    def __init__(self):
        self.updateTime = 0
        self.skyClock = 0
        self.skyParams = {'cn': '0', 'nw': '0', 'it': '0', 'tb': '0', 'ww': '0'}
        self.noise = Simplex3D()
        self.x = 0
        self.y = 0

        return
    def setSkyClock(self, clockTime):
        self.updateTime = int(time.monotonic() * 1000)
        self.skyClock = clockTime[0] + clockTime[1]/10000

    def setSkyClock2(self, clockTime):
        self.updateTime = int(time.monotonic() * 1000)
        self.skyClock = clockTime[0]/10000

    def setSkyParams(self, params):
        jsonObj = json.loads(params[0])
        self.skyParams = jsonObj

    def setXY(self, x, y):
        self.x = x
        self.y = y

    def mapRange(self, v, l1, h1, l2, h2):
        return ( l2 + (h2 - l2) * (v - l1) / (h1 - l1) );

    def generateNoise(self):
        skytime = self.skyClock + (int(time.monotonic() * 1000) - self.updateTime)/10000
        a = self.x/20 -  float(self.skyParams["ww"])  * skytime   / self.mapRange(float(self.skyParams["it"])+90., 0., 100., 1000., 10.)
        b = self.y/20 +  float(self.skyParams["nw"])  * skytime   / self.mapRange(float(self.skyParams["it"])+90., 0., 100., 1000., 10.)
        c = (0 + float(self.skyParams["tb"]) * skytime )
        value = self.noise.generateNoise(a, b, c)
        v = min(1.0, 2.5* abs(value * float(self.skyParams["cn"])))
        return max(0, v)
