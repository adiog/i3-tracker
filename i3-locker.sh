#!/bin/bash
# Copyright 2017 Aleksander Gajewski <adiog@brainfuck.pl>

# Register inactive state
curl http://tracker/inactive/ > /dev/null

# Take a screenshot
gnome-screenshot -f /tmp/screen_locked.png

# Pixellate it 10x
mogrify -scale 5% -scale 2000% /tmp/screen_locked.png

# Lock screen displaying this image.
i3lock -i /tmp/screen_locked.png

# Turn the screen off after a delay.
sleep 60; pgrep i3lock && xset dpms force off
