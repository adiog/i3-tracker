#!/bin/bash
# Copyright 2017 Aleksander Gajewski <adiog@brainfuck.pl>

# Register inactive state
if [[ "$1" == "TIMEOUT" ]]; then
    curl http://tracker/timeout/ > /dev/null && OK=OK || OK=".."
else
    curl http://tracker/userlock/ > /dev/null && OK=OK || OK=".."
fi
(echo -n "[$OK]: $1                      " | sed -e "s#^\(.\{30\}\).*#\1#"; echo -n "|") > /dev/shm/i3-tracker-status.txt

