# Copyright (C) 2016 Richard Hughes <richard@hughsie.com>

VENDOR=8Bitdo
PROJECT_NAME=N30Pro2
VERSION=6.10
FIRMWARE_FILES=$(wildcard *.dat)
METAINFO_FILES=n30pro2.metainfo.xml

all: $(VENDOR)-$(PROJECT_NAME)-$(VERSION).cab

clean:
	rm *.cab

check: $(METAINFO_FILES)
	appstream-util validate-relax $(METAINFO_FILES)

%.cab: $(FIRMWARE_FILES) $(METAINFO_FILES)
	gcab --create --nopath $@ "$(FIRMWARE_FILES)" $(METAINFO_FILES)
