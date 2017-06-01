# Copyright (C) 2016 Richard Hughes <richard@hughsie.com>

VENDOR=8Bitdo
PROJECT_NAME=SFC30_NES30_SFC30_SNES30
VERSION=2.67
FIRMWARE_FILES=				\
	bluetooth_firmware_V2.67.dat
METAINFO_FILES=				\
	fc30.metainfo.xml		\
	nes30.metainfo.xml		\
	sfc30.metainfo.xml		\
	snes30.metainfo.xml

all: $(VENDOR)-$(PROJECT_NAME)-$(VERSION).cab

clean:
	rm *.cab

check: $(METAINFO_FILES)
	appstream-util validate-relax $(METAINFO_FILES)

%.cab: $(FIRMWARE_FILES) $(METAINFO_FILES)
	gcab --create --nopath $@ $(FIRMWARE_FILES) $(METAINFO_FILES)
