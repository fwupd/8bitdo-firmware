#!/usr/bin/python3

import requests,json,sys

baseurl = "http://dl.8bitdo.com:8080"

things = {}

print("8BitDo Firmware Fetcher v0.0.1\n")

if len(sys.argv) == 1 or sys.argv[1] in [ "-?", "-h", "--help" ]:
    print("Halp!")
    exit(0)

response = requests.post(baseurl+"/firmware/select",headers={"Beta":"1"})
result = response.json()

for item in result["list"]:
    num = item["type"]
    if not num in things:
        things[num] = []
    things[num].append(item)

if sys.argv[1] == "-l":

    if len(sys.argv) == 2:
    
        for num,item in things.items():
            print(str(num)+":\t"+item[0]["fileName"])
        exit(0)

    else:

        num = int(sys.argv[2])
        fws = things[num]

        print("Firmware versions for "+fws[0]["fileName"]+" (#"+str(num)+"):\n")

        for fw in fws:
            ver = str(fw["version"])
            beta = " (beta)" if fw["beta"] != "" else ""
            print(ver[0:4]+"."+ver[4:]+beta)
