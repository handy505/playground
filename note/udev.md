udev - Linux dynamic device management  
========================================  

### 0) Reference web page, google: udev  
https://www.kernel.org/pub/linux/utils/kernel/hotplug/udev/udev.html  
http://www.linuxjournal.com/article/7316?page=0,2  
http://linux.vbird.org/linux_basic/0610hardware/0610hardware-centos5.php#udev  
http://kolmogolovi.blogspot.tw/2011/11/linux-udev-1.html  
http://blog.xuite.net/mb1016.flying/linux/28257730-%E7%90%86%E8%A7%A3%E5%92%8C%E8%AA%8D%E8%AD%98udev  

### 1) Get the device information from system:  
`udevadm info -a -n ttyUSB0`  

### 2) Observe the feature, for example:    
```
  looking at device '/devices/pci0000:00/0000:00:14.0/usb1/1-1/1-1:1.0/ttyUSB0/tty/ttyUSB0':
    KERNEL=="ttyUSB0"
    SUBSYSTEM=="tty"
    DRIVER==""

  looking at parent device '/devices/pci0000:00/0000:00:14.0/usb1/1-1/1-1:1.0/ttyUSB0':
    KERNELS=="ttyUSB0"
    SUBSYSTEMS=="usb-serial"
    DRIVERS=="pl2303"
    ATTRS{port_number}=="0"
```
note that the **DRIVERS** feature

### 3) Write the configuration file
configuration file's location: `/dev/udev/rule.d/`  
content:  
```

DRIVERS=="ftdi_sio", SUBSYSTEM=="tty", ACTION=="add", NAME="handy", RUN+="/home/handy/udevtest/udevrun.sh", SYMLINK="ttyftdi"  
DRIVERS=="pl2303", SUBSYSTEM=="tty", ACTION=="add", NAME="handy", RUN+="/home/handy/udevtest/udevrun.sh", SYMLINK="ttypolific"  

```
you also can make a script to indicate your action:  
`RUN+="/home/handy/udevtest/udevrun.sh"`  
so you should write the `udevrun.h` in `/home/handy/udevtest/` by yourself.  
like this:
```
#!/bin/sh
LOGFILE=/home/handy/udevtest/xx.log
echo ${SEQNUM} ${SUBSYSTEM} ${ACTION} ${DEVNAME} >> ${LOGFILE} 2>&1
exit $?

```

### 4) Test the effect
insert hardware and observer the differents under `/dev`  
for example, use this instruction: `ls /dev/tty*`
