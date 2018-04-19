## Merge ~/.Xresources
[[ -f ~/.Xresources ]] && xrdb -merge -I$HOME ~/.Xresources

## Start i3wm
exec i3

## Start i3wm with logging
# exec i3 -V >> ~/i3log-$(date + '%F-%k-%M-%S') 2>&1

