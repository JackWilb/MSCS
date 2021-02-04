# Author: Ryan Stutsman <stutsman@cs.utah.edu>
# Basic Makefile for CS5460 Assignment 1
# Copyright 2020 University of Utah. All rights reserved.

# Use the latest version of GCC.
CC := /usr/local/bin/gcc-10

# Turn off the optimizer to make debugging easier.
# Use the latest C standard; language reference here:
#  https://en.cppreference.com/w/c
# Turn on all warnings.
# Turn on pedantic warnings.
# Make all warnings errors.
# Compile in undefined behavior sanitizer.
# Make all UBsan failures cause exit.
# Retain the frame pointer to make debugging easier.
CFLAGS := -O0 \
	-ggdb \
	-std=c11 \
	-Wall \
	-pedantic \
	-Werror \
	-fsanitize=undefined \
	-fno-sanitize-recover \
	-fno-omit-frame-pointer

# Link in math lib and substitute our own implementations of malloc and free.
LDFLAGS := -lm \
	-Wl,--wrap=malloc,--wrap=free,--wrap=calloc,--wrap=realloc

# By default comiler the tester target.
all: tester

# Make an .o target for each .c and make it depend on the headers as well.
%.o: %.c assignment1.h tester.h
	$(CC) $(CFLAGS) -c $<

# Make tester target depend on the .o files.
tester: tester.o assignment1.o tests.o
	$(CC) $(LDFLAGS) $(CFLAGS) -static -o $@ $^

# Always run clean and test regardless of dependencies.
.PHONY: clean test

# Remove .o files and tester, ignore failures.
clean:
	-rm *.o tester

# Run tester with per-test forking.
test: tester
	./tester -f

# Run tester with gdb and disable the per-test forking.
debug: tester
	gdb --args ./tester