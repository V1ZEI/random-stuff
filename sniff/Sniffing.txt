all right we are now the man in the middle who can actually see the information that is sent from our victim to router
but yet we didnt how how to see the information in the packets sent

so we do that by using the sniff function in the scapy module
the parameters that are needed are interface through which the packets are flowing and the call back function that needs to be executed after calling this sniff function
so the parameters are "iface" which is interface, "prn" which is the call back function
now this call back function takes one argument that is the packet that is flowing through this interface

just to make sure everything is good and well, just print the packet that contains the information
we get gibrrish, coz it contains all the information in some other format, we just need to separate the useful and non useful information in that packet

along with this the sniff function stores all the information that is inside the packet in our systems memory
to reduce this burden we can directly print out the information in the terminal there itself while sniffing
along with that we can filter the information that is exactly we needed by using the filter parameter in the sniff function
for this we use the store parameter in the sniff function, which we set it to False

and finally to grab the information in that packet we use the third party python tool called scapy_http

install this scapy_http module by the command "pip install scapy_http"
and import this by the line of code "from scapy_http import http"

here we precisely are importing the http related modules in the whole scapy_http module
coz we are looking the information, which is passing through the interfaces and the internet accurately
so this means that every request and the response packet that the user asks or gets contains the http request
and we can use that tool to see the information inside this packet

Then the first target for us it to check for the http request in the packet received, since we are looking for the information in the internet,
if that particular packet doesnot contains any http request then we can ignore the pakect, coz we are actually checking for the request and response packects information for now(at this task)

to check for a particular layer in that packects, we use the haslayer method on that packet
syntax goes like this
<packetVariable>.haslayer(<theLayerYouNeedToCheckInThatPacket>)
if you need to check for the http request layer then the syntax will be(considering that the packetVariable is named as packet)
packet.haslayer(http.HTTPRequest)

generally the login credentials are sent through the Raw layer in the http request in a packet
so we can print that information in a packet by checking for the presence of Raw Layer and printing the information in it
the url that contains the login credentials is under the load object

if packet.haslayer(http.HTTPRequest):
  if packet.haslayer(scapy.Raw):
    print(packect[scapy.Raw].load)

cool stuff right, getting the login credentials
but to what site these login credentials are applied???

we can get the urls visited by the victim too....

these urls are under the layer HTTPRequest and is decomposed into the Host site and Path in the host site
example:
  Host: udemy.com
  Path : /topic/django

the url victim visited is udemy.com/topics/django
now you get the idea of this path and parent site values in this packet

to get the full url he/she visited we use the string concatination method
so the full url visited will be

urlVisited = packet[http.HTTPRequest].Host + packect[http.HTTPRequest].Path
and as usual we can print these things in the terminal by the print function
