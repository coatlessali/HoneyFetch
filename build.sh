#!/bin/bash
pyinstaller HoneyFetch.py --hidden-import='PIL._tkinter_finder'
cp gato.png dist/HoneyFetch/gato.png