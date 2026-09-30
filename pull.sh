#!/bin/bash
echo Copying files from $CP...

FILES="README.md
USBtoDIN.py"

for f in $FILES
do
  cp $CP/$f .
done

git status

