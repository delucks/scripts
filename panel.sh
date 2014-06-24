#!/bin/bash

# Finally gonna try to replace my shitty panels with something sexy

BATTERY_CAPACITY=/sys/class/power_supply/BAT0/capacity
BATTERY_STATUS=/sys/class/power_supply/BAT0/capacity

function tags {
	herbstclient tag_status | sed 's/[\t ]*//g' | sed -e 's/\../\ /g' | sed -e 's/:./▒/g' | sed -e 's/#./█/g'
}

function battery {
	if [ "$(cat $BATTERY_STATUS)" = "Charging" ]; then
		echo -n "+"
	elif [ "$(cat $BATTERY_STATUS)" = "Discharging" ]; then
		echo -n "-"
	else
		echo -n "~"
	fi
	sed -n p $BATTERY_CAPACITY
}

function volume {
	VOLUME=$(amixer get Master | sed -n 's/^.*\[\([0-9]\+\)%.*$/\1/p'| uniq)
	echo $VOLUME
}

function cpu {
	CPU=$(ps -eo pcpu |tail -n +2| awk 'BEGIN {sum=0.0f} {sum+=$1} END {print sum}')
	echo $CPU
}

while :; do
	buf=""
	buf="${buf} [$(tags)]		-- "
	buf="${buf} CPU: $(cpu) -"
	buf="${buf} VOL: $(volume) -"
	buf="${buf} BAT: $(battery) -"

	echo $buf
	sleep 1
done
