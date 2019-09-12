#!/bin/bash

sys_icon_dir=$HOME/.local/share/icons/
sys_myapp_desktop=$HOME/.local/share/applications/wireguard_tray.desktop

myapp=$PWD/wireguard_tray.py
myapp_icon=$PWD/icons/wireguard_icon.png

cp $myapp_icon $sys_icon_dir

chmod 444 $sys_icon_dir/wireguard_icon.png

echo "[Desktop Entry]" > $sys_myapp_desktop
echo "Name=WireGuard Indicator" >> $sys_myapp_desktop
echo "Comment=Program to connect WireGuard tunell" >> $sys_myapp_desktop
echo "Exec=$myapp" >> $sys_myapp_desktop
echo "Icon=wireguard_icon.png" >> $sys_myapp_desktop
echo "Terminal=false" >> $sys_myapp_desktop
echo "Type=Application" >> $sys_myapp_desktop
echo "Categories=Application" >> $sys_myapp_desktop
echo "NoDisplay=True" >> $sys_myapp_desktop

#Add autoloading
#cp $sys_myapp_desktop $HOME/.config/autostart

#Copy desktop file in work folder
cp $sys_myapp_desktop $PWD/wireguard_tray.desktop
chmod +x wireguard_tray.desktop

