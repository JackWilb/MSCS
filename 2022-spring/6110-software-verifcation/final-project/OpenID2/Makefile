#
# CS259 Homework 1
#
# This is a Makefile for the Murphi model of the NS(L) protocol.
#

MURPHI = ./Murphi3.1/bin/mu
MOPTS  = -b

CXX = g++ -DCATCH_DIV -fno-default-inline -Wno-deprecated
INCLUDE = ./Murphi3.1/include/

ns: ns.C
	${CXX} -I${INCLUDE} ns.C -o ns -lm

ns.C: ns.m
	${MURPHI} ${MOPTS} ns.m

report:
	pdflatex report.tex

clean:
	rm -f ns ns.C *~
	ls report.* | grep -v tex | xargs rm -rf

