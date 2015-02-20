#!/bin/bash
initializeANSI()
{
 esc=""

  blackf="${esc}[30m";   redf="${esc}[31m";    greenf="${esc}[32m"
  yellowf="${esc}[33m"   bluef="${esc}[34m";   purplef="${esc}[35m"
  cyanf="${esc}[36m";    whitef="${esc}[37m"
  
  blackb="${esc}[40m";   redb="${esc}[41m";    greenb="${esc}[42m"
  yellowb="${esc}[43m"   blueb="${esc}[44m";   purpleb="${esc}[45m"
  cyanb="${esc}[46m";    whiteb="${esc}[47m"

  boldon="${esc}[1m";    boldoff="${esc}[22m"
  italicson="${esc}[3m"; italicsoff="${esc}[23m"
  ulon="${esc}[4m";      uloff="${esc}[24m"
  invon="${esc}[7m";     invoff="${esc}[27m"

  reset="${esc}[0m"
}
if [[ $# -gt 0 ]];then
	if [[ "$1" -eq "dirty" ]];then
		DIRTY=0
	else
		DIRTY=1
	fi
else
	DIRTY=1
fi
initializeANSI
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
