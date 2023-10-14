# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import subprocess
import webbrowser

from libqtile import bar, hook, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal


mod = "mod4"
alt = "mod1"
terminal = "konsole"
home = os.path.expanduser("~")

colors = []
cache = home + "/.cache/wal/colors"
def load_colors(cache):
    with open(cache, "r") as file:
        for i in range(8):
            colors.append(file.readline().strip())
    colors.append("#ffffff")
    lazy.reload()
load_colors(cache)

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle split stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "e", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Rofi shortcuts
    Key([mod], "z", lazy.spawn("/usr/bin/rofi -show drun .")),
    # Toggle keyboard layout switch
    Key([alt], "Shift_L", lazy.widget["keyboardlayout"].next_keyboard()),
    Key([mod], "F4", lazy.hide_show_bar("bottom")),
]

groups = [
    Group("1", layout="columns", matches=[Match(wm_class=[])]),
    Group("2", layout="columns", matches=[Match(wm_class=["xfce4-terminal"])]),
    Group("3", layout="columns"),
    Group("4", layout="columns"),
    Group("5", layout="columns"),
    Group("a", layout="columns", matches=[Match(wm_class=["vlc"])]),
    Group("s", layout="columns", matches=[Match(wm_class=["steam"])]),
    Group("d", layout="columns", matches=[Match(wm_class=["signal"])]),
    Group("f", layout="stack", matches=[Match(wm_class=["konsole"])]),
    Group("g", layout="columns", matches=[Match(wm_class=["qbittorrent"])]),
]

for k, group in zip(["1", "2", "3", "4", "5", "a", "s", "d", "f", "g"], groups):
    keys.append(Key([mod], (k), lazy.group[group.name].toscreen()))
    keys.append(Key([mod, "shift"], (k), lazy.window.togroup(group.name)))

layouts = [
    layout.Columns(
        border_focus_stack=[colors[1], colors[4]],
        border_width=2,
        border_on_single=True,
        margin=[0,6,0,6],
        margin_on_single=[0,6,0,6],
    ),
    layout.Stack(
        num_stacks=1,
        margin=[40, 430, 40, 430],
        border_width=0
    ),
    layout.Tile(
        add_after_last=True,
        border_focus=colors[4],
        border_normal=colors[1],
        border_width=4,
        margin=[0,4,0,4],
    ),
    layout.TreeTab(
        active_bg=colors[1],
        active_fg=colors[7],
        bg_color=colors[0],
        font="Iosevka",
        fontsize=12,
        margin_left=4,
        padding_left=4,
        panel_width=200,
    ),
]


widget_defaults = dict(
    font = "Iosevka Nerd Font Medium",
    fontsize = 14,
    padding = 2,
)

