VENDOR=8Bitdo
PROJECT_NAME=SN30_Pro+
VERSION=4.01
FIRMWARE_FILES=Firmware_SN30_Pro+_V$(VERSION).dat
METAINFO_FILES=sn30pro_plus.metainfo.xml

all: $(VENDOR)-$(PROJECT_NAME)-$(VERSION).cab

clean:
	rm *.cab

check: $(METAINFO_FILES)
	appstream-util validate-relax $(METAINFO_FILES)

%.cab: $(FIRMWARE_FILES) $(METAINFO_FILES)
	gcab --create --nopath $@ "$(FIRMWARE_FILES)" $(METAINFO_FILES)
