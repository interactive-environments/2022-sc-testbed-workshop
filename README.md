# 2022-sc-testbed-workshop

In this repository contains code to connect to the LASG Test-Bed installed in the Science Centre of the TUDelft.

Skygen should respond to messages (OSC or MQTT) of the following format (JSON-formatted string):
OSC:  /skyParams {"nw":49,"ww":48,"tb":"2.70","it":"2.80","cn":"0.43"}
MQTT: /influences/sky {"nw":49,"ww":48,"tb":"2.70","it":"2.80","cn":"0.43"}

Touchpoint should respond to OSC messages of the following format:
typetag: iiiiififf
parameters: int x, int y, int z, int core, int size, float speed, int lifespan, float strength, float fadeRatio (f)
example: /touchPoint -715 1304 2800 670 670 0.2 50 0.9 0.7
