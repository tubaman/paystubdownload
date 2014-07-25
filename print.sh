#!/bin/bash

PDFNAME=$1

echo "raise window"
xdotool search -name "Printer-Friendly" windowraise

echo "open hamburger menu"
xdotool mousemove 1175 100
xdotool click 1
sleep 1

echo "click print"
xdotool mousemove 950 320
xdotool click 1
sleep 1

echo "click print"
xdotool mousemove 50 70
xdotool click 1
sleep 1

xdotool mousemove 500 240
xdotool click 1
sleep 1

xdotool mousemove 500 370
xdotool click 1
sleep 1

echo "select all text"
xdotool key "ctrl+a"
sleep 1
xdotool key "BackSpace"
sleep 1

echo "name pdf"
xdotool type "$PDFNAME"
sleep 1

echo "click print"
xdotool mousemove 900 600
xdotool click 1
