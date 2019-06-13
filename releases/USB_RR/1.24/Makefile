# Copyright (C) 2016 Richard Hughes <richard@hughsie.com>

VENDOR=8Bitdo
PROJECT_NAME=USB_RR
VERSION=1.24
FIRMWARE_FILES=				\
	USB_RR_Firmware_V$(VERSION).dat
METAINFO_FILES=				\
	usbrr.metainfo.xml

all: $(VENDOR)-$(PROJECT_NAME)-$(VERSION).cab

clean:
	rm *.cab

check: $(METAINFO_FILES)
	appstream-util validate-relax $(METAINFO_FILES)

%.cab: $(FIRMWARE_FILES) $(METAINFO_FILES)
	gcab --create --nopath $@ $(FIRMWARE_FILES) $(METAINFO_FILES)
