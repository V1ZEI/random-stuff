'''
Logic is that:-
  Hacker sends packets to our system saying that this is the ip of the router with the mac address specified in the packet
  Now since the packet contains the source ip and mac address from which the packet came from
  We can cross verify our packets source mac information with our mac address finder algorithm aganist the hacker system

  If these mac address are not matched then our system is under attack

  Attacker is actually pretending to be router by giving his IP and router mac address in the packets sent
    we take this mac address as spoof_mac and compare it with the original mac address of the IP that is sent in the packet
    If these two are not same then we are under attack as attacker is just pretending to be router
'''


#!usr/bin/env python
import sys
import pyttsx3
import argparse
import scapy.all as scapy

engine = pyttsx3.init()

class Backup:
  def get_interface():
    return str(input("Enter the network interface you want listen for changes: "))

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="Interface", help="Network interface you want to listen for changes")
    options = parser.parse_args()
    if not options.Interface:
      options.Interface = Backup.get_interface()
    return options.Interface

def get_mac(ip):
  arp_request = scapy.ARP(pdst=ip)
  broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
  arp_request_packet = broadcast/arp_request 
  answered_list = scapy.srp(arp_request_packet, timeout=1, verbose=False)[0]
  return answered_list[0][1].hwsrc

def PacketsInfo(interface):
  scapy.sniff(iface=interface, store=False, prn=detect_arp_spoof)

def detect_arp_spoof(packet):
  if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
    try:
      actual_mac = get_mac(packet[scapy.ARP].psrc)
      spoof_mac = packet[scapy.ARP].hwsrc
      if actual_mac != spoof_mac:
        print("[+] Under MITM attack")
        engine.say("You are under attack")
        engine.runAndWait()
        
    except IndexError as error:
      pass

interface = get_arguments()
try:
  PacketsInfo(interface)
  print("[+] Startin ARP spoof detector program...")
except KeyboardInterrupt as error:
  print("\r[-] Detected keyboard interruption, exiting the program...")
except Exception as error:
  print("\r[-] Detected error...\n")
  print(error)
  print("\n[-] Exiting the program...")
  sys.exit()