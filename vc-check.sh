#!/bin/bash
# check all git and svn repos found under ~ (or some arbitrary directory) for their cleanliness

usage() {
  echo "Usage: $0 <directory>"
  echo
  echo "This script recursively looks through"
  echo "a directory for paths under svn or git"
  echo "version control, and gets the status of"
  echo "each."
  echo
  echo "Flags:"
  echo "  -c      Enable colorization"
  echo "  -d      Show only dirty repos"
  echo "  -g      Show only git repos"
  echo "  -s      Show only svn repos"
}

handle_git() {
  if [ $# -lt 1 ]
  then
    return 1
  fi
	baserepo=$(echo "$1"|sed 's/\.git$//g')
  cd $baserepo 1>/dev/null
	if [ -n "$(git status --untracked-files='no' --porcelain)" ]
  then
    echo "$baserepo ${redf}dirty${reset}"
  else
    if [ $DIRTYONLY == 0 ]
    then
      echo "$baserepo ${greenf}clean${reset}"
    fi
  fi
  cd - 1>/dev/null
}

handle_svn() {
  if [ $# -lt 1 ]
  then
    return 1
  fi
	baserepo=$(echo "$1"|sed 's/\.svn$//g')
  if [ -n "$(svn status $baserepo)" ]
  then
    echo "$baserepo ${redf}dirty${reset}"
  else
    if [ $DIRTYONLY == 0 ]
    then
      echo "$baserepo ${greenf}clean${reset}"
    fi
  fi
}

# parse my args
COLOR=0
DIRTYONLY=0
GITONLY=0
SVNONLY=0
while [[ $1 =~ -[cdgsh] ]]
do
  case "$1" in
    -c) COLOR=1
    ;;
    -d) DIRTYONLY=1
    ;;
    -g) GITONLY=1
    ;;
    -s) SVNONLY=1
    ;;
    -h) usage && exit 1
    ;;
  esac
  shift
done

# positional argument, a directory to start from
DIR="${1:-$HOME}"

if [ $COLOR == 1 ]
then
  esc=""
  redf="${esc}[31m";
  greenf="${esc}[32m"
  reset="${esc}[0m"
fi

if [ $GITONLY == 1 ]
then
  repos=$(find $DIR -name ".git")
elif [ $SVNONLY == 1 ]
then
  repos=$(find $DIR -name ".svn")
else
  repos=$(find $DIR \( -name ".git" -o -name ".svn" \))
fi

echo "$repos" | while read vcpath
do 
  if [[ $vcpath == *".git"* ]]
  then
    handle_git $vcpath
  else
    handle_svn $vcpath
  fi
done
