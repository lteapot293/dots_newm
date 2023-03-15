from __future__ import annotations
from typing import Callable, Any

import os
import pwd
import time
import logging

from newm.layout import Layout
from newm.helper import BacklightManager, WobRunner, PaCtl

from pywm import (
    PYWM_MOD_LOGO,
    PYWM_MOD_ALT
)

logger = logging.getLogger(__name__)

pywm = {
    'xkb_model': "",
    'xkb_layout': "us,ru",
    'xkb_variant': "",
    'xkb_options': "grp:lalt_toggle",
    'enable_xwayland': True,
    'xcursor_theme': 'Qogirr-Dark',
    'xcursor_size': 15,
    'tap_to_click': True,
    'natural_scroll': False,
    'focus_follows_mouse': True,
    #'contstrain_popups_to_toplevel': True,
    'encourage_csd': False,
    'texture_shaders': 'basic',
    'renderer_mode': 'pywm',
}

def on_reconfigure():
    gnome_schema = "org.gnome.desktop.interface"
    gnome_peripheral = "org.gnome.desktop.peripherals"
    gnome_preferences = "org.gnome.desktop.wm.preferences"
    # easyeffects = "com.github.wwmm.easyeffects"
    theme = "Nordic"
    icons = "Papirus-Dark"
    cursor = "Catppuccin-Mocha-Dark-Cursors"
    font = "Fira code medium 12"
    gtk2 = "~/.gtkrc-2.0"

    GSETTINGS = (
        f"gsettings set {gnome_preferences} button-layout :",
        f"gsettings set {gnome_preferences} theme {theme}",
        f"gsettings set {gnome_schema} gtk-theme {theme}",
        f"gsettings set {gnome_schema} color-scheme prefer-dark",
        f"gsettings set {gnome_schema} icon-theme {icons}",
        f"gsettings set {gnome_schema} cursor-theme {cursor}",
        f"gsettings set {gnome_schema} cursor-size 15",
        f"gsettings set {gnome_schema} font-name '{font}'",
        f"gsettings set {gnome_peripheral}.keyboard repeat-interval 50",
        f"gsettings set {gnome_peripheral}.keyboard delay 500",
        f"gsettings set {gnome_peripheral}.mouse natural-scroll true",
        f"gsettings set {gnome_peripheral}.mouse speed 0.0",
        f"gsettings set {gnome_peripheral}.mouse accel-profile 'default'",
        # f"gsettings {easyeffects} process-all-inputs true",
        # f"gsettings {easyeffects} process-all-outputs true",
    )

    def options_gtk(file, c=""):
        CONFIG_GTK = (
            set_value(f"gtk-theme-name={c}{theme}{c}", file),
            set_value(f"gtk-icon-theme-name={c}{icons}{c}", file),
            set_value(f"gtk-font-name={c}{font}{c}", file),
            set_value(f"gtk-cursor-theme-name={c}{cursor}{c}", file),
        )
        execute_iter(CONFIG_GTK)

    # options_gtk(gtk3)
    options_gtk(gtk2, '"')
    execute_iter(GSETTINGS)
    # gtk4
    # os.environ["GTK_THEME"] = theme
    # os.system("killall albert &")
    # os.system("albert &")
    notify("Reload", "update config success")
    
def on_startup():
    init_service = (
        "/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1",
        "systemctl --user import-environment \
        DISPLAY WAYLAND_DISPLAY XDG_CURRENT_DESKTOP",
        "hash dbus-update-activation-environment 2>/dev/null && \
        dbus-update-activation-environment --systemd \
        DISPLAY WAYLAND_DISPLAY XDG_CURRENT_DESKTOP",
		os.system("waybar &"),
    )

    for service in init_service:
        service = f"{service} &"
        os.system(service)
		
background = {
    "path": os.path.expanduser("~/wallp/1.png"),
    "time_scale": 0.11,
    "anim": False,
}

anim_time = 0.1
blend_time = 0.5
corner_radius = 10

outputs = [
    { 'name': 'eDP-1' }
]

def app_rules(view):
    common_float = {"float": True}
    common_blur = {"blur": {"radius": 6, "passes": 4}}
    float_apps = ("pavucontrol", "imv", "mpv", "dialog", "title: Properties", "polkit-kde-authentication-agent-1", "title:Open File",  )  #Плавающие окна
    blur_apps = ()  #Окна с блюром
    if view.app_id in float_apps:
        return common_float
    if view.app_id in blur_apps:
        return common_blur

    #Правила для wlogout 
    if view.app_id == "wlogout":
        return { "float": True, "float_size": (1920, 1080) }
    
    #Правила для wofi
    if view.app_id == "wofi":
        return { "float": True }

    return None


