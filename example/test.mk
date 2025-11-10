# Simple test Makefile
CC = gcc
CFLAGS = -Wall -O2
SRC = main.c helper.c
OBJ = $(SRC:.c=.o)
TARGET = myapp

.PHONY: all clean install

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f $(OBJ) $(TARGET)

install: $(TARGET)
	cp $(TARGET) /usr/local/bin/

# Test some variables
PREFIX ?= /usr/local
BINDIR = $(PREFIX)/bin
VERSION = 1.0.0
