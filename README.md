# Usage
## On linux with i3: i3-tracker-spawn.sh
## On linux without i3: x-tracker-spawn.sh

# i3-tracker-server: django webserver
* registering and storing events
* presenting daily time tracker
![screenshot](https://github.com/adiog/i3-tracker/raw/master/screenshot.png "Screenshot")

# i3-tracker-tracker
* process collecting i3 events

# x-tracker.sh
* alternative to i3-tracker-tracker: instead of subscribing to i3 events, scripts is polling on x and registering changed focus event in a loop.

# i3-tracker-helper.sh
* emits lock/inactivity events

# i3-tracker-status.sh
* trivial status text to be embedded into i3bar

# i3-tracker-locker.sh
* TBD: lock and register inactivity status

```
https://faq.i3wm.org/question/239/how-do-i-suspendlockscreen-and-logout.1.html
bindsym $mod+l exec "~/i3-locker.sh"
exec xautolock -time 15 -locker '~/i3-locker.sh' &
```
