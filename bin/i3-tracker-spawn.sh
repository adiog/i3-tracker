#!/bin/bash
# Copyright 2017 Aleksander Gajewski <adiog@brainfuck.pl>
#   created:  pon, 6 lis 2017, 07:35:41
#   modified: Tue 05 Feb 2019 06:32:26 AM CET

cd $(dirname $0)

if [[ ! -d ~/.venvs/i3-tracker ]];
then
  mkdir -p ~/.venvs/
  python3 -m virtualenv -p python3 ~/.venvs/i3-tracker
  . ~/.venvs/i3-tracker/bin/activate
  python3 -m pip install -e .. --upgrade

  grep -q -e "127.0.0.1.*\<tracker\>" /etc/hosts || sudo sed -e "s#127\.\0\.0\.1\s.*#& tracker#" -i /etc/hosts

  if [[ ! -e /etc/nginx/sites-enabled/tracker ]];
  then
    sudo apt install nginx
    sudo mkdir -p /etc/nginx/sites-enabled/
    sudo ln -fs $(realpath ../etc/nginx/sites-enabled/tracker) /etc/nginx/sites-enabled/tracker
    sudo service nginx restart
  fi

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

screen -ls | grep -q i3-tracker-server || \
  screen -d -m -S i3-tracker-server bash ~/.venvs/i3-tracker/spawn/i3-tracker-server
screen -ls | grep -q i3-tracker-tracker || \
  screen -d -m -S i3-tracker-tracker bash ~/.venvs/i3-tracker/spawn/i3-tracker-tracker

