# skymeter
Exede satellite internet usage monitor Raspberry Pi appliance


Example root crontab file (edit with 'sudo su' then 'crontab -e')

@reboot /root/heartbeat.sh

@reboot /home/pi/skymeter/usage_display.sh

0 3 * * * /home/pi/skymeter/usage_updater.sh
