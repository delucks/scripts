#!/bin/bash

#################################
# QWOP Bot for CAGDstravaganza 	#
# Author: Ryan Keeley						#
# Date: May 10, 2014						#
#################################

sleep 5
xdotool key space
sleep 3

function press () {
	[[ ! $1 ]] && exit 1

	xdotool keydown $1
	sleep .2s
	xdotool keyup $1
}

for i in {1..10000}; do
	for j in q w o p; do press $j; done
done
