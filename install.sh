#!/bin/sh
tput clear
tput civis
echo "     ____  ____  ______       __      __       __   "
echo "    / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_  "
echo "   / __  / / / /\__ \| | /| / / __  / __/ ___/ __ \ "
echo "  / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / / "
echo " /_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/  "
echo "            German BOS Information Script           "
echo "                 by Bastian Schroll                 "
echo ""
echo "This may take several minutes... Don't panic!"
echo ""
echo "Caution, the script doesn't install a Webserver with PHP and MySQL"
echo "so you have to install it later manually if you want to use the MySQL features"

mkdir -p ~/boswatch/install

tput cup 13 15
echo "[ 1/10] [#---------]"
tput cup 15 5
echo "-> refreshing package versions............."
apt-get update -y > ~/boswatch/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 2/10] [##--------]"
tput cup 15 5
echo "-> downloading GIT and other stuff.........."
apt-get -y install git cmake build-essential libusb-1.0 qt4-qmake libpulse-dev libx11-dev sox >> ~/boswatch/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 3/10] [###-------]"
tput cup 15 5
echo "-> downloading rtl_fm......................"
cd ~/boswatch/install
git clone git://git.osmocom.org/rtl-sdr.git >> ~/boswatch/install/setup_log.txt 2>&1
cd rtl-sdr/

tput cup 13 15
echo "[ 4/10] [####------]"
tput cup 15 5
echo "-> compiling rtl_fm........................"
mkdir -p build && cd build
cmake ../ -DINSTALL_UDEV_RULES=ON >> ~/boswatch/install/setup_log.txt 2>&1
make >> ~/boswatch/install/setup_log.txt 2>&1
make install >> ~/boswatch/install/setup_log.txt 2>&1
ldconfig >> ~/boswatch/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 5/10] [#####-----]"
tput cup 15 5
echo "-> downloading multimon-ng................"
cd ~/boswatch/install
git clone https://github.com/EliasOenal/multimonNG.git >> ~/boswatch/install/setup_log.txt 2>&1
cd multimonNG/

tput cup 13 15
echo "[ 6/10] [######----]"
tput cup 15 5
echo "-> compiling multimon-ng................."
mkdir -p build
cd build
qmake ../multimon-ng.pro >> ~/boswatch/install/setup_log.txt 2>&1
make >> ~/boswatch/install/setup_log.txt 2>&1
make install >> ~/boswatch/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 7/10] [#######---]"
tput cup 15 5
echo "-> downloading the MySQL Connector for Python."
cd ~/boswatch/install
wget "http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-1.0.9.tar.gz/from/http://cdn.mysql.com/" -O mysql-connector.tar >> ~/boswatch/install/setup_log.txt 2>&1
tar xfv mysql-connector.tar >> ~/boswatch/install/setup_log.txt 2>&1
cd mysql-connector-python*

tput cup 13 15
echo "[ 8/10] [########--]"
tput cup 15 5
echo "-> installing the MySQL Connector for Python.."
chmod +x ./setup.py
./setup.py install >> ~/boswatch/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 9/10] [#########-]"
tput cup 15 5
echo "-> downloading BOSWatch from GitHub.........."
cd ~/boswatch
git clone https://github.com/Schrolli91/BOSWatch >> ~/boswatch/install/setup_log.txt 2>&1

tput cup 13 15
echo "[10/10] [##########]"
tput cup 15 5
echo "-> Configuring BOSWatch................"
cd ~/boswatch
chmod +x *
echo "# BOSWatch - blacklist the DVB drivers to avoid conflict with the SDR driver\n blacklist dvb_usb_rtl28xxu \n blacklist rtl2830\n blacklist dvb_usb_v2\n blacklist dvb_core" >> /etc/modprobe.d/boswatch_blacklist_sdr.conf

tput cup 17 1
echo "BOSWatch is now installed in ~/boswatch/"
echo "Installation finished!"
