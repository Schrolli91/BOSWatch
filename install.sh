#!/bin/bash
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

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root!" 1>&2
   exit 1
fi

echo "This may take a several minutes... Don't panic!"
echo ""
echo "Caution, script does not install a webserver with PHP and MySQL"
echo "So you have to make up manually if you want to use MySQL support"

boswatchpath=/opt/boswatch
mkdir -p $boswatchpath
reboot=false

for (( i=1; i<=$#; i=$i+2 )); do
    t=$((i + 1))
    eval arg=\$$i
    eval arg2=\$$t

    case $arg in
      -r|--reboot)
        case $arg2 in
          y|yes) reboot=true ;;
          n|no) reboot=false ;;
          *) echo "Please use y/yes or n/no for reboot" ; exit 1 ;;
        esac ;;

      -b|--branch)
      case $arg2 in
        dev) echo "       !!! WARNING: you are using the DEV BRANCH !!!      "; branch=dev ;;
        *) branch=master ;;
      esac ;;

      *) echo "Internal error!" ; exit 1 ;;
    esac
done

mkdir -p $boswatchpath/install

echo ""

tput cup 13 15
echo "[ 1/10] [#---------]"
tput cup 15 5
echo "-> make an apt-get update................"
apt-get update -y > $boswatchpath/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 2/10] [##--------]"
tput cup 15 5
echo "-> download GIT and other stuff.........."
apt-get -y install git cmake build-essential libusb-1.0 qt4-qmake qt4-default libpulse-dev libx11-dev sox >> $boswatchpath/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 3/10] [###-------]"
tput cup 15 5
echo "-> download rtl_fm......................"
cd $boswatchpath/install
#git clone git://git.osmocom.org/rtl-sdr.git >> $boswatchpath/install/setup_log.txt 2>&1
git https://github.com/Schrolli91/rtl-sdr.git >> $boswatchpath/install/setup_log.txt 2>&1
cd rtl-sdr/

tput cup 13 15
echo "[ 4/10] [####------]"
tput cup 15 5
echo "-> compile rtl_fm......................"
mkdir -p build && cd build
cmake ../ -DINSTALL_UDEV_RULES=ON >> $boswatchpath/install/setup_log.txt 2>&1
make >> $boswatchpath/install/setup_log.txt 2>&1
make install >> $boswatchpath/install/setup_log.txt 2>&1
ldconfig >> $boswatchpath/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 5/10] [#####-----]"
tput cup 15 5
echo "-> download multimon-ng................"
cd $boswatchpath/install
#git clone https://github.com/EliasOenal/multimonNG.git >> $boswatchpath/install/setup_log.txt 2>&1
git clone https://github.com/Schrolli91/multimon-ng.git multimonNG >> $boswatchpath/install/setup_log.txt 2>&1

cd $boswatchpath/install/multimonNG/

tput cup 13 15
echo "[ 6/10] [######----]"
tput cup 15 5
echo "-> compile multimon-ng................."
mkdir -p build
cd build
qmake ../multimon-ng.pro >> $boswatchpath/install/setup_log.txt 2>&1
make >> $boswatchpath/install/setup_log.txt 2>&1
make install >> $boswatchpath/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 7/10] [#######---]"
tput cup 15 5
echo "-> download MySQL connector for Python."
cd $boswatchpath/install
wget "http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-1.0.9.tar.gz/from/http://cdn.mysql.com/" -O mysql-connector.tar >> $boswatchpath/install/setup_log.txt 2>&1
tar xfv mysql-connector.tar >> $boswatchpath/install/setup_log.txt 2>&1
cd $boswatchpath/install/mysql-connector-python*

tput cup 13 15
echo "[ 8/10] [########--]"
tput cup 15 5
echo "-> install MySQL connector for Python.."
chmod +x ./setup.py
./setup.py install >> $boswatchpath/install/setup_log.txt 2>&1

tput cup 13 15
echo "[ 9/10] [#########-]"
tput cup 15 5
echo "-> download BOSWatch..................."
cd $boswatchpath/

case $branch in
  dev) git clone -b develop https://github.com/Schrolli91/BOSWatch >> $boswatchpath/install/setup_log.txt 2>&1 ;;
  *) git clone -b master https://github.com/Schrolli91/BOSWatch >> $boswatchpath/install/setup_log.txt 2>&1 ;;
esac

tput cup 13 15
echo "[10/10] [##########]"
tput cup 15 5
echo "-> configure..........................."
cd $boswatchpath/
chmod +x *
echo $'# BOSWatch - blacklist the DVB drivers to avoid conflict with the SDR driver\n blacklist dvb_usb_rtl28xxu \n blacklist rtl2830\n blacklist dvb_usb_v2\n blacklist dvb_core' >> /etc/modprobe.d/boswatch_blacklist_sdr.conf

tput cup 17 1
echo "BOSWatch is now installed in $boswatchpath/"
echo "Installation ready!"

tput cnorm

if [ $reboot = "true" ]; then
  /sbin/reboot
fi
