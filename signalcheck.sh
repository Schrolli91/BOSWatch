#!/bin/bash
user=root
password=root

count=$(mysql boswatch -u $user -p$password -se "select minute(timediff(now(),time)) as timediff from bos_signal order by time desc limit 1")

if [ $count -gt 10 ] && [ $count -lt 30 ]
then
  logger "Last POCSAG Signal >10min. Restarting Boswatch."
  sudo service boswatch restart
elif [ $count -gt 31 ]
then
  logger "Last POCSAG Signal >30min. Resarting Server."
  sudo shutdown -r now
fi
