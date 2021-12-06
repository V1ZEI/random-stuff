Goal is to inject some evil code in the packets that we captured in the network

First we use netfilterqueue to capture the packets
Since these captured packets are cannot be modified then we convert it into scapy packet to modify the data inside the packet

to convert the packet into scapy packet, we use scapy.IP() method to do it

since the data of the request is sent inside the load field in the Raw layer of the packet 
we use if condition to check whether the packet contains the Raw layer or not

If we proceed without checking for the Raw layer in the packet, then for the packets for which the Raw layer is not present then the program crashes and causes error

In the packet information, if we print the packet data by using the scapy show() method,
we can see that the request packets are the ones with dport value in TCP layer with http,
while hte response packets are the ones with sport value in the TCP layer with http

Since all the data inside the load field encrypted in the response packets, we cannot be able to read and write the data inside the packet

This happens because in the request packet, by default there is a field called "Accept-Encoding: " with some values
These values are type of encoding that the system can be able to decode the encoded message or data

If there is nothing like the field "Accept Encoding: ", then the server responds with the plane text as the request packet says that it cannot understand the encoding

So we try to replace this Accept Encoding : <blah> <blah> part in the packet with empty string or just delete this part from the packet

Now we can be able to read the load field in the packet

Now in the response packet we can inject our code, like in the above python script we just added alert message using javascript language


Now if you think you are good to go then you are wrong,

This algorithm does not work with all websites 
Reason:
  so each response packet comes with certain parameters like http response status, packet length, packet size, encoding type etc...
  one of these parameters is Content-Length
  This is sent from the server saying that, this is the length of the packet data that is sent to you, if you are loading more that this the packet is modified in the fly and dont load the packet after this length

Since we are adding our extra code in the packet, content length may vary and if the value is more than the value sent by server then the browser stops loading after the loaded content length reaches the value sent by server

So for this not to happen we have to change this field value too before sending the resposne to the user

Once again we use regex expressions to get the field value and change the value

and we calculate the length of our injected code and add it to the content length mentioned in the packet and then replace it

Drawback of this process is that we are trying to inject code in html page or javascript page, but what if the server resopnds with just an image?
In that case there will be no body tag and no code injection but there will be change in content length that is provided by server hence this leads to bad request

So for this not to happen we also have to check for the content-type in the reponse, this value should be text/html

Now we are good to go with code injection script we built so far
