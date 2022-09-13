#!/usr/bin/env bash

# source wal colors.
# source ~/.cache/wal/colors.sh

# export envar with alpha set.
export color0_alpha1="#77${color0/'#'}"
export color0_alpha2="#cc${color0/'#'}"

DIR="$HOME/.config/polybar/liminal"
killall -q polybar
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done;

polybar mainbar_monitora -c "$DIR/config.ini" &
ln -s /tmp/polybar_mqueue.$! /tmp/ipc-mainbar_monitora
