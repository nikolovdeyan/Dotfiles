#! /bin/bash

## Original file from here: https://github.com/qtile/qtile-examples/

# If the process doesn't exists, start one in background
run() {
	if ! pgrep $1 ; then
		$@ &
	fi
}

# Just as the above, but if the process exists, restart it
run-or-restart() {
	if ! pgrep $1 ; then
		$@ &
	else
		process-restart $@
	fi
}

# Graphical authentication agent
run /usr/lib/polkit-kde-authentication-agent-1

# Setup keyboard layouts
run setxkbmap -model pc105 -layout us,bg -variant ,phonetic -option grp:alt_shift_toggle

run xset b off 				      # Disable beep
run xfce4-power-manager     # Power manager
run udiskie --tray --notify # Front-end to manage removable media from userspace

# Notification daemon
run /usr/bin/dunst -conf "$HOME/.config/dunst/dunstrc"

# Drop-down terminal
run guake


# Transparency, blurring, shadows
run picom --config "$HOME/.config/picom/picom.conf"

run wal -n -i
run nitrogen --set-zoom-fill "$(< "${HOME}/.cache/wal/wal")"
run qtile cmd-obj -o cmd -f reload_config

run signal-desktop
run qbittorrent
run steam
run firefox
run flameshot
# Some process you may want to start with Qtile
# run urxvtd -q -o					# URxvt daemon
# run cbatticon						# Battery icon and command
# run light-locker					# Screen locker
# run xfce4-clipman					# Clipboard management
# run mpd --no-daemon					# Music player daemon
