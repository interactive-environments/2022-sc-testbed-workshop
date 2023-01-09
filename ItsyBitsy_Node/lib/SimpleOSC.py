import struct
class SimpleOSCParser():
    def __init__(self):
        return

    def writeOSC(self, topic, dataTypes, data):
        output = topic.encode('utf-8') + b'\x00'
        if (4 - (len(output) % 4))%4 > 0:
            output += (b'\x00' * (4 - (len(output) % 4)))
        output += (","+dataTypes).encode('utf-8') + b'\x00'
        if (4 - (len(output) % 4))%4 > 0:
            output += (b'\x00' * (4 - (len(output) % 4)))
        for i in range (len(dataTypes)):
            if dataTypes[i] == "s":
                output += data[i].encode('utf-8') + b'\x00'
                output += (b'\x00' * (4 - (len(output) % 4)))
            elif dataTypes[i] == "i":
                output += data[i].to_bytes(4, 'big', signed=True)
                continue
            elif dataTypes[i] == "f":
                output += struct.pack(">f", data[i])
                continue
        return output

    def parseOSC(self, message: Bytes):
#         print(message)
        length = len(message)
        if length > 0:
            if length%4 == 0:
                curPos = 0
                topic = []
                dataTypes = []
                messages = []
                for i in range(length):
                    if message[i] != 0:
                        topic.append(message[i])
                    else:
                        curPos = i
                        break

                for i in range(curPos, length):
                    if message[i] != 0:
                        curPos = i
                        break;

                for i in range(curPos, length):
                    if message[i] != 0:
                        if message[i] != 44:
                            dataTypes.append(message[i])
                    else:
                        curPos = i
                        break
                changeTypeOnce = False
                typePos = 0
                skips = 0
                curMessage = []
                for i in range(curPos, length):
                    if skips > 0:
                        skips -= 1
                        continue
                    if typePos < len(dataTypes):
                        if dataTypes[typePos] == 115: # Strings
                            if message[i] != 0:
                                changeTypeOnce = True
                                curMessage.append(message[i])
                            else:
                                if changeTypeOnce:
                                    messages.append(bytearray(curMessage).decode())
                                    curMessage = []
                                    changeTypeOnce = False
                                    typePos += 1
                        elif dataTypes[typePos] == 105: #Integers
                            if i%4 == 0:
                                [x] = struct.unpack('>i', message[i:i+4])
                                messages.append(x)
                                skips = 3
                                typePos += 1
                        elif dataTypes[typePos] == 102: #Floats
                            if i%4 == 0:
                                [x] = struct.unpack('>f', message[i:i+4])
                                messages.append(x)
                                skips = 3
                                typePos += 1
                return (bytearray(topic).decode(), bytearray(dataTypes).decode(), messages)
            else:
                return "Length not divisible by 4"
        else:
            return ("", "", [])
