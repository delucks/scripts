#!/bin/bash

# frame out a python project as laid out in "Learn Python the Hard Way"
# run from the project directory ('skeleton' in LPtHW example), this will create necessary module/test subfolders

if [[ $# -lt 1 ]]; then
  echo "Usage: project.sh {name of project}"
fi

# Basic dirs
NAME="$1"
CWD="$(basename $(pwd))"
echo "Creating project directories with root import $NAME"
mkdir -p bin $NAME tests doc

# Module files
echo "Touching __init__.py for modules"
touch $NAME/__init__.py
touch tests/__init__.py

# Setup
echo "Creating setup.py with project name $CWD"
(
cat <<EOF
try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

config = {
  "description": "replaceme",
  "author": "replaceme",
  "url": "https://github.com/replaceme/$CWD",
  "download_url": "https://github.com/replaceme/$CWD",
  "author_email": "me@replaceme.com",
  "version": "0.1",
  "install_requires": ["nose"],
  "packages": ["$NAME"],
  "scripts": [],
  "name": "$CWD"
}

setup(**config)
EOF
) > "setup.py"

# Tests
echo "Creating skeleton tests for $NAME module"
(
cat <<EOF
from nose.tools import *
import $NAME

def setup():
    print 'SETUP!'

def teardown():
    print 'TEAR DOWN!'

def test_basic():
    print 'I RAN!'
EOF
) > "tests/${NAME}_tests.py"

echo 'Running `nosetests` to check your progress!'
nosetests
