#!/bin/bash
# This script gathers the currently tracked dotfiles into the repository


cd /home/deo
cp -v .zshrc /home/deo/Workspace/Dotfiles/
cp -v .config/compton/* /home/deo/Workspace/Dotfiles/.config/compton
cp -v .config/i3/* /home/deo/Workspace/Dotfiles/.config/i3
cp -v .config/polybar/* /home/deo/Workspace/Dotfiles/.config/polybar
cp -v .xinitrc /home/deo/Workspace/Dotfiles/.config/xorg
cp -v .config/xorg/.* /home/deo/Workspace/Dotfiles/.config/xorg

