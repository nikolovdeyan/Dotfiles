#!/usr/bin/env bash

polybar-msg -p "$(pgrep -f "polybar btmmainbar")" cmd toggle
