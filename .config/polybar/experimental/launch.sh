#!/usr/bin/env bash

# source wal colors.
source /home/deo/.cache/wal/colors.sh
# export envar with alpha set.
export color0_alpha1="#77${color0/'#'}"
export color0_alpha2="#cc${color0/'#'}"

DIR="/home/deo/.config/polybar/experimental"
killall -q polybar
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done;

# invoke bars and create symlinks to each channel for messages
# see: https://github.com/polybar/polybar/wiki/Inter-process-messaging
polybar topmainbar -c "$DIR/config.ini" &
ln -s /tmp/polybar_mqueue.$! /tmp/ipc-topmainbar

polybar topauxbar -c "$DIR/config.ini" &
ln -s /tmp/polybar_mqueue.$! /tmp/ipc-topauxbar

polybar btmmainbar -c "$DIR/config.ini" &
ln -s /tmp/polybar_mqueue.$! /tmp/ipc-btmmainbar
