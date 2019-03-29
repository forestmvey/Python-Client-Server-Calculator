import socket, sys

port = int(sys.argv[1])

# Create the socket object using DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
loop = True
s.bind( ("", port) )

def twoBitUnpackerFirst(x):
    return ((x & 240) >> 4)
def twoBitUnpackerSecond(x):
    return (x & 15)

# Servers stay open for client acceptance
while loop == True:

    # wait for a client to send a packet
    packet, addr = s.recvfrom(1024)
    

    operator = packet[0]
    numVals = packet[1]
    operand = 2
    
    
    result = 0

    # if bit 0 - add operands
    if operator & 1 == 1:
        for x in range(0,int((numVals + 1) / 2)):
            if x == int((numVals + 1)/2 - 1) and numVals % 2 != 0:
                result += int(twoBitUnpackerFirst(packet[operand]))
                operand += 1
            else:
                result += int((twoBitUnpackerFirst(packet[operand])) + int(twoBitUnpackerSecond(packet[operand])))
                operand += 1
        
        packet = bytearray(4)
        packet[0] = (result >> 24) & 255
        packet[1] = (result >> 16) & 255
        packet[2] = (result >> 8) & 255
        packet[3] = result & 255
        s.sendto(packet, addr)
        
    # if bit 1 - minus operands
    elif operator & 2 == 2:
        result = int(twoBitUnpackerFirst(packet[operand]))
        if len(packet) > 2:
            result -= int(twoBitUnpackerSecond(packet[operand]))
        
        operand += 1
        
        for x in range(0,int((numVals - 1) / 2)):
            if x == int((numVals - 1)/2 - 1) and numVals % 2 != 0:
                result -= int(twoBitUnpackerFirst(packet[operand]))
            else:
                result -= int(twoBitUnpackerFirst(packet[operand]))
                result -= int(twoBitUnpackerSecond(packet[operand]))
                operand += 1
        
        # if result is negative, sign the integer before placing in array
        if result < 0:
             result = result * -1
             result = result | 2**31

        packet = bytearray(4)
        packet[0] = (result >> 24) & 255
        packet[1] = (result >> 16) & 255
        packet[2] = (result >> 8) & 255
        packet[3] = result & 255

        s.sendto(packet, addr)
        
    # if bit 2 - multiply operands
    elif operator & 4 == 4:
        result = 1
        for x in range(0,int((numVals + 1) / 2)):
            if x == int((numVals + 1)/2 - 1) and numVals % 2 != 0:
                result *= int(twoBitUnpackerFirst(packet[operand]))
                operand += 1
            else:
                result *= int((twoBitUnpackerFirst(packet[operand])))
                result *= int((twoBitUnpackerSecond(packet[operand])))
                operand += 1

        packet = bytearray(4)
        packet[0] = (result >> 24) & 255
        packet[1] = (result >> 16) & 255
        packet[2] = (result >> 8) & 255
        packet[3] = result & 255
        s.sendto(packet, addr)
            

    

