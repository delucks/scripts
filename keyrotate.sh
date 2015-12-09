#!/usr/bin/env bash

# Script to robotically add a new ssh key to every host in your ~/.ssh/config
# Caution: This script is potentially destructive. Use at your own risk

esc=""
redf="${esc}[31m"
greenf="${esc}[32m"
reset="${esc}[0m"

if [[ $# -lt 2 ]]; then
  echo 'Usage: keyrotate.sh {old key} {new key}'
  exit 1
fi

oldkey="$1"
newkey="$2"

if [[ ! "$(find /tmp -name 'agent.*')" ]]; then
  echo $redf'Start yo fuckin ssh agent m9'$reset
  exit 1
else
  if [[ ! "$(ssh-add -l | grep $oldkey)" ]]; then
    echo "[::] Requesting permission for $oldkey"
    ssh-add "$oldkey"
  fi
fi

HOSTS=$(egrep '^Host\ [^*]+' ~/.ssh/config | awk '{print $NF}')
OLDCONTENTS="$(cat $oldkey'.pub')"
for hostname in $HOSTS
do
  echo
  echo "Processing $hostname:"
  ssh -o ConnectTimeout=10 -q $hostname 'exit'
  if [[ $? -gt 0 ]]; then
    echo "  [$redf$hostname$reset] Down"
    continue
  fi
  echo "  [$greenf$hostname$reset] Making ~/.ssh"
  ssh -q $hostname 'mkdir ~/.ssh'
  echo "  [$greenf$hostname$reset] Copying new key"
  scp -q $newkey'.pub' $hostname:~/.ssh/temp_pubkey
  echo "  [$greenf$hostname$reset] Adding to ~/.ssh/authorized_keys"
  ssh -q $hostname 'cat ~/.ssh/temp_pubkey >> ~/.ssh/authorized_keys'
  echo "  [$greenf$hostname$reset] Removing old key"
  ssh -q $hostname "grep -v \"${OLDCONTENTS}\" ~/.ssh/authorized_keys > ~/.ssh/temp_authorized_keys && cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys_backup && cp ~/.ssh/temp_authorized_keys ~/.ssh/authorized_keys"
  echo "  [$greenf$hostname$reset] Cleaning up"
  ssh -q $hostname 'rm ~/.ssh/temp_pubkey ~/.ssh/temp_authorized_keys'
  ssh -q $hostname 'sort ~/.ssh/authorized_keys | uniq > ~/.ssh/temp_new_key && mv ~/.ssh/temp_new_key ~/.ssh/authorized_keys'
done
