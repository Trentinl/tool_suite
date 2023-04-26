#!/usr/bin/env python3

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", help="The interface to change the MAC Address of.")
    parser.add_option("-m", "--mac", help="The new MAC Address. Ex 00:11:22:33:44:55")
    (options, argumets) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.mac:
        parser.error("[-] Please specify a MAC Address, use --help for more info.")
    return options


def change_mac(interface, mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    verify_mac = subprocess.check_output(["ifconfig", interface]).decode()
    verify_mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", verify_mac)

    if verify_mac_result:
        return verify_mac_result.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

change_mac(options.interface, options.mac)
print("[+] Changing MAC Address for " + options.interface + " to " + options.mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.mac:
    print("[+] MAC Address was successfully changed to " + current_mac)
else:
    print("[-] MAC Address was not changed.")
    



