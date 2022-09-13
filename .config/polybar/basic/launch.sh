#!/usr/bin/env bash
DIR="$HOME/.config/polybar/basic"
killall -q polybar
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done;

polybar mainbar -c "$DIR/config.ini" &
polybar auxbar -c "$DIR/config.ini" &
