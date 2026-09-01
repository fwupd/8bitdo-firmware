#!/usr/bin/env python3

# (c) 2025 Florian 'floe' Echtler <floe@butterbrot.org>
# (c) 2026 Arthur 'arthurlt' Tucker <arthur@tuckerfami.ly>
# SPDX-License-Identifier: GPL-3.0-or-later

# based on https://ladis.cloud/blog/posts/firmware-update-8bitdo.html

import argparse
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List
from urllib import request

SCRIPT_VERSION = "0.0.2"


@dataclass
class FirmwareDetails:
    date: str
    fileName: str
    androidDownload: int
    iOSDownload: int
    readme: str
    type: int
    version: str
    winDownload: int
    fileSize: int
    filePathName: str
    macDownload: int
    exists: bool
    fileURL: str
    readme_en: str
    id: int
    beta: str
    md5: str

    def parse_version(self) -> tuple[str, str]:
        version = str(self.version)
        return version[0:4], version[4:]


class FirmwareDownloadClient:
    def __init__(self, base_url: str = "http://dl.8bitdo.com:8080"):
        self.base_url = base_url

    def list_firmwares(self, gamepad_id: int, beta=True) -> List[FirmwareDetails]:
        type = str(gamepad_id)
        post_request = request.Request(
            self.base_url + "/firmware/select",
            data=b"",
            headers={"Type": type, "Beta": str(int(beta))},
            method="POST",
        )
        with request.urlopen(post_request) as response:
            data = json.loads(response.read().decode("utf-8"))
            return [FirmwareDetails(**detail) for detail in data.get("list", [])]

    def download_firmware(self, firmware: FirmwareDetails) -> Path:
        version, _ = firmware.parse_version()
        file_ext = Path(firmware.filePathName).suffix
        file_name = f"{firmware.fileName} Firmware v{version}{file_ext}"
        with (
            request.urlopen(self.base_url + firmware.filePathName) as response,
            open(file_name, "wb") as out_file,
        ):
            shutil.copyfileobj(response, out_file)
        # TODO: add md5sum check
        return Path(file_name).absolute()


def list_firmwares(client: FirmwareDownloadClient, args: argparse.Namespace) -> None:
    num = args.num
    firmwares = client.list_firmwares(num)

    if not firmwares:
        print(f"No firmware versions for controller ID/type #{num}")
        exit(1)

    print(f"Firmware versions for {firmwares[0].fileName} (#{num}):\n")

    for firmware in firmwares:
        version, build = firmware.parse_version()
        beta = " (beta) " if firmware.beta != "" else ""
        print(f"{version} (build {build}){beta}\n{firmware.readme_en}\n")


def fetch_firmwares(client: FirmwareDownloadClient, args: argparse.Namespace) -> None:
    num = args.num
    ver = args.ver

    firmwares = client.list_firmwares(num)

    print(f"Fetching firmware {ver} for {firmwares[0].fileName} (#{num}):\n")
    for firmware in firmwares:
        version, _ = firmware.parse_version()
        if ver == version:
            print("Downloading: " + version)
            file = client.download_firmware(firmware)
            print("Saved firmware to " + str(file) + ".\n")
            exit(0)

    print("... version not found.\n")
    exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=f"8BitDo Firmware Fetcher v{SCRIPT_VERSION}"
    )
    subparsers = parser.add_subparsers(dest="action")
    parser_list = subparsers.add_parser(
        "list", help="list all firmware versions for device [num]"
    )
    parser_list.add_argument("num", type=int, help="device number")
    parser_list.set_defaults(func=list_firmwares)

    parser_fetch = subparsers.add_parser(
        "fetch", help="fetch firmware version [ver] for device [num]"
    )
    parser_fetch.add_argument("num", type=int, help="device number")
    parser_fetch.add_argument("ver", type=str, help="firmware version")
    parser_fetch.set_defaults(func=fetch_firmwares)

    args = parser.parse_args()
    client = FirmwareDownloadClient()

    if not args.action:
        parser.print_help()
        exit(1)

    args.func(client, args)


if __name__ == "__main__":
    main()
