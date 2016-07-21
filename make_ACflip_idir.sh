#!/bin/sh
# flips AC cameras for wfov in a directory named like the input dir with suffix ACflip
FLIPDIR=${1}ACflip
if [ ! -d ${FLIPDIR} ]
then
    mkdir $FLIPDIR
fi
cd $1
find * -name '*AC16.png' | parallel convert {} -rotate 180 ../${FLIPDIR}/{}
cd ../$FLIPDIR
find ../$1 -type f -name '*FC16.png' | xargs -I {} ln -s {}
cd ..

