# make --no-builtin-variables
CC?=cc
ifeq ($(shell uname -s),Darwin)
  CXX?=c++
else
  CXX?=g++
endif
AR?=ar
MAKE_VERSION?=4.2.1
KATI?=ckati
MAKE?=make
MAKECMDGOALS?=
CURDIR:=$(shell pwd)

# make --no-builtin-rules
.c.o:
	$(CC) $(CFLAGS) $(CPPFLAGS) $(TARGET_ARCH) -c -o $@ $<
.cc.o:
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) $(TARGET_ARCH) -c -o $@ $<

# make --file Makefile
-include $(CURDIR)/GNUmakefile
ifeq ($(shell uname -s),Darwin)
  -include $(CURDIR)/makefile
endif
-include $(CURDIR)/Makefile
