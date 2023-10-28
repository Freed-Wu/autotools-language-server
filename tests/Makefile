#!/usr/bin/env -S make -f
.PHONY: default
default: all
include common.mk
include fake.mk
-include fake.mk

export KBUILD_EXTMOD
export abs_objtree := $(CURDIR)
unexport KBUILD_EXTMOD
define f
	@echo $(1)
endef
.PHONY: default all
default all: test
	$(call f,test)
	ls $(CURDIR)
DRIVER_NAME := $(notdir $(SRC))
ifneq ($(KERNELRELEASE),)
	obj-m := $(DRIVER_NAME).o
else
	KERNEL_SRC := /usr/src/linux
	KERNEL_MAKE := $(MAKE) -C$(KERNEL_SRC) M=$(SRC)
	RULES := all modules modules_prepare modules_check modules_install clean
.PHONY: default $(RULES) install uninstall reinstall
default:
	$(KERNEL_MAKE)
$(RULES):
	$(KERNEL_MAKE) $@
endif
pwd
