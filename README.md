# Python-Client-Server-Calculator
A simple python client and server implementation of a calculator using 2 integers for each byte of data sent using DGRAM.

The client takes a server address, a port number, an operator (‘+’, ‘-’ or ‘*’) and up to 10 small integers on the command-line.
The integers must be between 0 and 15, inclusive. The server returns the result of the performed operation on all integers from
left to right.


command line args
arg 1 - ip
arg 2 - port
arg 3 - Operand
arg 4 >= operators
