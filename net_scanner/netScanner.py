# !/usr/bin/env python3

import optparse
import scapy.all as scapy
import argparse

# optparse is the old module that is from python2.7
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="IP", help="IP address of local network to scan")
    (options, arguments) = parser.parse_args()
    if not options.IP:
        parser.error("[+] Please Specify correct IP address, use --help for more information")
    return options

# argparse is the module that is new from python 3 and the only difference is that it returns only options
def get_argumentsby_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="IP", help="IP address of local network to scan")
    options = parser.parse_args()
    if not options.IP:
        parser.error("[+] please specify the correct IP address, use --help for more information")
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_packet = broadcast/arp_request
    answeredList = scapy.srp(arp_request_packet, timeout=1, verbose=False)[0]
    client_list = []
    for element in answeredList:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def displayClients(clients):
    print("IP\t\t\tMAC Address\n----------------------------------------------")
    for client in clients:
        print(client["ip"] + "\t\t" + client["mac"])

option = get_argumentsby_argparse()
clients_list = scan(option.IP)
displayClients(clients_list)
