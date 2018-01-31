#!/bin/bash
# Copyright 2017 Aleksander Gajewski <adiog@brainfuck.pl>
#   created:  Mon 11 Dec 2017 03:39:45 AM CET
#   modified: Mon 11 Dec 2017 03:53:55 AM CET

# BASH CLEANUP {{{
# PRIVATE:
BASH_TMPDIR=/dev/shm/
BASH_MKTEMP="mktemp --tmpdir=$BASH_TMPDIR"
BASH_CLEANUP_FILE=`$BASH_MKTEMP`
trap BASH_CLEANUP EXIT

function BASH_CLEANUP() {
  tac $BASH_CLEANUP_FILE | bash
  rm $BASH_CLEANUP_FILE
}

# PUBLIC:
function FINALLY() {
  echo "$*" >> $BASH_CLEANUP_FILE
}

function MKTEMP() {
  BASH_TMP=`$BASH_MKTEMP`
  FINALLY "rm $BASH_TMP"
  echo $BASH_TMP
}

function MKTEMP_DIR() {
  BASH_TMP=`$BASH_MKTEMP -d`
  FINALLY "rm -fr $BASH_TMP"
  echo $BASH_TMP
}
# }}}

PREV_NAME=""
while true;
do
  DATE=`date +%Y-%m-%dT%H:%M:%S.%6N`
  NAME=`xdotool getactivewindow getwindowname`
  CLASS=$(xprop WM_CLASS -id `xdotool getactivewindow`)
  CLASS=${CLASS/*= /}
  CLASS=${CLASS/*, /}
  CLASS=${CLASS/\"/}
  CLASS=${CLASS/\"/}
  echo __${NAME}__ __${CLASS}__
  if [[ "${NAME}" != "${PREV_NAME}" ]];
  then
    PAYLOAD="{\"type\": \"window::title\", \"name\": \"${NAME}\", \"workspace\": \"x\", \"window_class\": \"${CLASS}\", \"time\": \"${DATE}\"}"
    curl -d "${PAYLOAD}" 'http://tracker/register/'
    echo $PAYLOAD
  fi
  sleep 5;
  PREV_NAME=$NAME
done
