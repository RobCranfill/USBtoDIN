#!/bin/bash
echo Copying files from $CP...

FILES="README.md
LED14.py
USBtoDIN.py
USBtoDIN_no_gui.py
USBtoDIN_LED14.py"

for f in $FILES
do
  cp $CP/$f .
done

git status

