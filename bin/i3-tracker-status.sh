#!/bin/bash

if [[ -e /dev/shm/i3-tracker-status.txt ]];
then
  cat /dev/shm/i3-tracker-status.txt
else
  echo -n "[..] ------ i3tracking ------ |"
fi

