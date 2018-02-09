# <center>Raspberry Pi 2/3 + solarpi note</center>



## 1.Official image
how to install NOOBS on linux:  
http://qdosmsq.dunbar-it.co.uk/blog/2013/06/noobs-for-raspberry-pi/  
 * download NOOBS 
 * fdisk split sdcard
 * mkfs.vfat format sdcard
 * unzip to sdcard


## 2.System configuration(language/time-zone/keyboard/Serial/SSH/I2C)
`sudo raspi-config`  
or  
GUI Desktop, Menu/Preferences/Raspberry Pi Configuration  


## 3.system update
`sudo apt-get update`  
`sudo apt-get upgrade`  
`sudo apt-get dist-upgrade`  

by the way, install the vim, for habit: `sudo apt-get install vim`


## 4.Network configuration(3g)
refer below links：
 - [RPi VerifiedPeripherals](http://elinux.org/RPi_VerifiedPeripherals)    
 - [Dlink dwm-156](https://www.raspberrypi.org/forums/viewtopic.php?t=50380&p=390538)  
 - [HwaWei E220](http://raspberry-at-home.com/installing-3g-modem/)  
 - [rpi official teaching for 3g installation](http://www.raspberrypi.com.tw/tutorial/basic/)  

concept: 3 g 3 pecedule  
    1. usb identification  
    2. modeswitch: install modeswitch and config it  
    3. dial: install wvdial and config it  
  
confirm the system have updated: `sudo apt-get update`  
insert 3g-usb-dongle, use instruction `lsusb` and `dmesg` to observe the mount stat (default is virtial Disk)  
udev + modeswitch will convert the virtual disk to usb-modem: `sudo apt-get install usb-modeswitch`  
`/lib/udev/rules.d/*` it's the rule document of udev, add the device rule of the network interface card to udev, filename: `40-usb_modeswitch.rules`  

	# xxxx
	ATTRS{idVendor}=="xxxx", ATTRS{idProduct}=="xxxx", RUN+="usb_modeswitch '%b/%k'"

`/etc/usb_modeswitch.conf` modeswitch configuration file  

	DefaultVendor=xxxx
	DefaultProduct=xxxx

	TargetVendor=yyyy
	TargetProduct=yyyy

	MessageContent="5553424312345678000000000000061e000000000000000000000000000000"

xxxx, get from `lsusb`  
yyyy, get from google, ex:  
[here](http://www.draisberghof.de/usb_modeswitch/device_reference.txt)  
[github](https://github.com/Distrotech/usb-modeswitch-data/blob/master/40-usb_modeswitch.rules)  

confirm the mode switch whether success: `ls /dev/tty*`  
before mode swithch **/dev/ttyAMA0**, **/dev/ttyprintk**  
after mode switch **/dev/ttyUSB0**, **/dev/ttyUSB1**, **/dev/ttyUSB2**  

there are 2 kind dial program: sakis3g / wvdial, here use wvdial  
install `sudo apt-get install wvdial` will install ppp together  
edit wvdial configuration file: `/etc/wvdial.conf`  

	[Dialer E1820]
	Phone = *99#
	APN = internet
	Username = username
	Password = password
	Init1 = ATZ
	Init2 = ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0
	Init3 = AT+CGDCONT=1, "IP","Internet"
	Modem = /dev/ttyUSB0
	Baud = 460800
	Stupid Mode = 1

dial instruction: `sudo wvdial xxxx`  

after link success, it will radom offline, use **crontab + re-connect script** to solve this problem  

## 5.RTC(i2c)
[rpi+rtc](http://yehnan.blogspot.tw/2014/01/raspberry-pirtc.html)  
[Adding a Real Time Clock to your Raspberry Pi](http://thepihut.com/blogs/raspberry-pi-tutorials/17209332-adding-a-real-time-clock-to-your-raspberry-pi)  

watch current system time: `date`  

**raspi-config to enable i2c**, after enable, system will generate i2c-1 link in /sys/class/i2c-adapter/ (rpi2)  
`$ sudo apt-get install python-smbus i2c-tools`  

insert module manual  
`$ sudo modprobe i2c-bcm2708`  
`$ sudo modprobe i2c-dev`  
`$ sudo modprobe rtc-ds1307`

pull up the arthority  
`sudo bash`   
write the configuration(only for rpi2)  
`echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device`   
`exit`   

adjust time and date: query time of rtc, query system time, write time to rtc  
`sudo hwclock -r`    
`date`    
`sudo hwclock -w`   
`sudo hwclock -r`    

## 6.Autorun after boot
create *.desktop file in `~/.config/autostart/runjava.desktop`  

	[Desktop Entry]  
	Name=runjava  
	Exec=/home/pi/solarpi/bin/runjava.sh  
	Type=Application  

excute directory is upper the `*.jar` directory, so make `*.sh` in `~/solarpi/bin/runjava.sh`  

	cd /home/pi/solarpi/bin
	java -jar dist/SolarPi.jar



shell script **DO NOT forget** the first line: **`#!/bin/bash`**

```
  1 #!/bin/bash
  2 output=`ps aux|grep SolarPi|grep -v "grep"`
  3 set -- $output
  4 pid=$2
  5 echo $pid
  6 if [ "$pid" == "" ]; then
  7     echo "SolarPi not running, excute it."
  8     cd /home/pi/solarpi/bin
  9     java -jar dist/SolarPi.jar
 10 fi
```

addition:(not all tested)  
basically autostart have several ways:
 * autostart after login, via `~/.bashrc`  
 * autostart after console, via `/etc/init.d/`  
 * autostart after lxde, via `~/.config/lxsession/LXDE-pi/autostart`  
 * autostart after lxde, via `~/.config/autostart/xx.desktop`  
ref:   
[lxde wiki](https://wiki.lxde.org/en/Autostart)  
[forum](http://raspberrypi.stackexchange.com/questions/8734/execute-script-on-start-up/8735#8735)  

## 7.Disconnection detect (crontab + repppoe)
`crontab -l #list`  
`crontab -e #edit`    
`crontab -r #remove`    

repppse script:  

	#!/bin/bash
	PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
	export PATH
	strdate=$(date)
	echo $strdate
	testing=$(ifconfig | grep "ppp0 ")
	if [ "$testing" != "" ] ; then
		strdate=$(date)
		echo "running"
	else
		echo "not running"
		sudo wvdial E173
	fi

	linktest=$(ping -c 3 8.8.8.8 | grep "time=")
	if [ "$linktest" != "" ]; then
		echo "linking."
	else
		echo "not linking."
	fi
	exit 0


set the editor when using `crontab -e`  
using command: `sudo update-alternatives --config editor` and follow the prompt.

    pi@raspberrypi ~ $ sudo update-alternatives --config editor
    There are 4 choices for the alternative editor (providing /usr/bin/editor).

      Selection    Path                Priority   Status
    ------------------------------------------------------------
    * 0            /bin/nano            40        auto mode
      1            /bin/ed             -100       manual mode
      2            /bin/nano            40        manual mode
      3            /usr/bin/vim.basic   30        manual mode
      4            /usr/bin/vim.tiny    10        manual mode

    Press enter to keep the current choice[*], or type selection number: 3
    update-alternatives: using /usr/bin/vim.basic to provide /usr/bin/editor (editor) in manual mode


## 8.Java low-level driver library(Pi4J)
follow the official webside(pi4j.com) Installation guide  
`curl -s get.pi4j.com | sudo bash`  


## 9.Chinese language  
`sudo apt-get -y install tty-wqy-zenhei`  


# <center>Others</center>


### vim configuration file: `~/.vimrc`  
    set encoding=utf-8
    set fileencodings=utf-8,cp950
    set nocompatible
    syntax on
    set number
    set expandtab
    set shiftwidth=4
    set tabstop=4
    set hlsearch
    set incsearch
    set ic

    "colorscheme torte
    colorscheme desert


### query the timestamp of system reboot  
`cat /var/log/syslog | grep shutdown`  


vsftpd  

bash configuration file: ~/.bashrc  
vim configuration file: add `~/.vimrc` in home directory  
wavemon: monitor tool for wifi network interface card, signal strength, packege statistics, device setting, network configuration.    
cmatrix: The Matrix(movie)  
retext: Markdown editor  
screen: multi-windows in terminal
    - ctrl-a + a : switch between 2 windows
    - ctrl-a + c : create new window
    - ctrl-a + n : next window
    - ctrl-a + p : previous window
    - ctrl-a + w : list opened windows  


### minicom  
`sudo apt-get intall minicom`  
`sudo minicom -s`: setting serial port  
`ctrl-A + Z`: help  
`ctrl-A + Z + C`: clear  
`ctrl-A + Z + S`: send file  


### terminal on windows: MobaXterm
[MobaXterm teach](http://ruten-proteus.blogspot.tw/2013/01/windows-raspberry-pi_31.html?view=classic)


### ntp
`sudo apt-get install ntpdate`  
`sudo ntpdate -u watch.stdtime.gov.tw`  
manual set date: `sudo date --s="2011-01-01 01:01:01"`  
reference: http://elmagnificogi.github.io/2015/11/08/RaspberryStartup-3/  
check ntp service state:  
`sudo service ntp status`  
`sudo service ntp start`  
`sudo service ntp stop`  
Taiwan ntp server list:
 - tock.stdtime.gov.tw
 - watch.stdtime.gov.tw
 - time.stdtime.gov.tw
 - clock.stdtime.gov.tw	
 - tick.stdtime.gov.tw


### auto ntp
pi@raspberrypi:~ $ timedatectl  
Local time: Tue 2016-08-30 17:27:05 CST  
Universal time: Tue 2016-08-30 09:27:05 UTC  
RTC time: n/a  
Time zone: Asia/Taipei (CST, +0800)  
NTP enabled: no  
NTP synchronized: yes  
RTC in local TZ: no  
DST active: n/a  
pi@raspberrypi:~ $ sudo timedatectl set-ntp yes  
pi@raspberrypi:~ $ sudo timedatectl   
Local time: Tue 2016-08-30 17:27:52 CST  
Universal time: Tue 2016-08-30 09:27:52 UTC  
RTC time: n/a  
Time zone: Asia/Taipei (CST, +0800)  
NTP enabled: yes  
NTP synchronized: yes  
RTC in local TZ: no  
DST active: n/a  


### vcgencmd: useful command to monitor hardware/firmware infomantion
`vcgencmd measure_clock <clock>`  
<clock> = arm, core, h264, isp, v3d, uart, pwm, emmc, pixel, vec, hdmi, dpi  

`vcgencmd measure_volts <id>`  
option: core, sdram_c, sdram_i, sdram_p  

`vcgencmd measure_temp`

`vcgencmd codec_enable <codec>`  
option: H264, MPG2, WVC1, MPG4, MJPG, WMV9  

`vcgencmd get_config [config|int|str]`  
query all setting: `vcgencmd get_config int`  

`vcgencmd version` query firmware version  

`vcgencmd otp_dump`  
28: serial number  
30: revision
mac address was generated from serial number  
refer with `ifconfig` and `cat /proc/cpuinfo` 


### rpi bench mark: sysbench

cpu:  
`sysbench --test=cpu --cpu-max-prime=10000 --num-threads=4 run`  

memory:  
`sysbench --test=memory --memory-block-size=1K --memory-total-size=10G --num-threads=4 run`  


### wifi configuration ( console mode )  

`sudo iwlist wlan0 scan | grep -i ESSID`  

https://www.raspberrypi.com.tw/2152/setting-up-wifi-with-the-command-line/    
`sudo vim /etc/wpa_supplicant/wpa_supplicant.conf`  


### check wifi signal quality/level

`cat /proc/net/wireless`  

`iwconfig wlan0 | grep -i --color quality`  