widget_leftbox = widget.TextBox(fmt="", foreground=colors[0], background="#00000000", fontsize=16, padding=-1)
widget_rightbox = widget.TextBox(fmt="", foreground=colors[0], background="#00000000", fontsize=16, padding=-1)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget_leftbox,
                widget.GroupBox(
                    background=colors[0],
                    foreground=colors[7],
                    block_highlight_text_color=colors[0],
                    highlight_color=colors[7],
                    active=colors[7],
                    inactive="#656565",
                    padding_x=4,
                    margin_x=0,
                    rounded=True,
                    highlight_method="block",
                    disable_drag=True,
                ),
                widget_rightbox,
                widget.Spacer(),
                widget_leftbox,
                widget.Clock(
                    format="%H:%M",
                    background=colors[0],
                    foreground=colors[7],
                    padding=4,
                ),
                widget_rightbox,
                widget.Spacer(),
                widget_leftbox,
                widget.Clock(
                    format="%A %d %b",
                    background=colors[0],
                    foreground=colors[7],
                    mouse_callbacks={
                        'Button1': lazy.spawn("gsimplecal"),
                    }
                ),
                widget_rightbox,
                widget.Spacer(length=8),
                widget_leftbox,
                widget.Wallpaper(
                    directory=home + "/Backgrounds",
                    random_selection=True,
                    background=colors[0],
                    label=" ",
                    wallpaper_command=["nitrogen", "--set-zoom-fill"],
                ),
                widget_rightbox,
                widget.Spacer(length=8),
                widget_leftbox,
                widget.OpenWeather(
                    background=colors[0],
                    foreground=colors[7],
                    fmt="{}",
                    location="Sofia",
                    format="{main_temp:.0f}°{units_temperature}",
                    mouse_callbacks={
                        "Button1": lambda: webbrowser.open_new_tab(
                            "https://www.meteoblue.com/en/weather/week/sofia_bulgaria_727011?day=1"
                        )

                    },
                ),
                widget.OpenWeather(
                    fontsize=16,
                    background=colors[0],
                    foreground=colors[7],
                    fmt="{}",
                    location="Sofia",
                    format="{icon}",
                ),
                widget_rightbox,
                widget.Spacer(length=8),
                widget_leftbox,
                widget.PulseVolume(
                    step=5,
                    background=colors[0],
                    foreground=colors[7],
                    padding=2,
                    limit_max_volume=True,
                    fmt="Vol: {}",
                    mouse_callbacks={
                        "Button3": lazy.spawn("pavucontrol -t 3"),
                        "Button2": lazy.spawn("pkill pavucontrol"),
                    },
                ),
                widget_rightbox,
                widget.Spacer(length=8),
                widget_leftbox,
                widget.KeyboardLayout(
                    fmt="  {}",
                    configured_keyboards=["us", "bg phonetic"],
                    background=colors[0],
                    display_map={"us":"En", "bg phonetic": "Bg"},
                    foreground=colors[7],
                ),
                widget_rightbox,
            ],
            size=22,
            background="#00000000",
            # border_color=[colors[0], colors[0], colors[0], colors[0]],
            # border_width=[3, 2, 3, 2],  # Draw top and bottom borders
            margin=[6, 6, 6, 6],  # Space around bar as int or list of ints [N E S W]
            opacity=0.6, # Bar window opacity
        ),
        bottom=bar.Bar(
            [
                widget.CurrentLayoutIcon(background=colors[0], padding=8, fontsize=12),
                widget.WidgetBox(
                    background=colors[0],
                    foreground=colors[7],
                    fontsize=12,
                    widgets=[
                        widget.CurrentLayout(background=colors[0], padding=4, fontsize=12),
                        widget.Sep(linewidth=20, foreground="#00000000"),
                        widget.TextBox(text="colorscheme:", fontsize=12, background="#00000000", foreground=colors[7]),
                        widget.Sep(linewidth=10, padding=2, foreground=colors[0]),
                        widget.Sep(linewidth=10, padding=2, foreground=colors[1]),
                        widget.Sep(linewidth=10, padding=2, foreground=colors[2]),
                        widget.Sep(linewidth=10, padding=2, foreground=colors[3]),
                        widget.Sep(linewidth=10, padding=2, foreground=colors[4]),
                        widget.Sep(linewidth=10, padding=2, foreground=colors[5]),
                        widget.Sep(linewidth=10, padding=2, foreground=colors[6]),
                        widget.Sep(linewidth=10, padding=2, foreground=colors[7]),
                        widget.Sep(linewidth=60, foreground="#00000000"),
                        widget.CPU(background="#00000000", foreground=colors[7], fontsize=12),
                        widget.Sep(linewidth=20, foreground="#00000000"),
                        widget.Memory(background="#00000000", foreground=colors[7], fontsize=12, format="mem: {MemUsed:.2f}{mm}/{MemTotal:.2f}{mm}", measure_mem="G"),
                        widget.Sep(linewidth=20, foreground="#00000000"),
                        widget.Net(
                            background="#00000000",
                            foreground=colors[7],
                            fontsize=12,
                            format="net: U:{up} D:{down}",
                            prefix="M",
                        ),
                    ]
                ),
                widget.Spacer(),
                widget.CheckUpdates(
                    distro="Arch_checkupdates",
                    update_interval=240,
                    display_format="{updates} Updates",
                    fontsize=12,
                    background="#00000000",
                    foreground=colors[7],
                    no_update_string="No updates",
                ),
                widget.Sep(linewidth=10, foreground="#00000000"),
                widget.Systray(icon_size=12),
            ],
            size=16,
            background="#00000000",
            # border_color=["ff00ff", "000000", "ff00ff", "000000"],  # Borders are magenta
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            margin=[6, 4, 2, 4],  # Space around bar as int or list of ints [N E S W]
            opacity=0.6, # Bar window opacity
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="Pavucontrol"),
        Match(wm_class="confirmreset"),  # gitk
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup
def start():
    subprocess.call([home + "/.config/qtile/autostart.sh"])
