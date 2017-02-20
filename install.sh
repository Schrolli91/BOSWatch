#!/bin/bash

function exitcodefunction {
  errorcode=$1
  action=$2
  module=$3

  if [ $errorcode -ne "0" ]; then
    echo "Action: $action on $module failed."
    echo "Exitcode: $errorcode"
    exit 1
  else
    echo "Action: $action on $module ok."
  fi
 }


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

echo "This may take several minutes... Don't panic!"
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
        dev|develop) echo "       !!! WARNING: you are using the DEV BRANCH !!!      "; branch=dev ;;
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
exitcodefunction $? download stuff

tput cup 13 15
echo "[ 3/10] [###-------]"
tput cup 15 5
echo "-> download rtl_fm......................"
cd $boswatchpath/install
git clone https://github.com/Schrolli91/rtl-sdr.git >> $boswatchpath/install/setup_log.txt 2>&1
exitcodefunction $? git-clone rtl-sdr
cd rtl-sdr/

tput cup 13 15
echo "[ 4/10] [####------]"
tput cup 15 5
echo "-> compile rtl_fm......................"
mkdir -p build && cd build
cmake ../ -DINSTALL_UDEV_RULES=ON >> $boswatchpath/install/setup_log.txt 2>&1
exitcodefunction $? cmake rtl-sdr

make >> $boswatchpath/install/setup_log.txt 2>&1
exitcodefunction $? make rtl-sdr

make install >> $boswatchpath/install/setup_log.txt 2>&1
exitcodefunction $? make-install rtl-sdr

ldconfig >> $boswatchpath/install/setup_log.txt 2>&1
exitcodefunction $? ldconfig rtl-sdr



tput cup 13 15
echo "[ 5/10] [#####-----]"
tput cup 15 5
echo "-> download multimon-ng................"
cd $boswatchpath/install
git clone https://github.com/Schrolli91/multimon-ng.git multimonNG >> $boswatchpath/install/setup_log.txt 2>&1
exitcodefunction $? git-clone multimonNG


cd $boswatchpath/install/multimonNG/

tput cup 13 15
echo "[ 6/10] [######----]"
tput cup 15 5
echo "-> compile multimon-ng................."
mkdir -p build
cd build
qmake ../multimon-ng.pro >> $boswatchpath/install/setup_log.txt 2>&1
exitcodefunction $? qmake multimonNG

make >> $boswatchpath/install/setup_log.txt 2>&1
exitcodefunction $? make multimonNG


make install >> $boswatchpath/install/setup_log.txt 2>&1
exitcodefunction $? qmakeinstall multimonNG


tput cup 13 15
echo "[ 7/10] [#######---]"
tput cup 15 5
echo "-> download MySQL connector for Python."
cd $boswatchpath/install
wget "http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-1.0.9.tar.gz/from/http://cdn.mysql.com/" -O mysql-connector.tar >> $boswatchpath/install/setup_log.txt 2>&1
exitcodefunction $? download mysql-connector

tar xfv mysql-connector.tar >> $boswatchpath/install/setup_log.txt 2>&1
exitcodefunction $? untar mysql-connector

cd $boswatchpath/install/mysql-connector-python*

tput cup 13 15
echo "[ 8/10] [########--]"
tput cup 15 5
echo "-> install MySQL connector for Python.."
chmod +x ./setup.py
./setup.py install >> $boswatchpath/install/setup_log.txt 2>&1
exitcodefunction $? setup mysql-connector


tput cup 13 15
echo "[ 9/10] [#########-]"
tput cup 15 5
echo "-> download BOSWatch..................."
cd $boswatchpath/

case $branch in
  "dev") git clone -b develop https://github.com/Schrolli91/BOSWatch >> $boswatchpath/install/setup_log.txt 2>&1 && \
    exitcodefunction $? git-clone BOSWatch-develop ;;
  *) git clone -b master https://github.com/Schrolli91/BOSWatch >> $boswatchpath/install/setup_log.txt 2>&1 && \
    exitcodefunction $? git-clone BOSWatch ;;
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
tput cup 19 3
echo "Watch out: to run BOSWatch you have to generate and modify the config.ini!"
echo "Do the following steps to have a running version of BOSWatch:"
echo "sudo cp $boswatchpath/BOSWatch/config/config.template.ini $boswatchpath/BOSWatch/config/config.ini"
echo "sudo nano $boswatchpath/BOSWatch/config/config.ini"
echo "and modify the config as you need. This step is optional if you are upgrading an old version of BOSWatch. "

tput cnorm

# cleanup
mkdir $boswatchpath/log/install -p
mv $boswatchpath/install/setup_log.txt $boswatchpath/log/install/
rm $boswatchpath/install/ -R

mv $boswatchpath/BOSWatch/* $boswatchpath/
rm $boswatchpath/BOSWatch -R

if [ $reboot = "true" ]; then
  /sbin/reboot
fi
