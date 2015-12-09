#!/usr/bin/env bash

if [[ $# -le 1 ]]; then
	echo "Usage: ./figletsample.sh 'Sample Text' filename.txt"
	exit 1
fi

for font in /usr/share/figlet/fonts/*.flf;do
	echo "$font" | tee -a "$2"
	echo "$1" | figlet -f $font | tee -a "$2"
	echo | tee -a "$2"
	echo | tee -a "$2"
	echo | tee -a "$2"
done
