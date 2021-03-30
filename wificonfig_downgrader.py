import argparse
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET


def parse_xml_tree(xml_path):
    print("Parsing xml from {} with tree".format(xml_path))
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for element in root:
        print(element)

def parse_xml(xml_path):
    print("Parsing xml from {} with loop/lines".format(xml_path))

    return_list = []

    # Temp vars
    ssid = ""
    config_key = ""
    psk = ""
    key_mgmt = ""

    with open(xml_path) as f:
        for line in f.readlines():
            line = line.strip()
            #print(line)

            parsed_dict = {}

            if line.endswith("<WifiConfiguration>"):
                print("*" * 80)
            elif line.startswith("<string name=\"ConfigKey\">"):
                config_key = line.replace("<string name=\"ConfigKey\">", "")
                config_key = config_key.replace("</string>", "")
                config_key = config_key.replace("&quot;", ",")

                key_mgmt = config_key.split(",")[2]

                print("Config key obtained: {}".format(config_key))
                print("key_mgmt obtained: {}".format(key_mgmt))
            elif line.startswith("<string name=\"SSID\">"):
                ssid = line.replace("<string name=\"SSID\">", "")
                ssid = ssid.replace("</string>", "")
                ssid = ssid.replace("&quot;", "")

                print("SSID obtained: {}".format(ssid))
            elif line.startswith("<string name=\"PreSharedKey\">"):
                psk= line.replace("<string name=\"PreSharedKey\">", "")
                psk = psk.replace("</string>", "")
                psk = psk.replace("&quot;", "")

                print("PSK obtained: {}".format(psk))
            elif line.endswith("<null name=\"PreSharedKey\" />"):
                psk = ""
                print("No PSK for this network")
            elif line.endswith("</WifiConfiguration>"):
                parsed_dict = {"ssid": ssid, "config_key": config_key, "psk": psk, "key_mgmt": key_mgmt}
                print("Attaching dict to list: {}".format(parsed_dict))
                return_list.append(parsed_dict)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='wificonfig_downgrader',
                                     usage='%(prog)s [options] inpath',
                                     description='Convert WifiConfigStore.xml to wpa_supplicant.conf')
    parser.add_argument('inpath',
                        metavar='inpath',
                        type=str,
                        help='File path to be converted')
    parser.add_argument('-o',
                        '--outpath',
                        metavar='outpath',
                        type=str,
                        default=os.getcwd(),
                        help='Dir path to write file. Defaults to current working directory')

    # Start of script
    args = parser.parse_args()

    input_path = args.inpath
    output_path = args.outpath

    print("Processing input file at {}".format(input_path))
    if not os.path.exists(input_path):
        print('The file in the path specified does not exist')
        sys.exit()

    # Parse xml into list of dicts
    network_list = parse_xml(input_path)