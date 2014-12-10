.SHELL=/bin/bash
TARGET?=/usr/share/ansible/plugins

define CITADEL_PY
import libcitadel

class LookupModule(libcitadel.S3LookupModule):
    bucket_var = 'citadel_bucket'
    profile_var = 'citadel_profile'
    region_var = 'citadel_region'
endef


.PHONY: all install

all: install

export CITADEL_PY
install:
	if [ ! -d $(TARGET)/lookup_plugins ]; then mkdir -p $(TARGET)/lookup_plugins; fi
	cp -p libcitadel.py $(TARGET)/lookup_plugins
	if [ ! -e $(TARGET)/lookup_plugins/citadel.py ]; then echo "$$CITADEL_PY" > $(TARGET)/lookup_plugins/citadel.py; fi
