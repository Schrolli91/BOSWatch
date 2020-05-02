#!/bin/bash

function exitcodefunction {
  errorcode=$1
  action=$2
  module=$3

  if [ $errorcode -ne "0" ]; then
    echo "Action: $action on $module failed." >> $boswatch_install_path/setup_log.txt
    echo "Exitcode: $errorcode" >> $boswatch_install_path/setup_log.txt
    echo ""
    echo "Action: $action on $module failed."
    echo "Exitcode: $errorcode"
    echo ""
    echo " -> If you want to open an issue at https://github.com/Schrolli91/BOSWatch/issues"
    echo "    please post the logfile, located at $boswatch_install_path/setup_log.txt"
    exit 1
  else
    echo "Action: $action on $module ok." >> $boswatch_install_path/setup_log.txt
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
boswatch_install_path=/opt/boswatch_install
reboot=false
didBackup=false

# Checking for Backup
# check for old version (for the old ones...)
if [ -f $boswatchpath/BOSWatch/boswatch.py ]; then
	echo "Old installation found!"
	echo "A backup will be copied to $boswatchpath/old"

	mkdir /tmp/boswatch
	mv $boswatchpath/BOSWatch/* /tmp/boswatch/
	didBackup=true
fi

#and the future...
if [ -f $boswatchpath/boswatch.py ]; then
	echo "Old installation found!"
	echo "A backup will be copied to $boswatchpath/old"

	mkdir /tmp/boswatch
	mv $boswatchpath/* /tmp/boswatch/
	didBackup=true
fi

# Check for Flags in command line
for (( i=1; i<=$#; i=$i+2 )); do
    t=$((i + 1))
    eval arg=\$$i
    eval arg2=\$$t

    case $arg in
      -r|--reboot) reboot=true ;;

      -b|--branch)
      case $arg2 in
        dev|develop)  echo "       !!! WARNING: you are using the DEV BRANCH !!!       "; branch=dev ;;
        *) branch=master ;;
      esac ;;

      -p|--path)    echo " !!! WARNING: you'll install BOSWATCH to alternative path !!! "; boswatchpath=$arg2 ;;

      *) echo "Internal error!" ; exit 1 ;;
    esac
done

# Create default paths
mkdir -p $boswatchpath
mkdir -p $boswatch_install_path

echo ""

# Update of computer
tput cup 13 15
echo "[ 1/9] [#--------]"
tput cup 15 5
echo "-> make an apt-get update................"
apt-get update -y > $boswatch_install_path/setup_log.txt 2>&1

# download software
tput cup 13 15
echo "[ 2/9] [##-------]"
tput cup 15 5
echo "-> download GIT and other stuff.........."
apt-get -y install git cmake build-essential libusb-1.0 qt4-qmake qt4-default libpulse-dev libx11-dev sox python-pip >> $boswatch_install_path/setup_log.txt 2>&1
exitcodefunction $? download stuff

# download BOSWatch via git
tput cup 13 15
echo "[ 3/9] [###------]"
tput cup 15 5
echo "-> download BOSWatch..................."
cd $boswatchpath/

case $branch in
  "dev") git clone -b develop https://github.com/Schrolli91/BOSWatch . >> $boswatch_install_path/setup_log.txt 2>&1 && \
    exitcodefunction $? git-clone BOSWatch-develop ;;
  "beta") git clone -b beta https://github.com/Schrolli91/BOSWatch . >> $boswatch_install_path/setup_log.txt 2>&1 && \
    exitcodefunction $? git-clone BOSWatch-beta ;;
  *) git clone -b master https://github.com/Schrolli91/BOSWatch . >> $boswatch_install_path/setup_log.txt 2>&1 && \
    exitcodefunction $? git-clone BOSWatch ;;
esac

# Download RTL-SDR
tput cup 13 15
echo "[ 4/9] [####-----]"
tput cup 15 5
echo "-> download rtl_fm......................"
cd $boswatch_install_path
git clone https://github.com/Schrolli91/rtl-sdr.git >> $boswatch_install_path/setup_log.txt 2>&1
exitcodefunction $? git-clone rtl-sdr
cd rtl-sdr/

# Compie RTL-FM
tput cup 13 15
echo "[ 5/9] [#####----]"
tput cup 15 5
echo "-> compile rtl_fm......................"
mkdir -p build && cd build
cmake ../ -DINSTALL_UDEV_RULES=ON >> $boswatch_install_path/setup_log.txt 2>&1
exitcodefunction $? cmake rtl-sdr

make >> $boswatch_install_path/setup_log.txt 2>&1
exitcodefunction $? make rtl-sdr

make install >> $boswatch_install_path/setup_log.txt 2>&1
exitcodefunction $? make-install rtl-sdr

ldconfig >> $boswatch_install_path/setup_log.txt 2>&1
exitcodefunction $? ldconfig rtl-sdr


# Download Multimon-NG
tput cup 13 15
echo "[ 6/9] [######---]"
tput cup 15 5
echo "-> download multimon-ng................"
cd $boswatch_install_path
git clone https://github.com/Schrolli91/multimon-ng.git multimonNG >> $boswatch_install_path/setup_log.txt 2>&1
exitcodefunction $? git-clone multimonNG

cd $boswatch_install_path/multimonNG/

# Compile Multimon-NG
tput cup 13 15
echo "[ 7/9] [#######--]"
tput cup 15 5
echo "-> compile multimon-ng................."
mkdir -p build
cd build
qmake ../multimon-ng.pro >> $boswatch_install_path/setup_log.txt 2>&1
exitcodefunction $? qmake multimonNG

make >> $boswatch_install_path/setup_log.txt 2>&1
exitcodefunction $? make multimonNG

make install >> $boswatch_install_path/setup_log.txt 2>&1
exitcodefunction $? qmakeinstall multimonNG

# Download & Install MySQL-Connector for Python via pip
tput cup 13 15
echo "[ 8/9] [########-]"
tput cup 15 5
echo "-> Download & Install MySQL connector for Python."
cd $boswatch_install_path
pip install mysql-connector-python >> $boswatch_install_path/setup_log.txt 2>&1
exitcodefunction $? install mysql-connector

# Blacklist DVB-Drivers
tput cup 13 15
echo "[9/9] [#########]"
tput cup 15 5
echo "-> configure..........................."
cd $boswatchpath/
chmod +x *
echo $'# BOSWatch - blacklist the DVB drivers to avoid conflicts with the SDR driver\n blacklist dvb_usb_rtl28xxu \n blacklist rtl2830\n blacklist dvb_usb_v2\n blacklist dvb_core' >> /etc/modprobe.d/boswatch_blacklist_sdr.conf

# Installation is ready
tput cup 17 1
echo "BOSWatch is now installed in $boswatchpath/"
echo "Installation ready!"
tput cup 19 3
echo "Watch out: to run BOSWatch you have to modify the config.ini!"
echo "Do the following step to do so:"
echo "sudo nano $boswatchpath/config/config.ini"
echo "and modify the config as you need. This step is optional if you are upgrading an old version of BOSWatch. "

tput cnorm

# cleanup
mkdir $boswatchpath/log/install -p
mv $boswatch_install_path/setup_log.txt $boswatchpath/log/install/
rm $boswatch_install_path/ -R

#copy the template config to run boswatch
cp $boswatchpath/config/config.template.ini $boswatchpath/config/config.ini


#replay the backup
if [ $didBackup = "true" ]; then
	mkdir $boswatchpath/old/
	mv /tmp/boswatch/* $boswatchpath/old/
fi

if [ $reboot = "true" ]; then
  /sbin/reboot
fi
