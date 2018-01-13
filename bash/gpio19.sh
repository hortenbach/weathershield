#!/bin/sh

echo "19" > /sys/class/gpio/export      
echo "out" > /sys/class/gpio/gpio19/direction
echo "0" > /sys/class/gpio/gpio19/value
