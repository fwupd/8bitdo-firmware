# Copyright (C) 2016 Richard Hughes <richard@hughsie.com>

VENDOR=8Bitdo
PROJECT_NAME=SN30v2
VERSION=6.14
FIRMWARE_FILES=Firmware_SN30v2_v$(VERSION).dat
METAINFO_FILES=sn30v2.metainfo.xml

all: $(VENDOR)-$(PROJECT_NAME)-$(VERSION).cab

clean:
	rm *.cab

check: $(METAINFO_FILES)
	appstream-util validate-relax $(METAINFO_FILES)

%.cab: $(FIRMWARE_FILES) $(METAINFO_FILES)
	gcab --create --nopath $@ "$(FIRMWARE_FILES)" $(METAINFO_FILES)
