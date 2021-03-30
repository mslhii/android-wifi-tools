import argparse
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET


def parse_xml(xml_path):
    print("Parsing xml from {}".format(xml_path))

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

args = parser.parse_args()

input_path = args.inpath
output_path = args.outpath

print("Processing input file at {}".format(input_path))

if not os.path.exists(input_path):
    print('The file in the path specified does not exist')
    sys.exit()

parse_xml(input_path)