#!/usr/bin/python3

# (c) 2025 Florian 'floe' Echtler <floe@butterbrot.org>
# SPDX-License-Identifier: GPL-3.0-or-later

# based on https://ladis.cloud/blog/posts/firmware-update-8bitdo.html

import requests,json,sys,os
import urllib.request

baseurl = "http://dl.8bitdo.com:8080"

products = {}

def help():
    print("Usage: 8bitdo-firmware.py ...\n")
    print("\t-l\t\tlist all available devices")
    print("\t-l [num]\tlist all firmware versions for device [num]")
    print("\t-f [num] [ver]\tfetch firmware version [ver] for device [num]\n")
    exit(0)

print("8BitDo Firmware Fetcher v0.0.1\n")

if len(sys.argv) == 1 or sys.argv[1] in [ "-?", "-h", "--help" ]:
    help()

response = requests.post(baseurl+"/firmware/select",headers={"Beta":"1"})
result = response.json()

for item in result["list"]:
    num = item["type"]
    if not num in products:
        products[num] = []
    products[num].append(item)

if sys.argv[1] == "-l":

    if len(sys.argv) == 2:
    
        for num,item in products.items():
            print(f"{num}:\t{item[0]["fileName"]}")

    else:

        num = int(sys.argv[2])
        if num not in products:
            print("... device number not found.\n")
            exit(1)
        fws = products[num]

        print(f"Firmware versions for {fws[0]["fileName"]} (#{num}):\n")

        for fw in fws:
            ver = str(fw["version"])
            beta = " (beta)" if fw["beta"] != "" else ""
            print(f"{ver[0:4]} (build {ver[4:]})"+beta)

    print("")
    exit(0)

if sys.argv[1] == "-f":

    if len(sys.argv) != 4:
        help()

    num = int(sys.argv[2])
    ver = sys.argv[3]

    fws = products[num]

    print(f"Fetching firmware {ver} for {fws[0]["fileName"]} (#{num}):\n")
    for fw in fws:
        if str(fw["version"]).startswith(ver):
            url = baseurl+fw["filePathName"]
            file = os.path.basename(url)
            print("Downloading: "+url)
            urllib.request.urlretrieve(url,file)
            print("Saved firmware to "+file+".\n")
            exit(0)

    print("... version not found.\n")
    exit(1)
