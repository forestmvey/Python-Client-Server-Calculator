# Author Forest Vey
import socket, sys

# create the socket using DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# build the packet.
host = sys.argv[1]
port = int(sys.argv[2])
operator = sys.argv[3]
passedValues = int(len(sys.argv)) - 4
packet = bytearray(int((passedValues + 1)/2) + 2)


# function to fit 2 integers into one 8 bit byte
def twoBitPacker(a, b):
    return int(b) | (int(a) << 4)


# give number equivalent to represent operator to use
if operator == '+':
    operator = 1
elif operator == '-':
    operator = 2
elif operator == '*':
    operator = 4
else:
    print("please enter a valid operator + - *")

packet[0] = operator
packet[1] = passedValues
toPack = 2
x = 4

# add all values in command line to byte array
while x < passedValues + 4:
    if x == passedValues + 3:
        packet[toPack] = int(sys.argv[x]) << 4
        toPack += 1
        x += 1
    else:
        packet[toPack] = twoBitPacker(sys.argv[x],sys.argv[x+1])
        toPack += 1
        x += 2

# send the packet. 
s.sendto(packet, (host, port))

# receive the response
data = s.recv(4)

# unpack the byte array to a meaningful value.
#    each integer represented in 4 bits, first bit tells if positive/negative integer
value = int(data[0]) << 24 | int(data[1]) << 16 | int(data[2]) << 8 | int(data[3])

if value & 2**31 == 2**31:
    value = value ^ 2**31
    value *= -1
print(value)
