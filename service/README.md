### Use BOSWatch as service ###

Old description below

We assume that BOSWatch is installed to /opt/boswatch! Otherwise you need to adapt all the pathes in this description and in the service-file itself.

#### Adapt the script
Enter the frequency and the decoder(s) you want to use in line 7; you can add more specific switches if you need to

### Install the service
1. Use the install-script install_service.sh as sudo: `sudo bash install_service.sh` (self explaining)

OR

1. Copy the file to /etc/systemd/system: sudo cp /opt/boswatch/service/boswatch.service /etc/systemd/system/
2. Enable the service: sudo systemctl enable boswatch.service
3. Start the service: sudo systemctl start boswatch.service
4. Check the status: sudo systemctl status boswatch.service

---

### Start BOSWatch as a daemon

##### Changing the init script

Lines 14 and 15 define where to find the Python script.
In this case the script expects that there is a folder `/usr/local/bin/BOSWatch` and that the script is inside there.

Line 23 sets what user to run the script as. Using a root-user is necessary for BOSWatch.

Line 19 sets the parameters for BOSWatch, use the same as starting BOSWatch from the shell.
We recommend to use "-u" and "-q" when you want to run BOSWatch as a daemon.
- "-u": You will find the logfiles in `/var/log/BOSWatch`
- "-q": Shows no information. Only logfiles

##### Using the init script

To actually use this script, put BOSWatch where you want (recommend `/usr/local/bin/BOSWatch`)
and make sure it is executable (e.g. `sudo chmod 755 boswatch.py`).
Edit the init script accordingly. Copy it into /etc/init.d using e.g. `sudo cp boswatch.sh /etc/init.d`.
Make sure the script is executable (chmod again) and make sure that it has UNIX line-endings.
After creating this new daemon it's neccessary to do a `sudo systemctl daemon-reload` in order to make it findable.

At this point you should be able to start BOSWatchcd ~/srt using the command `sudo /etc/init.d/boswatch.sh start`,
check its status with the `sudo /etc/init.d/boswatch.sh status` argument and stop it with `sudo /etc/init.d/boswatch.sh stop`.

To make the Raspberry Pi use your init script at the right time, one more step is required:
Running the command `sudo update-rc.d boswatch.sh defaults`.
This command adds in symbolic links to the /etc/rc.x directories so that the init script is run at the default times.
You can see these links if you do `ls -l /etc/rc?.d/*boswatch.sh`
