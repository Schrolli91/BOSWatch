#!/bin/bash
bospath=/opt/boswatch/BOSWatch/
echo $module
# ----------------------------------------------------------------------------------------------------------------------------------
#                                                        base Tests
# ----------------------------------------------------------------------------------------------------------------------------------
if [ $module == "base" ]; then
  cp $bospath/config/config.template.ini $bospath/config/config.ini
  sudo /usr/bin/python $bospath/boswatch.py -f 1 -d 0 -e 10 -a POC512 POC1200 POC2400 -v -t
  boserror=$(sudo cat $bospath/log/boswatch.log | grep -i ERROR)

  sudo chmod 777 $bospath/log/boswatch.log
  if grep -Fxq '\[ERROR' "$bospath/log/boswatch.log"
  then
    echo "Found Error in boswatch.log"
    exit 1
  fi


# ----------------------------------------------------------------------------------------------------------------------------------
#                                                        mysql Tests
# ----------------------------------------------------------------------------------------------------------------------------------
elif [ $module == "mysql" ]; then
  sudo cp citest/config.mysql.ini $bospath/config/config.ini
  export DEBIAN_FRONTEND=noninteractive
  sudo -E apt-get -q -y install mysql-server
  sudo service mysql start

  sudo mysql -e "create database boswatch;"
  sudo mysql boswatch < plugins/MySQL/boswatch.sql

  sudo /usr/bin/python $bospath/boswatch.py -f 1 -d 0 -e 10 -a POC512 POC1200 POC2400 -v -t
  sudo chmod 777 $bospath/log/boswatch.log

  if grep -Fxq '\[ERROR' "$bospath/log/boswatch.log"
  then
    echo "Found Error in boswatch.log"
    exit 1
  fi

  fms=$(mysql -s -N -u boswatch -proot boswatch -e "SELECT COUNT(*) FROM bos_fms;")
  mysql  -s -N -u boswatch -proot boswatch -e "SELECT COUNT(*) FROM bos_fms;"
  if [ "$fms" == "0" ]; then
   echo "FMS Table emtpy"
   exit 1
  fi


  zvei=$(mysql -s -N -u boswatch -proot boswatch -e "SELECT COUNT(*) FROM bos_zvei;")
  mysql  -s -N -u boswatch -proot boswatch -e "SELECT COUNT(*) FROM bos_zvei;"
  if [ "$zvei" == "0" ]; then
   echo "ZVEI Table emtpy"
   exit 1
  fi


  pocsag=$(mysql -s -N -u boswatch -proot boswatch -e "SELECT COUNT(*) FROM bos_pocsag;")
  mysql  -s -N -u boswatch -proot boswatch -e "SELECT COUNT(*) FROM bos_pocsag;"
  if [ "$pocsag" == "0" ]; then
   echo "POCSAG Table emtpy"
   exit 1
  fi


# ----------------------------------------------------------------------------------------------------------------------------------
#                                                        httpRequest Tests
# ----------------------------------------------------------------------------------------------------------------------------------
elif [ $module == "httpRequest" ]; then
  sudo cp citest/config.httpRequest.ini $bospath/config/config.ini
  sudo /usr/bin/python $bospath/boswatch.py -f 1 -d 0 -e 10 -a POC512 POC1200 POC2400 -v -t

  sudo chmod 777 $bospath/log/boswatch.log
  if grep -Fxq '\[ERROR' "$bospath/log/boswatch.log"
  then
    echo "Found Error in boswatch.log"
    exit 1
  fi
fi
