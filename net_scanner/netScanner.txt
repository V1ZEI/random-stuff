the module thats gonna use to gather the information about the system and so on
is "scapy.all"

Important Point about "scapy" module:
this is actually intended to use for linux distributions and for windows distributions, the download process and the usage is different that of the linux distributions
check out more about it here -> pypi.org/python/

created a new python file named netScanner.py file 
imported the module scapy.all as scapy in that program and for reference in this text also scapy means scapy.all
like import scapy.all as scapy

scapy.arping(<ipaddress>) -> this literally does the job for us
this sends the IP addresses of the subnet you are in and asks each connected system to reply with their mac address

and we are going to use this scapy module to create our own arping function


CONCEPT:
behind the scenes what happens is,,
this arping sends a broadcast message saying that if you have this IP address please respond
and this arping sends the same message for all different subnets of IP addresses
example: consider your subnet is 10.2.0.45
now you are in the sebnet of IP's 10.2.0
and you are eager to know what different types of systems and their IP and MAC addresses in your subnet
then this arping sends the request message asking for 10.2.0.1 and
then it asks for 10.2.0.2, again for 10.2.0.3 and so on till max of 10.2.0.254

if you mention only one IP address then it does the process for just that particular IP 
you can mention multiple IP address in this case
since we are lazy to write all 254 IP subnets we pass the argument as "10.2.0.1/24"
this means that scan through the subnet of 10.2.0 all the way from 10.2.0.1 to 10.2.0.255
-->(i dont know the reason why subnet 255 is ignored in teaching by zaid,,, need to learn about it)<--

one more thing is that, if we use arping() inbuilt function this does the behind the scenes job for us
but if we are creating a new function that job is to do the same as the arping()
then we need to careful about the broadcast mac address

first the request message is sent to the broadcast system or maybe router(lets say by the host system), then that broadcast system broadcasts the message to all the users in that subnet,
and after it gets the reply then it send the reply to the main or the host system


Working Mechanism or Algorithm:
we use ARP() function to generate the message to request for the information.
this ARP() function is inbuilt in scapy module in python

ls() function in scapy:
we have to pass the arguments right,, how do we do that???
we use ls() function to listout all the possible parameters and arguments and their breif discussion about them

syntax is like scapy.ls(scapy.ARP())
this lists out all the paramerters or arguments that can be given to the ARP() function

if we do this for ARP() function we get psdt as the variable that takes IP address as the parameter that passes value into the function

we need output right for the program we are executing,,,
so we add the print statement as follow
print(<var>.summary())
<var> is the variable created and the summary is the function that summaries the whole object and then returns the text that is needed

for data to be sent to the computers, we need to make sure that the request message is sent to the broadcast mac address
coz
data in the network is sent using the mac address not ip address
this mac address is physical and unique that is engraved in each system.

this means that we need to create a ethernet frame and append the arp request message to it

creating an ethernet frame:
we use scapy.Ether()
and to find the different parameters that are used in this function use the ls() function in scapy
scapy.ls(scapy.Ether()) 
and the destination MAC address parameter is dst.

and now the destination mac address is the one that is virtually present and also make sure that this is the 
broadcast mac address

generally in this course we use ff:ff:ff:ff:ff:ff

ok good now we have both the ipaddress and the mac address that are needed for this task

and we need to attach these two so that the information recieved by the broadcast mac system is sent to the request system

we do that in scapy by using scapy.Ether()/scapy.ARP() -->this is important gonna use is exact as it is

this syntax is used to create overall packet to send to all other systems

we pass that as a variable that also has the summary() function to print all the data (of course we have to use that print syntax)
and also for more detailed information about that packet we can use the show() function in scapy

<var>.show()

like (scapy.Ether(<mac>)/scapy.ARP(<IP>)).show()

one more thing is that we can use the show() function for all the methods that we are using till now
and we can clearly say that the final packet has the information of both the ethernet frame and the IP packet 

now its time to send the packet over the internet and recieve response

and we do that by using the scapy module's "srp()" function
the syntax for it goes like this
scapy.srp(<var that contains the details of the ip and mac address both>)

actually scapy has a custom sr() function to do this job for sending the data over the internet
but we use the srp() function coz this allows us to send data with the custom ether part in that packet
https://scapy.readthedocs.io/en/latest/usage.html this is the link to scapy module functions usage

now this srp() function returns the two peices of data, this normally contains answered and unanswered data that is recieved respectively
this means to say that in the recieved packets we get answered first and then unanswered information in the form of lists
and we then capture the data into two variables(of course we name them accordingly)

and we are gonna add one more parameter to that function called timeout ...
what is the role of this timeout parameter,
after sending the packet to the particular IP address then the srp() function waits until it recieves the information from the other system
and if the other system is not responding then the program never stops and runs till it gets the signal(in this case information) from the other end

and with the help of this timeout parameter we can restrict the time spent on each IP address
this means that after particular time that is spent on a IP address after not recieveing any information this program just passes on to another IP address

this eventually helps the program to separate the captured information as answered and unanswered fast and efficiently
this timeout is given in seconds 

now lets print the captured result by using the summary() function
and the output comes in like 
<query packet>  ==> <answer packet>
this query packet information contains the destination IP address followed by the host IP address( that is asking for the information about the first IP address)
and the answer packet contains mac address of the responeded system along with their IP address

what if we print the unanswered packets??
the same thing as of printing the answered packet happens, but this time we dont get any response from the other side of the conversation
and that just displays the unanswered IP addresses.

Question::
	why the self system not responding to the recieved packet from the broadcast mac?????????????

CAREFUL INSTRUCTION:
this program works only if we append the ethernet frame with the IP address not reverse


now lets try t print the answered section of the recieved response
this response is also a list which contains the sent packet and recieved packet
not the information that we needed is that with the response that contains mac and IP address

if we use show() function on that recieved answered packets then this will show the more detailed information about each IP address and MAC address like source and destination etc..

the parameter that we are intrested in are psrc for getting the IP address and hwsrc for the MAC address
so we get that information be the line of code answeredList[1].psrc for obtaining just IP address and 
answeredList[1].hwsrc for obtaining MAC address (the name answeredList is a variable and you can name it as you want)

one of the most annoying thing after printing the result is that begin emmission and sending packets line that is actually printed by the srp() function itself
we can undo that by setting the false value to the parameter verbose in the srp() function and send it as a parameter

so lets see the final code

--------------------------(start of code)------------------------
import scapy.all as scapy
def scan(ip):
	arp_request=scapy.ARP(pdst=ip)
	broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_request_packet=broadcast/arp_request
	answeredList=srp(arp_request_packet, verbose=False, timeout=1)[0]
	#unansweredList=srp(arp_request_packet, verbose=False, timeout=1)[1]
	#this commented line contains the information about the unanswered packets and normally there is no use of it and if you are intrested you can do research about it
	print("IP\t\t\tMAC Address\n----------------------------------------")
	for element in answeredList:
		print(element[1].psrc + "\t\t" + element[1].hwsrc)

scan(<the ip address you need to scan>)
# generally it will be scan("10.0.2.1/24")

------------------------------------------(end of code)-------------

we can add some more features like the amount of time taken to do all the scanning and the different fucntion just to print the clients and more

most important funcions that we use are the
	summary()
	show()
	ARP()
	Ether()
	ls()
and more important thing is that syntax is scapy.<functionName>

better thing to do is that to create separate functions for each different work done by each functions.

optparse is the module that returns both options and arguments which is compatable with all versions of python
the new module introduced from python3 is that argparse, this retuns only options and which is cool...
