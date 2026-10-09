#!/usr/bin/python3

# (c) 2025 Florian 'floe' Echtler <floe@butterbrot.org>
# SPDX-License-Identifier: GPL-3.0-or-later

# based on https://ladis.cloud/blog/posts/firmware-update-8bitdo.html

import requests, json, sys, os, time
import urllib.request

baseurl = "http://dl.8bitdo.com:8080"
enum_file = "firmware.results.json" # output file for cached enumeration (overridden with -e)
enum_max_misses = 5 # stop enumerating after 5 misses
enum_max_age = 7 * 24 * 60 * 60  # ask to re-enumerate after one week
enum_sleep_interval = 0.3 # how long to wait in between each enumeration request


def help():
    print("Usage: 8bitdo-firmware.py ...\n")
    print("\t-l\t\tlist all available devices")
    print("\t-l [num]\tlist all firmware versions for device [num]")
    print("\t-f [num] [ver]\tfetch firmware version [ver] for device [num]")
    print("\t-e [file]\tdevice type cache file (default: firmware.results.json)")
    print("\t-r\t\tre-enumerate device types\n")
    exit(0)


def enumerate_types():
    print("Enumerating device types...\n")
    results = {}
    misses = 0
    num = 1
    while misses < enum_max_misses:
        try:
            data = requests.post(baseurl + "/firmware/select", headers={"Beta": "1", "Type": str(num)}).json()
        except Exception:
            data = {}
        if isinstance(data.get("list"), list) and data["list"]:
            results[num] = data["list"]
            misses = 0
            print(f'{num}:\t{data["list"][0]["fileName"]}')
        else:
            misses += 1
        num += 1
        time.sleep(enum_sleep_interval)

    with open(enum_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {len(results)} device types to {enum_file}.\n")


def ask(question):
    return input(question + " [y/N] ").strip().lower() in ["y", "yes"]


print("8BitDo Firmware Fetcher v0.0.1\n")

args = sys.argv[1:]

if "-e" in args:
    i = args.index("-e")
    enum_file = args[i + 1]
    del args[i:i + 2]

force = "-r" in args
if force:
    args.remove("-r")

if not args or args[0] in ["-?", "-h", "--help"]:
    help()

if force:
    enumerate_types()
elif not os.path.exists(enum_file):
    print("Device types need to be enumerated first (one request per device type ID, takes about a minute, then cached).")
    if not ask("Enumerate now?"):
        exit(1)
    enumerate_types()
elif time.time() - os.path.getmtime(enum_file) > enum_max_age:
    print(f"{enum_file} is over a week old and may be missing new devices or firmware.")
    if ask("Re-enumerate now?"):
        enumerate_types()

with open(enum_file) as f:
    products = {int(num): fws for num, fws in json.load(f).items()}

if args[0] == "-l":

    if len(args) == 1:

        for num, item in products.items():
            print(f'{num}:\t{item[0]["fileName"]}')

    else:

        num = int(args[1])
        if num not in products:
            print("... device number not found.\n")
            exit(1)
        fws = products[num]

        print(f'Firmware versions for {fws[0]["fileName"]} (#{num}):\n')

        for fw in fws:
            ver = str(fw["version"])
            beta = " (beta)" if fw["beta"] != "" else ""
            print(f"{ver[0:4]} (build {ver[4:]})" + beta)

    print("")
    exit(0)

if args[0] == "-f":

    if len(args) != 3:
        help()

    num = int(args[1])
    ver = args[2]

    fws = products[num]

    print(f'Fetching firmware {ver} for {fws[0]["fileName"]} (#{num}):\n')
    for fw in fws:
        if str(fw["version"]).startswith(ver):
            url = baseurl + fw["filePathName"]
            file = os.path.basename(url)
            print("Downloading: " + url)
            urllib.request.urlretrieve(url, file)
            print("Saved firmware to " + file + ".\n")
            exit(0)

    print("... version not found.\n")
    exit(1)
