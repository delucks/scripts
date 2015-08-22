#!/bin/bash
# check all git repos found under ~ for their cleanliness
if [[ $# -gt 0 ]];then
	if [[ "$1" ]];then
		DIRTY=0
	else
		DIRTY=1
	fi
else
	DIRTY=0
fi
esc=""
redf="${esc}[31m";
greenf="${esc}[32m"
reset="${esc}[0m"
repos=$(find ~ -name '.git')
echo "$repos" | while read line
do 
	baserepo=$(echo "$line"|sed 's/\.git$//g')
	cd $baserepo
	if [ -n "$(git status --untracked-files='no' --porcelain)" ];then
		echo "$baserepo is ${redf}dirty${reset}"
	else
		if [[ $DIRTY -eq 0 ]];then
			echo "$baserepo is ${greenf}clean${reset}"
		fi
	fi
done
