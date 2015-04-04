#!/bin/sh
clear
echo ""
echo "        ##########################"
echo "        #                        #"
echo "        #   BOSWatch Installer   #"
echo "        #                        #"
echo "        ##########################"
echo ""
echo "This may take a several minutes... Don't panic!"
echo ""
echo "Caution, script don't installed a Webserver with PHP and MySQL"
echo "So you have to make up manually if you want to use MySQL support"
echo ""

mkdir -p /home/pi/bos/install 

echo "[ 1/10] [#---------] make a apt-get update..."
apt-get update > /home/pi/bos/install/setup_log.txt 2>&1

echo "[ 2/10] [##--------] download GIT an other stuff..."
apt-get -y install git cmake build-essential libusb-1.0 qt4-qmake libpulse-dev libx11-dev sox >> /home/pi/bos/install/setup_log.txt 2>&1

echo "[ 3/10] [###-------] download rtl_fm..."
cd /home/pi/bos/install 
git clone git://git.osmocom.org/rtl-sdr.git >> /home/pi/bos/install/setup_log.txt 2>&1
cd rtl-sdr/

echo "[ 4/10] [####------] compile rtl_fm..."
mkdir -p build && cd build
cmake ../ -DINSTALL_UDEV_RULES=ON >> /home/pi/bos/install/setup_log.txt 2>&1
make >> /home/pi/bos/install/setup_log.txt 2>&1
make install >> /home/pi/bos/install/setup_log.txt 2>&1
ldconfig >> /home/pi/bos/install/setup_log.txt 2>&1

echo "[ 5/10] [#####-----] download multimon-ng..."
cd /home/pi/bos/install 
git clone https://github.com/EliasOenal/multimonNG.git >> /home/pi/bos/install/setup_log.txt 2>&1
cd multimonNG/

echo "[ 6/10] [######----] compile multimon-ng..."
mkdir -p build
cd build
qmake ../multimon-ng.pro >> /home/pi/bos/install/setup_log.txt 2>&1
make >> /home/pi/bos/install/setup_log.txt 2>&1
make install >> /home/pi/bos/install/setup_log.txt 2>&1

echo "[ 7/10] [#######---] download MySQL Connector for Python..."
cd /home/pi/bos/install 
wget "http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-1.0.9.tar.gz/from/http://cdn.mysql.com/" -O mysql-connector.tar >> /home/pi/bos/install/setup_log.txt 2>&1
tar xfv mysql-connector.tar >> /home/pi/bos/install/setup_log.txt 2>&1
cd mysql-connector-python*

echo "[ 8/10] [########--] install MySQL Connector for Python..."
chmod +x ./setup.py
./setup.py install >> /home/pi/bos/install/setup_log.txt 2>&1

echo "[ 9/10] [#########-] download BOSWatch..."
cd /home/pi/bos
git clone https://github.com/Schrolli91/BOSWatch >> /home/pi/bos/install/setup_log.txt 2>&1

echo "[10/10] [##########] configure..."
cd BOSWatch
chmod +x *
echo "# blacklist the DVB drivers to avoid conflict with the SDR driver\n blacklist dvb_usb_rtl28xxu \n blacklist rtl2830\n blacklist dvb_usb_v2\n blacklist dvb_core" >> /etc/modprobe.d/boswatch_blacklist_sdr.conf

echo ""
echo "BOSWatch are now in /home/pi/bos/BOSWatch/"
echo "Install ready!"
