#!/bin/bash

# Script to robotically add a new ssh key to every host in your ~/.ssh/config
# Caution: This script is potentially destructive. Use at your own risk

if [[ $# -lt 2 ]]; then
  echo 'Usage: keyrotate.sh {old key} {new key}'
  exit 1
fi

oldkey="$1"
newkey="$2"

if [[ ! "$(find /tmp -name 'agent.*')" ]]; then
  echo 'Start yo fuckin ssh agent m9'
  exit 1
else
  if [[ ! "$(ssh-add -l | grep $oldkey)" ]]; then
    echo "[::] Requesting permission for $oldkey"
    ssh-add "$oldkey"
  fi
fi

HOSTS=$(egrep '^Host\ [^*]+' ~/.ssh/config | awk '{print $NF}')
for hostname in $HOSTS
do
  echo '[::] Making ~/.ssh/config'
  ssh $hostname 'mkdir ~/.ssh/config'
  echo '[::] Copying new key'
  scp $newkey'.pub' $hostname:~/.ssh/temp_pubkey
  echo '[::] Adding to ~/.ssh/authorized_keys'
  ssh $hostname 'cat ~/.ssh/temp_pubkey >> ~/.ssh/authorized_keys'
  echo '[::] Cleaning up'
  ssh $hostname 'rm ~/.ssh/temp_pubkey'
  exit 1
done
