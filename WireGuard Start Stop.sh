#!/bin/bash

WG_INTERFACE_NAME="wg0-client"

CLIENT=$(wg show interfaces)

if [ "$CLIENT" == "$WG_INTERFACE_NAME" ]; then
	echo -e "\e[1;33m$WG_INTERFACE_NAME запущен Останавливаю...\e[0m"
	wg-quick down $WG_INTERFACE_NAME
	echo -e "\e[31mВыполнено.\e[0m"
else
	echo -e "\e[1;33mЗапускаю $WG_INTERFACE_NAME\e[0m"
	wg-quick up $WG_INTERFACE_NAME
	sudo wg show
	echo -e "\e[31mВыполнено.\e[0m"
	#Запускаем индикатор.
	nohup python ~/WireGuard_Indicator/wireguard_tray.py &
fi
sleep 1
echo ""
echo -e "\e[1;36mДля закрытия окна, нажмите любую клавишу...\e[0m"

read

if [ -f nohup.out ]; then
    rm nohup.out
fi
