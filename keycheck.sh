#!/bin/bash

# Check if an RSA key exists on all hosts in your ~/.ssh/config

if [[ $# -lt 1 ]]; then
  echo 'Usage: keycheck.sh {key}'
  exit 1
fi

ESC=""
REDF="${ESC}[31m"
GREENF="${ESC}[32m"
RESET="${ESC}[0m"
HOSTS=$(egrep '^Host\ [^*]+' ~/.ssh/config | awk '{print $NF}')
CONTENTS="$(cat $1'.pub')"

for hostname in $HOSTS; do
  ssh -o ConnectTimeout=10 -q $hostname "grep -q \"${CONTENTS}\" ~/.ssh/authorized_keys"
  if [[ $? -gt 0 ]]; then
    echo "[$REDF$hostname$RESET] Does not contain $1"
  else
    echo "[$GREENF$hostname$RESET] Contains $1"
  fi
done
