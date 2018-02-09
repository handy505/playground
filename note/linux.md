## Install software
`sudo apt-get install`  
`dpkg -i *.deb`  
`dpkg -l`  
`dpkg --get-selection`  


## File zip  
** *.gz **:`gzip`, `gunzip`  
** *.bz2 **: `bzip2`, `bunzip2`  
`tar [-jcv -f]`, `tar [-jxv]`  

## Shell  
`echo`  
`alias` / `unalias`  
`bg` / `fg`  
`set` / `unset`
`env`  
`type`  
`wait`  
`history`  
`read`  
`exec`  
`shopt`  
`declare`  
`fc`  
query file encode type: 'file -i <filename>'


## Module  
`lsmod`  
`modinfo`  
`insmod`  
`modprobe`  
`rmmod`  

## mount extra hardisk to filesystem
find fd out: `ls /dev/sd*`  
try to mount: `sudo mount /dev/sdb5 /mnt`  
refused to mount, because the ntfs filesystem was unclean.  
suggest to mount with read-only mode.  
```
The disk contains an unclean file system (0, 0).
Metadata kept in Windows cache, refused to mount.
Failed to mount '/dev/sdb5': Operation not permitted
The NTFS partition is in an unsafe state. Please resume and shutdown
Windows fully (no hibernation or fast restarting), or mount the volume
read-only with the 'ro' mount option.
```
try again: `sudo mount -o ro /dev/sdb5 /mnt/`  

unmount the device: `sudo umount /mnt`
note that: spell the instruction is **u** mount, not **un** mount.  

## Network  
`ping [-c]`

`netstat [-anltup]`
```
-a: all
-n: numeric
-l: listen
-t: tcp
-u: udp
-p: pid/program-name
```
`netstat -an`: all connection  
`netstat -an | grep :80`: show port 80 connection  

`traceroute`  
`arpwatch`  

firewall setting:  
`iptables`, `iptables-save`, `iptables-restore`  
`ip6tables`, `ip6tables-save`, `ip6tables-restore`  

`ip`: powerful network setting tool  
`iptraf`: monite network date flow  
