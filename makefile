#export LD_LIBRARY_PATH=`pwd`

CC = clang
CFLAGS = -Wall -std=c99 -pedantic
LDFLAGS = -shared
LIBRARY_PATH = -L. -L/usr/lib/python3.11
PYTHON_LIB = -lpython3.11
PHYLIB_LIB = -lphylib

SHELL := /bin/bash

all: _phylib.so
	export LD_LIBRARY_PATH=$$(pwd)

phylib.o: phylib.c
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o

libphylib.so: phylib.o
	$(CC) $(LDFLAGS) -o libphylib.so phylib.o -lm

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11/ -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(LDFLAGS) phylib_wrap.o $(LIBRARY_PATH) $(PYTHON_LIB) $(PHYLIB_LIB) -o _phylib.so

clean:
	rm -f *.o *.so
