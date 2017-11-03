#!/bin/bash
# Copyright 2017 Aleksander Gajewski <adiog@brainfuck.pl>

# Register inactive state
i3-tracker-helper.sh $1

# Take a screenshot
gnome-screenshot -f /tmp/screen_locked.png

# Pixellate it 10x
mogrify -scale 5% -scale 2000% /tmp/screen_locked.png

# Lock screen displaying this image.
i3lock -i /tmp/screen_locked.png

# Turn the screen off after a delay.
function cleanup()
{
    sleep 60; pgrep -q i3lock && xset dpms force off
}
cleanup &
