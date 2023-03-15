#!/bin/sh

# Session
export XDG_SESSION_TYPE=wayland
export XDG_SESSION_DESKTOP=wlroots
export XDG_CURRENT_DESKTOP=wlroots
export XDG_CURRENT_SESSION=wlroots
export XCURSOR_THEME=Catppuccin-Mocha-Dark-Cursors
export XCURSOR_SIZE=15
export repeat_rate=50
export repeat_delay=500
export gsettings set org.gnome.desktop.peripherals.keyboard repeat-interval 50
export gsettings set org.gnome.desktop.peripherals.keyboard delay 500

export XCURSOR_THEME=Catppuccin-Mocha-Dark-Cursors
export XCURSOR_SIZE=15
export GTK_THEME=Nordic
source /usr/local/bin/wayland_enablement.sh #we import the environment variables defined above

sleep 0.5;

start-newm
