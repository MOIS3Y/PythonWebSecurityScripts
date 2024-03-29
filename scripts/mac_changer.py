#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import optparse
import re


def get_arguments():
    """ gets command line arguments entered by user """

    parser = optparse.OptionParser()
    parser.add_option(
        '-i',
        '--interface',
        dest='interface',
        help='Interface to change its MAC address')
    parser.add_option(
        '-m',
        '--mac',
        dest='new_mac',
        help='New MAC address')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error(
            '[-] Please specify an interface, use --help for more info')
    elif not options.new_mac:
        parser.error(
            '[-] Please specify a new MAC-addres, use --help for more info')
    return options


def get_current_mac(interface):
    """ gets current MAC-addres """

    ifconfig_resuit = subprocess.check_output(
        ['ifconfig', interface]).decode("utf-8")
    mac_addres_search_result = re.search(
        r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_resuit)

    if mac_addres_search_result:
        return mac_addres_search_result.group(0)
    else:
        print('[-] Could not read MAC address.')
        return 'The interface does not have a MAC address'


def change_mac(interface, new_mac):
    """ changes the MAC address to the user entered """

    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])
    print('[+] Changing MAC address for ' + interface + ' to ' + new_mac)


if __name__ == "__main__":
    options = get_arguments()
    current_mac = get_current_mac(options.interface)
    print('[+] Current MAC = ' + str(current_mac))
    change_mac(options.interface, options.new_mac)
    current_mac = get_current_mac(options.interface)
    if current_mac == options.new_mac:
        print('[+] MAC address was successfully changed to ' + current_mac)
    else:
        print('[-] MAC address did not get changet')


# !  bad option (contains vulnerabilities)
# subprocess.call('ifconfig ' + interface + ' down', shell=True)
# subprocess.call('ifconfig ' + interface + ' hw ether ' + new_mac, shell=True)
# subprocess.call('ifconfig ' + interface + ' up', shell=True)

# * good option
# subprocess.call(['ifconfig', interface, 'down'])
# subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
# subprocess.call(['ifconfig', interface, 'up'])
