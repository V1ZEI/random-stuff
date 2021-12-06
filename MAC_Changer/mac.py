#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="Interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="NewMACAddress", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.Interface:
        parser.error("[+] PLease specify an interface, use --help fr more info ")
    elif not options.NewMACAddress:
        parser.error("[+] PLease specify a new MAC address, use --help fr more info ")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address, for the " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = str(subprocess.check_output(["ifconfig", interface]))
    mac_results = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_results:
        return mac_results.group(0)
    else:
        print(f"[-] Cannot read MAC address for {interface}")


option = get_arguments()
current_mac = str(get_current_mac(option.Interface))
print(f"[+] Current MAC address for {option.Interface} is {current_mac}")
change_mac(option.Interface, option.NewMACAddress)
current_mac = str(get_current_mac(option.Interface))

if current_mac == option.NewMACAddress:
    print(f"[+] MAC address for {option.Interface} have been changed to {option.NewMACAddress} successfully")
else:
    print(f"[-] MAC address did not get changed for {option.Interface}")
