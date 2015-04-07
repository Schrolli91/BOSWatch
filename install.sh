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
echo "This may take a several minutes... Don't panic!"
echo ""
echo "Caution, script don't install a Webserver with PHP and MySQL"
echo "So you have to make up manually if you want to use MySQL support"

mkdir -p ~/bos/install 

tput cup 13 15
echo "[ 1/10] [#---------]"
tput cup 15 5
echo "-> make a apt-get update................"
apt-get update > ~/bos/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 2/10] [##--------]"
tput cup 15 5
echo "-> download GIT an other stuff.........."
apt-get -y install git cmake build-essential libusb-1.0 qt4-qmake libpulse-dev libx11-dev sox >> ~/bos/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 3/10] [###-------]"
tput cup 15 5
echo "-> download rtl_fm......................"
cd ~/bos/install 
git clone git://git.osmocom.org/rtl-sdr.git >> ~/bos/install/setup_log.txt 2>&1
cd rtl-sdr/

tput cup 13 15
echo "[ 4/10] [####------]"
tput cup 15 5
echo "-> compile rtl_fm......................"
mkdir -p build && cd build
cmake ../ -DINSTALL_UDEV_RULES=ON >> ~/bos/install/setup_log.txt 2>&1
make >> ~/bos/install/setup_log.txt 2>&1
make install >> ~/bos/install/setup_log.txt 2>&1
ldconfig >> ~/bos/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 5/10] [#####-----]"
tput cup 15 5
echo "-> download multimon-ng................"
cd ~/bos/install 
git clone https://github.com/EliasOenal/multimonNG.git >> ~/bos/install/setup_log.txt 2>&1
cd multimonNG/

tput cup 13 15
echo "[ 6/10] [######----]"
tput cup 15 5
echo "-> compile multimon-ng................."
mkdir -p build
cd build
qmake ../multimon-ng.pro >> ~/bos/install/setup_log.txt 2>&1
make >> ~/bos/install/setup_log.txt 2>&1
make install >> ~/bos/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 7/10] [#######---]"
tput cup 15 5
echo "-> download MySQL Connector for Python."
cd ~/bos/install 
wget "http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-1.0.9.tar.gz/from/http://cdn.mysql.com/" -O mysql-connector.tar >> ~/bos/install/setup_log.txt 2>&1
tar xfv mysql-connector.tar >> ~/bos/install/setup_log.txt 2>&1
cd mysql-connector-python*

tput cup 13 15
echo "[ 8/10] [########--]"
tput cup 15 5
echo "-> install MySQL Connector for Python.."
chmod +x ./setup.py
./setup.py install >> ~/bos/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 9/10] [#########-]"
tput cup 15 5
echo "-> download BOSWatch..................."
cd ~/bos
git clone https://github.com/Schrolli91/BOSWatch >> ~/bos/install/setup_log.txt 2>&1

tput cup 13 15
echo "[10/10] [##########]"
tput cup 15 5
echo "-> configure..........................."
cd BOSWatch
chmod +x *
echo "# blacklist the DVB drivers to avoid conflict with the SDR driver\n blacklist dvb_usb_rtl28xxu \n blacklist rtl2830\n blacklist dvb_usb_v2\n blacklist dvb_core" >> /etc/modprobe.d/boswatch_blacklist_sdr.conf

tput cup 17 1
echo "BOSWatch are now in ~/bos/BOSWatch/"
echo "Install ready!"