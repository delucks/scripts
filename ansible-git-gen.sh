#!/usr/bin/env bash
# this will generate an ansible playbook to pull 
# all git repos inside yer home directory
# pipe this into some file, like foo.yml
# then,
# ansible-playbook -i localhost, foo.yml
cat << EOM
---
- hosts: localhost
  remote_user: $(whoami)
  vars:
    gitmappings:
EOM
for item in $(find ~ -type d -name '.git'); do
  cd $item
  echo "      - path: $(echo $item | sed 's/\.git$//g')"
  echo "        src: $(egrep -A 2 '\[remote "origin"\]' config | grep url | awk '{print $NF}')"
  cd - > /dev/null 2>&1
done
cat << EOM
  tasks:
    - name: pull all repositories
      git: repo={{ item.src }} dest={{ item.path }} update=yes
      with_items: "{{gitmappings}}"
EOM
