#!/bin/bash

CLIENT=$(wg show interfaces)

if [ "$CLIENT" == "wg0-client" ]; then
	echo -e "\e[1;33mwg0-client запущен Останавливаю...\e[0m"
	wg-quick down wg0-client
	echo -e "\e[31mВыполнено.\e[0m"
else 
	echo -e "\e[1;33mЗапускаю wg0-client\e[0m"
	wg-quick up wg0-client
	sudo wg show
	echo -e "\e[31mВыполнено.\e[0m"
	#Запускаем индикатор.
	nohup python ~/WireGuard_Indicator/wireguard_tray.py &
fi
sleep 1
echo ""
echo -e "\e[1;36mДля закрытия окна, нажмите любую клавишу...\e[0m"

read
rm nohup.out
