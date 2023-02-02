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

def on_startup():
    init_service = (
        "systemctl --user import-environment \
        DISPLAY WAYLAND_DISPLAY XDG_CURRENT_DESKTOP",
        "hash dbus-update-activation-environment 2>/dev/null && \
        dbus-update-activation-environment --systemd \
        DISPLAY WAYLAND_DISPLAY XDG_CURRENT_DESKTOP",
        "/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1",
	"waybar",
    )

    for service in init_service:
        service = f"{service} &"
        os.system(service)


def on_reconfigure():
    gnome_schema = 'org.gnome.desktop.interface'
    gnome_peripheral = 'org.gnome.desktop.peripherals'
    wm_service_extra_config = (
        f"gsettings set {gnome_schema} gtk-theme 'Dracula'",
        f"gsettings set {gnome_schema} icon-theme 'Papirus'",
        f"gsettings set {gnome_schema} cursor-theme 'Catppuccin-Mocha-Dark-Cursors'",
        f"gsettings set {gnome_schema} cursor-size 16",
        f"gsettings set {gnome_schema} font-name 'Fira code medium 16'",
        "gsettings set org.gnome.desktop.wm.preferences button-layout :",
        f"gsettings set {gnome_peripheral}.keyboard repeat-interval 30",
        f"gsettings set {gnome_peripheral}.keyboard delay 500",
        f"gsettings set {gnome_peripheral}.mouse natural-scroll false",
        f"gsettings set {gnome_peripheral}.mouse speed 0.0",
        f"gsettings set {gnome_peripheral}.mouse accel-profile 'default'",
    )

    for config in wm_service_extra_config:
        config = f"{config} &"
        os.system(config)


corner_radius = 0

outputs = [
    { 'name': 'eDP-1', 'scale': 1.0, 'width': 1920, 'height': 1080,
      'mHz': 60, 'pos_x': 0, 'pos_y': 0 , 'anim': True },
]

pywm = {
    'xkb_model': "",
    'xkb_layout': "us,ru",
    'xkb_variant': "",
    'xkb_options': "grp:lalt_toggle",
    'enable_xwayland': True,
    'xcursor_theme': 'Catppuccin-Mocha-Dark-Cursors',
    'xcursor_size': 20,
    'tap_to_click': True,
    'natural_scroll': True,
    'focus_follows_mouse': True,
    'contstrain_popups_to_toplevel': False,
    'encourage_csd': False,
    'texture_shaders': 'basic',
    'renderer_mode': 'pywm',
}
def should_float(view):
    size = (700, 700)
    position = (0.5, 0.35)
    standard_float_apps = [
        "pavucontrol", "blueman-manager"
]
    if view.app_id in standard_float_apps:
        return True, size, position
    if view.app_id == "catapult":
        return True, None, (0.5, 0.1)

view = {
    # 'xwayland_handle_scale_clientside': not OUTPUT_MANAGER,
    'padding': 6,
    'fullscreen_padding': 15,
    'send_fullscreen': False,
    'accept_fullscreen': True,
    'should_float': should_float,
    'floating_min_size': False,
    'debug_scaling': True,
    'border_ws_switch': 100
}

mod = PYWM_MOD_LOGO
background = {
    'path': os.environ["HOME"] + "/wallp/2.jpg",
    'time_scale': 0.0,
    'anim': False,
}
energy = {
    'idle_callback': lambda event: "idle",
    'idle_times': 
    'enable_unlock_command': True
    'suspend_command': "systemctl suspend",
}
anim_time = .25
blend_time = 0.5
menu = 'wofi --show drun'
wlogout = 'wlogout'

def key_bindings(layout: Layout) -> list[tuple[str, Callable[[], Any]]]:


    return [
        ("L-e", lambda: os.system("nemo &")),
        ("L-f", lambda: os.system("firefox &")),
        ("L-d", lambda: os.system(f"{menu} &")),
        ("L-x", lambda: os.system(f"{wlogout} &")),

        ("L-Return", lambda: os.system("alacritty &")),

		#Управление фокусом
        ("L-Left", lambda: layout.move(-1, 0)),
        ("L-Down", lambda: layout.move(0, 1)),
        ("L-Up", lambda: layout.move(0, -1)),
        ("L-Right", lambda: layout.move(1, 0)),

        ("L-s", lambda: layout.move_in_stack(1)),
        ("L-space", lambda: layout.toggle_fullscreen()),
        ("L-S-space", lambda: layout.toggle_focused_view_floating()),

		#Изменение размера просмотра
        ("L-equal", lambda: layout.basic_scale(1)),
        ("L-minus", lambda: layout.basic_scale(-1)),

		#Перемещение окон
        ("L-S-Left", lambda: layout.move_focused_view(-1, 0)),
        ("L-S-Down", lambda: layout.move_focused_view(0, 1)),
        ("L-S-Up", lambda: layout.move_focused_view(0, -1)),
        ("L-S-Right", lambda: layout.move_focused_view(1, 0)),

		#Ресайз окон
        ("L-C-Left", lambda: layout.resize_focused_view(-1, 0)),
        ("L-C-Down", lambda: layout.resize_focused_view(0, 1)),
        ("L-C-Up", lambda: layout.resize_focused_view(0, -1)),
        ("L-C-Right", lambda: layout.resize_focused_view(1, 0)),

		#Показать все окна
        ("L-", lambda: layout.toggle_overview(only_active_workspace=True)),
		#Закрыть окно
        ("L-q", lambda: layout.close_focused_view()),
		#Обновить конфиг
        ("L-C", lambda: layout.update_config()),
        #Это не нужно удалять
        ("L-Q", lambda: layout.terminate()),
        #Выход из newm
        ("C-A-Delete", lambda: layout.terminate()),
        #Залочить десктоп
        ("C-A-l", lambda: layout.ensure_locked(dim=True)),

		#Функциональные клавиши
        ("XF86MonBrightnessUp", lambda: os.system("brightnessctl s +5%")),
        ("XF86MonBrightnessDown", lambda: os.system("brightnessctl s 5%-")),
        ("XF86AudioRaiseVolume", lambda: os.system("wpctl set-volume @DEFAULT_AUDIO_SINK@ 10%+")),
        ("XF86AudioLowerVolume", lambda: os.system("wpctl set-volume @DEFAULT_AUDIO_SINK@ 10%-")),
        ("XF86AudioMute", lambda: os.system("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")),
("Print", lambda: os.system('grim -g "$(slurp)" ~/Скрины/screen-"$(date\
            +%s)".png &')),
    ]

bar = {'enabled': False}

gestures = {
    'lp_freq': 120.0,
    'lp_inertia': 0.4,
}


swipe = {'gesture_factor': 3}

panels = {
    'lock': {
        'cmd': 'alacritty -e newm-panel-basic lock', 
 },
     "bar": {
        "cmd": "waybar",
        "visible_normal": True,
        "visible_fullscreen": True,
    },
}
grid = {"throw_ps": [2, 10]}


