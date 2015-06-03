#!/bin/sh

L=presentation

if [ "$1" != "clean" ];
then
    cd pic
    for i in *.mp; do mpost "$i"; done
    cd ..
    pdflatex $L
    pdflatex $L
    pdflatex $L
else
    rm -f *.dvi *.log *.aux *.bbl *.blg $L.pdf *.ps *.nav *.out *.snm *.toc
    rm -f pic/*.? pic/*.log pic/*.mpx
fi
