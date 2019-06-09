# Copyright (C) 2016 Richard Hughes <richard@hughsie.com>

VENDOR=8Bitdo
PROJECT_NAME=SF30_Pro-SN30_Pro
VERSION=1.30
FIRMWARE_FILES=Firmware_SF30&SN30_Pro_V$(VERSION).dat
METAINFO_FILES=sf30sn30pro.metainfo.xml

all: $(VENDOR)-$(PROJECT_NAME)-$(VERSION).cab

clean:
	rm *.cab

check: $(METAINFO_FILES)
	appstream-util validate-relax $(METAINFO_FILES)

%.cab: $(FIRMWARE_FILES) $(METAINFO_FILES)
	gcab --create --nopath $@ "$(FIRMWARE_FILES)" $(METAINFO_FILES)
