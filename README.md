# WireGuard Indicator

**Unity Taskbar indicator for WireGuard.**  
Allows you to see whether it is currently raised tunnel network interface as well as start and stop the VPN interface.

Up/down interface is controlled by the **wg-quick** utility (required install).  
It is required to create a config file for **wg-quick** along the route  
***/etc/wireguard/NAME_INTERFACE.conf***  
and check the operation using the commands  
`wg-quick up NAME_INTERFACE`  
and  
`wg-quick down NAME_INTERFACE`  

After that, clone the repository in your home directory.
To create launch shortcuts, run **install.sh**  
Edit ***wireguard_tray.conf*** in work folder, set the name of the interface to control.

    [wire_guard_indicator_settings]
    interface_name = NAME_INTERFACE

------------

**Индикатор панели задач Unity для WireGuard.**  
Позволяет увидеть, подключен ли в данный момент туннельный сетевой интерфейс, а также запустить и остановить VPN интерфейс.

Запуск и остановка интерфейса, происходит с помощью утилиты **wg-quick** (требуется установка).  
Необходимо создать файл конфигурации для **wg-quick** по маршруту  
***/etc/wireguard/ИМЯ_ИНТЕРФЕЙСА.conf***  
и проверить его работу с помощью команд  
`wg-quick up ИМЯ_ИНТЕРФЕЙСА`  
и  
`wg-quick down ИМЯ_ИНТЕРФЕЙСА`  

После этого, склонируйте репозиторий в ваш домашний каталог.
Для создания ярлыков запуска, запустите **install.sh**  
Отредактируйте ***wireguard_tray.conf*** в рабочей директории, укажите имя интерфейса для управления.

    [wire_guard_indicator_settings]
    interface_name = ИМЯ_ИНТЕРФЕЙСА

------------

**Зависимости / Dependence**  
Python 2.7  
**module:**  
os, gi, commands, subprocess, signal, sys, fcntl, time, threading, time, ConfigParser
