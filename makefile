CC = clang
CFLAGS = -Wall -std=c99 -pedantic
LDFLAGS = -shared
LIBRARY_PATH = -L. -L/path/to/python3.11/libs
PYTHON_LIB = -lpython3.11
PHYLIB_LIB = -lphylib

all: _phylib.dll

phylib.o: phylib.c
	$(CC) $(CFLAGS) -c phylib.c -o phylib.o

libphylib.dll: phylib.o
	$(CC) $(LDFLAGS) -o libphylib.dll phylib.o -lm

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/path/to/python3.11/include -o phylib_wrap.o

_phylib.dll: phylib_wrap.o libphylib.dll
	$(CC) $(LDFLAGS) phylib_wrap.o $(LIBRARY_PATH) $(PYTHON_LIB) $(PHYLIB_LIB) -o _phylib.dll

clean:
	del *.o *.dll
