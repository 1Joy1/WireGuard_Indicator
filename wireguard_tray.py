#!/usr/bin/python
# coding: utf8
import os
import gi
import commands
import subprocess
import signal
import sys
import fcntl
import time
import threading, time

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator, Notify as notify, GdkPixbuf as gdkpixbuf
from ConfigParser import SafeConfigParser

CURR_PATH_APP = os.path.dirname(os.path.realpath(__file__))
APP_ID = "wire_guard_tray"
APP_NAME = "Wire Guard tray Indicator"
APP_ICON = CURR_PATH_APP + "/icons/wireguard_icon.png"
APP_VERSION = "1.0"
DESCRIPTION = u"""
Индикатор панели задач для WireGuard.
Позволяет видеть поднят ли в данный момент
сетевой интерфейс тунеля, а так же управлять
запуском и остановкой VPN тунеля.
"""
LICENSE ="""
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject
to the following conditions:
The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE."""



class WGIndicator(object):
    def __init__(self, tunel_interface_name, lock_file, notification):
        self.activ_icon = CURR_PATH_APP + "/icons/wireguard_icon_a.png"
        self.not_activ_icon = CURR_PATH_APP + "/icons/wireguard_icon_na.png"

        self.tunel_interface_name = tunel_interface_name
        self.lock_file = lock_file

        self.notification = notification

        is_tunel_up = self.getTunelState()

        self.menu = self.createMenu(is_tunel_up)

        self.indicator = appindicator.Indicator.new(APP_ID,
            self.getIcon(is_tunel_up),
            appindicator.IndicatorCategory.APPLICATION_STATUS)

        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu)
        self.indicator.set_ordering_index(2154500000)

        self.loop_stoping = False
        self.check_status_loop = threading.Thread(target=self.checkStatusThredingLoop)
        self.check_status_loop.daemon = True
        self.check_status_loop.start()


    def checkStatusThredingLoop(self):
        while not self.loop_stoping:
            self.updateIndicator()
            time.sleep(1)


    def createMenu(self, is_tunel_up):
        menu = gtk.Menu()

        command_start = gtk.MenuItem(u'Запустить VPN')
        command_start.connect('activate', self.startAction)
        command_start.set_sensitive(not is_tunel_up)
        menu.append(command_start)

        command_stop = gtk.MenuItem(u'Остановить VPN')
        command_stop.connect('activate', self.stopAction)
        command_stop.set_sensitive(is_tunel_up)
        menu.append(command_stop)

        command_check = gtk.MenuItem(u'Состояние VPN')
        command_check.connect('activate', self.checkAction)
        menu.append(command_check)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        about = gtk.MenuItem(u"О Программе")
        about.connect("activate", self.aboutAction)
        menu.append(about)

        exittray = gtk.MenuItem(u'Выход')
        exittray.connect('activate', self.quitAction)
        menu.append(exittray)

        menu.show_all()
        return menu


    def startAction(self, source):
        if not self.getTunelState():
            process = subprocess.Popen(['gksudo', 'wg-quick', 'up', self.tunel_interface_name],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
            out, err = process.communicate()
            errcode = process.returncode

            if errcode == 0:
                self.updateIndicator()
                self.showNotifycation(u"Сетевой интерфейс " + self.tunel_interface_name + u" установлен!")
            elif errcode == 255:
                self.showNotifycation(u"Для выполнения этой операции,\n требуется пароль пользователя.")
            else:
                self.showNotifycation(err)


    def stopAction(self, source):
        if self.getTunelState():
            process = subprocess.Popen(['gksudo', 'wg-quick', 'down', self.tunel_interface_name],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
            out, err = process.communicate()
            errcode = process.returncode

            if errcode == 0:
                self.updateIndicator()
                self.showNotifycation(u"Сетевой интерфейс " + self.tunel_interface_name + u" удален!")
            elif errcode == 255:
                self.showNotifycation(u"Для выполнения этой операции,\n требуется пароль пользователя.")
            else:
                self.showNotifycation(err)


    def checkAction(self, source):
        self.showNotifycation(u"Сетевой интерфейс " + self.tunel_interface_name + u" установлен!"
            if self.getTunelState() == True else u"Сетевой интерфейс " + self.tunel_interface_name + u" не поднят!")


    def aboutAction(self, source):
        window = gtk.Window()

        logo = gdkpixbuf.Pixbuf.new_from_file(APP_ICON).scale_simple(48, 48, gdkpixbuf.InterpType.BILINEAR)

        about = gtk.AboutDialog()
        about.set_program_name(APP_NAME)
        about.set_version('Version ' + APP_VERSION)
        about.set_logo(logo)
        about.set_website('https://github.com/1Joy1/WireGuard_Indicator')
        about.set_website_label('Домашняя страница.')
        about.set_authors(['Marshak Igor aka !Joy! https://github.com/1Joy1'])
        about.set_copyright('(c) 2019 Marshak Igor aka !Joy!')
        about.set_comments(DESCRIPTION)
        about.set_license(LICENSE)
        about.set_transient_for(window)
        about.set_keep_above(True)

        about.run()
        about.destroy()


    def quitAction(self, source):
        self.loop_stoping = True
        if self.getTunelState():
            process = subprocess.Popen(['gksudo', 'wg-quick', 'down', self.tunel_interface_name],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
            out, err = process.communicate()
            errcode = process.returncode

            if errcode == 0:
                self.showNotifycation(u"Сетевой интерфейс " + self.tunel_interface_name + u" удален!")
            else:
                self.showNotifycation(u"Выход без разрыва соединения.")

        notify.uninit()
        gtk.main_quit()
        self.lock_file.remove()


    def showNotifycation(self, body):
        self.notification.update("<b>WireGuard VPN</b>", body, APP_ICON)
        self.notification.set_timeout(3)
        self.notification.show()


    def getTunelState(self):
        return commands.getoutput("wg show interfaces") == self.tunel_interface_name


    def getIcon(self, is_tunel_up):
        return self.activ_icon if is_tunel_up else self.not_activ_icon


    def updateIndicator(self):
        is_tunel_up = self.getTunelState()

        self.indicator.set_icon(self.getIcon(is_tunel_up))

        self.menu.get_children()[0].set_sensitive(not is_tunel_up)
        self.menu.get_children()[1].set_sensitive(is_tunel_up)




class LockFile(object):
    def __init__(self, interface_name):
        self.interface_name = interface_name
        self.lock_file_path = CURR_PATH_APP + "/" + self.interface_name + ".lock"
        self.locked_file = None


    def create(self):
        self.locked_file = open(self.lock_file_path, "a")
        try:
            fcntl.flock(self.locked_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except:
            sys.exit(0)


    def remove(self):
        if os.path.isfile(self.lock_file_path):
            os.remove(self.lock_file_path)




class Config(object):
    def __init__(self, notification):
        self.file_name_config = "wireguard_tray.conf"
        self.config_file_path = CURR_PATH_APP + "/" + self.file_name_config
        self.notification = notification
        self.cfgParser = SafeConfigParser();


    def load(self):
        if not os.path.isfile(self.config_file_path):
            self.showNotifycation(u"Отсутствует файл " + self.file_name_config + u"\nПриложение будет закрыто!")
            sys.exit(0)
        self.cfgParser.read(self.config_file_path)
        try:
            config_interface_name = self.cfgParser.get('wire_guard_indicator_settings','interface_name')
        except:
            self.showNotifycation(u"В конфиге, отсутствует секция [wire_guard_indicator_settings]\nили параметр interface_name.\nПриложение будет закрыто!")
            sys.exit(0)
        self.checkConfig(config_interface_name)
        return config_interface_name


    def checkConfig(self, config_interface_name):
        if not os.path.isfile("/etc/wireguard/" + config_interface_name + ".conf"):
            self.showNotifycation(u"Имя интерфейса в настройках, не соответствует конфиг файлу в\n /etc/wireguard/\nПриложение будет закрыто!")
            sys.exit(0)


    def showNotifycation(self, body):
        self.notification.update("<b>WireGuard VPN</b>", body, APP_ICON)
        self.notification.set_timeout(3)
        self.notification.show()




if __name__=='__main__':
    notify.init(APP_ID)
    notification = notify.Notification.new("<b>WireGuard VPN</b>", APP_NAME + " - Запущен!", APP_ICON)
    notification.show()

    config = Config(notification)
    interface_name = config.load()

    lock_file = LockFile(interface_name)
    lock_file.create()

    WGIndicator(interface_name, lock_file, notification)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    gtk.main()