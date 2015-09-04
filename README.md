# skymeter

This code powers a Raspberry Pi appliance that acts as an Exede satellite internet usage monitor 
- Data usage is displayed to a 128x64 OLED screen (SSD1306)
- The device auto-updates the data usage information once per day (as dictated by the crontab)

TODO: 
- Handle password changes gracefully
- Auto-update code from remote source
- Periodic health report emails to an administrator

Example root crontab file (edit with 'sudo su' then 'crontab -e')
@reboot /home/pi/skymeter/usage_display.sh
0 3 * * * /home/pi/skymeter/usage_updater.sh
