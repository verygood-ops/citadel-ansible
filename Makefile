SHELL=/bin/bash
DEFAULT_TARGET=/usr/share/ansible/plugins
TARGET?=$(DEFAULT_TARGET)

define CITADEL_PY
import libcitadel

class LookupModule(libcitadel.S3LookupModule):
    bucket_var = 'citadel_bucket'
    profile_var = 'citadel_profile'
    region_var = 'citadel_region'
endef

define LIBCITADEL_ANNOTATION

# simple installation directly into lookup_plugins
LookupModule = S3LookupModule
endef

.PHONY: all install

all: install

export CITADEL_PY
export LIBCITADEL_ANNOTATION
install:
	if [ ! -d $(TARGET)/lookup_plugins ]; then mkdir -p $(TARGET)/lookup_plugins; fi
	cp -p libcitadel.py $(TARGET)/lookup_plugins/citadel.py
	echo "$$LIBCITADEL_ANNOTATION" >> $(TARGET)/lookup_plugins/citadel.py


# if we don't want to install libcitadel in the ansible virtualenv (or
# system-wide package), then we want to install into a target, in which
# case, the resulting file should be `citadel.py`

# if we do want to install with the virtualenv / or ansible python interpreter
# then the current install strategy works
# if [ ! -e $(TARGET)/lookup_plugins/citadel.py ]; then echo "$$CITADEL_PY" > $(TARGET)/lookup_plugins/citadel.py; fi
