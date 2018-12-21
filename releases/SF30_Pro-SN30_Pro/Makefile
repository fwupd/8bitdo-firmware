# Copyright (C) 2016 Richard Hughes <richard@hughsie.com>

VENDOR=8Bitdo
PROJECT_NAME=SF30_Pro-SN30_Pro
FIRMWARE_FILES=$(wildcard */*.dat)
METAINFO_FILES=n30pro2.metainfo.xml
METAINFO_FILES=sf30sn30pro.metainfo.xml

all: $(VENDOR)-$(PROJECT_NAME).cab

clean:
	rm *.cab

check: $(METAINFO_FILES)
	appstream-util validate-relax $(METAINFO_FILES)

%.cab: $(FIRMWARE_FILES) $(METAINFO_FILES)
	gcab --create --nopath $@ $(addprefix ",$(addsuffix ",$(FIRMWARE_FILES))) $(METAINFO_FILES)
