#!/bin/bash

sys_myapp_icon=$HOME/.local/share/icons/wireguard_icon.png
sys_myapp_desktop=$HOME/.local/share/applications/wireguard_tray.desktop
autoload_myapp_desktop=$HOME/.config/autostart/wireguard_tray.desktop

if [ -f "$sys_myapp_icon" ]; then rm $sys_myapp_icon; fi

if [ -f "$sys_myapp_desktop" ]; then rm $sys_myapp_desktop; fi

if [ -f "$PWD/wireguard_tray.desktop" ]; then rm $PWD/wireguard_tray.desktop; fi

if [ -f "$autoload_myapp_desktop" ]; then rm $autoload_myapp_desktop; fi




