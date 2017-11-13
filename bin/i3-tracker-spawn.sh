#!/bin/bash
# Copyright 2017 Aleksander Gajewski <adiog@brainfuck.pl>
#   created:  pon, 6 lis 2017, 07:35:41
#   modified: pon, 13 lis 2017, 16:34:08

cd $(dirname $0)

if [[ ! -d ~/.venvs/i3-tracker ]]; 
then
  mkdir -p ~/.venvs/
  virtualenv -p python3.6 ~/.venvs/i3-tracker
  . ~/.venvs/i3-tracker/bin/activate
  pip install -e .. --upgrade
  
  mkdir -p ~/.venvs/i3-tracker/spawn
  (
  echo ". ~/.venvs/i3-tracker/bin/activate"
  echo "i3-tracker-server runserver"
  ) > ~/.venvs/i3-tracker/spawn/i3-tracker-server
  chmod +x ~/.venvs/i3-tracker/spawn/i3-tracker-server
  i3-tracker-server makemigrations
  i3-tracker-server migrate

  (
  echo ". ~/.venvs/i3-tracker/bin/activate"
  echo "i3-tracker-tracker"
  ) >  ~/.venvs/i3-tracker/spawn/i3-tracker-tracker
  chmod +x  ~/.venvs/i3-tracker/spawn/i3-tracker-tracker
fi


screen -d -m -S i3-tracker-server bash ~/.venvs/i3-tracker/spawn/i3-tracker-server

screen -d -m -S i3-tracker-tracker bash ~/.venvs/i3-tracker/spawn/i3-tracker-tracker