# ВНЕШНИЙ ВИД ОКОН #################################################################
view = {
    'corner_radius': 5,	#Скруглние окон
    'padding': 2, #Гапсы
    'margin': 5,
    'fullscreen_padding': 5,
    'send_fullscreen': False,
    'accept_fullscreen': False,
    'floating_min_size': False,
    'debug_scaling': True,
    #'border_ws_switch': 100,
    'rules': app_rules,
    'ssd': {
		'enabled': False,
		'color': '#FAE3B0FF',
		'width': 2,
    },
}

interpolation = {
    'size_adjustment': 0.5
}

menu = 'wofi --show drun'

def key_bindings(layout: Layout) -> list[tuple[str, Callable[[], Any]]]:
    return [
        ("L-Left", lambda: layout.move(-1, 0)),
        ("L-Down", lambda: layout.move(0, 1)),
        ("L-Up", lambda: layout.move(0, -1)),
        ("L-Right", lambda: layout.move(1, 0)),

        ("L-s", lambda: layout.move_in_stack(1)),
        ("L-space", lambda: layout.toggle_fullscreen()),
        ("L-S-space", lambda: layout.toggle_focused_view_floating()),
        
        ("L-equal", lambda: layout.basic_scale(1)),
        ("L-minus", lambda: layout.basic_scale(-1)),
        ("L-t", lambda: layout.move_in_stack(1)),

         ("L-S-Left", lambda: layout.move_focused_view(-1, 0)),
        ("L-S-Down", lambda: layout.move_focused_view(0, 1)),
        ("L-S-Up", lambda: layout.move_focused_view(0, -1)),
        ("L-S-Right", lambda: layout.move_focused_view(1, 0)),

        ("L-C-Left", lambda: layout.resize_focused_view(-1, 0)),
        ("L-C-Down", lambda: layout.resize_focused_view(0, 1)),
        ("L-C-Up", lambda: layout.resize_focused_view(0, -1)),
        ("L-C-Right", lambda: layout.resize_focused_view(1, 0)),

        ("L-Return", lambda: os.system("alacritty &")),
        ("L-d", lambda: os.system(f"{menu} &")),
        ("L-e", lambda: os.system("nemo &")),
        ("L-g", lambda: os.system("geany &")),
        ("L-f", lambda: os.system("firefox &")),
        ("L-q", lambda: layout.close_focused_view()),

        ("L-p", lambda: layout.ensure_locked(dim=True)),
        ("L-P", lambda: layout.terminate()),
        ("L-C", lambda: layout.update_config()),

        ("L-F", lambda: layout.toggle_fullscreen()),

        ("L-", lambda: layout.toggle_overview()),

         ("XF86MonBrightnessUp", lambda: os.system("brightnessctl s +10%")),
        ("XF86MonBrightnessDown", lambda: os.system("brightnessctl s 10%-")),
        ("XF86AudioRaiseVolume", lambda: os.system("amixer -q \
            set Master 5%+")),
        ("XF86AudioLowerVolume", lambda: os.system("amixer -q \
            set Master 5%-")),
        ("XF86AudioMute", lambda: os.system("amixer set Master toggle")),
    ]

panels = {
    "bar": {
        "cmd": "waybar",
        "visible_normal": True,
        "visible_fullscreen": False,
    },
}

gestures = {
    'lp_freq': 60.,
    'lp_inertia': 0.8,
    'two_finger_min_dist': 0.1,
    'validate_threshold': 0.02,

    'c': {
		'enabled': True,
		'scale_px': 800,
    },

    'dbus': {
		'enabled': True,
    },

    'pyevdev': {
		'enabled': False,
		'two_finger_min_dist': 0.1,
		'validate_threshold': 0.02,
    },
}

swipe = {
    'gesture_factor': 3,
    'grid_m': 1,
    'grid_ovr': 0.2,
    'lock_dist': 0.01,
}

swipe_zoom = {
    'gesture_factor': 3,
    'grid_m': 1,
    'grid_ovr': 0.2,
    'hyst': 0.2,
}

grid = {
    'min_dist': .05,
    'throw_ps': [2, 10],
    'time_scale': 0.3,
}

resize = {
    'grid_m': 3,
    'grid_ovr': 0.1,
    'hyst': 0.2,
}

move = {
    'grid_m': 3,
    'grid_ovr': 0.1,
}

move_resize = {
    'gesture_factor': 2
}

focus = {
    'enabled': True,
    'color': '#96CDFBFF', #Цвет рамки
    'distance': 4, #Отступ рамки от окна
    'width': 5, #Толщина рамки
    'animate_on_change': False,
    'anim_time': 0.25, #Время анимации
}

energy = {
    'idle_callback': lambda event: "idle",
	'idle_times': [],
}
