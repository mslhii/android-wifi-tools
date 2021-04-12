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
    count = 0

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
                if key_mgmt == "WPA_PSK":
                    key_mgmt = key_mgmt.replace("_", "-")

            elif line.startswith("<string name=\"SSID\">"):
                ssid = line.replace("<string name=\"SSID\">", "")
                ssid = ssid.replace("</string>", "")
                ssid = ssid.replace("&quot;", "")

            elif line.startswith("<string name=\"PreSharedKey\">"):
                psk= line.replace("<string name=\"PreSharedKey\">", "")
                psk = psk.replace("</string>", "")
                psk = psk.replace("&quot;", "")

            elif line.endswith("<null name=\"PreSharedKey\" />"):
                psk = ""
            elif line.endswith("</WifiConfiguration>"):
                priority = count + 1
                parsed_dict = {"ssid": ssid, "config_key": config_key, "psk": psk, "key_mgmt": key_mgmt, "priority": priority}
                print("Attaching dict to list: {}".format(parsed_dict))
                return_list.append(parsed_dict)
                count += 1

    print("Parsed {} networks".format(count))
    return return_list

def write_conf_file(input_list, file_outpath):
    print("Generate wpa_supplicant.conf file with input list of dicts to {}".format(file_outpath))

    count = 0

    f = open(file_outpath, "w+")
    f.write("ctrl_interface=eth0\n")
    f.write("update_config=1\n")
    f.write("\n")

    for network_item in input_list:
        f.write("network={\n")
        f.write("\tssid=\"{}\"\n".format(network_item["ssid"]))

        if network_item["key_mgmt"] != "NONE" or len(network_item["psk"]) > 0:
            f.write("\tpsk=\"{}\"\n".format(network_item["psk"]))

        f.write("\tkey_mgmt={}\n".format(network_item["key_mgmt"]))
        f.write("\tpriority={}\n".format(network_item["priority"]))
        f.write("}\n")
        f.write("\n")
        count += 1
    f.close()

    print("Wrote {} networks!".format(count))

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
    parser.add_argument('-p',
                        '--postfix',
                        metavar='postfix',
                        type=str,
                        default="",
                        help='Postfix to differentiate wpa_supplicant.conf files (writes to wpa_supplicant_<postfix>.conf')

    # Start of script
    args = parser.parse_args()

    input_path = args.inpath
    output_path = args.outpath
    output_postfix = args.postfix

    print("Processing input file at {}".format(input_path))
    if not os.path.exists(input_path):
        print('The file in the path specified does not exist')
        sys.exit()

    # Parse xml into list of dicts
    network_list = parse_xml(input_path)

    # Take xml and create wpa_supplicant.conf with it
    if len(output_postfix) > 0:
        out_name = "wpa_supplicant_{}.conf".format(output_postfix)
    else:
        out_name = "wpa_supplicant.conf"
    final_path = os.path.join(output_path, out_name)
    write_bool = write_conf_file(network_list, final_path)

    print("Finished!")
