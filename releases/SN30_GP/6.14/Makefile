# Copyright (C) 2019 Richard Hughes <richard@hughsie.com>
# Copyright (C) 2019 Mikhail f. Shiryaev <mr.felixoid@gmail.com>

VENDOR=8Bitdo
PROJECT_NAME=SN30_GP
VERSION=6.14
FIRMWARE_FILES=$(wildcard *.dat)
METAINFO_FILES=sn30gp.metainfo.xml

all: $(VENDOR)-$(PROJECT_NAME)-$(VERSION).cab

clean:
	rm *.cab

check: $(METAINFO_FILES)
	appstream-util validate-relax $(METAINFO_FILES)

%.cab: $(FIRMWARE_FILES) $(METAINFO_FILES)
	gcab --create --nopath $@ "$(FIRMWARE_FILES)" $(METAINFO_FILES)
