## monite crontab action  
`watch -n 1 -d tail -n 4 debug`  

## crontab config  
	#* 8,9,17,18 * * 1-5 /usr/bin/python3 /home/handy/democode/python/hhsaver/hhsaver.py
	* * * * * /usr/bin/python3 /home/handy/democode/python/hhsaver/hhsaver.py >> /home/handy/democode/python/hhsaver/debug
	* * * * * /bin/date >> /home/handy/democode/python/hhsaver/datelog.txt

## display gui on monitor: export DISPLAY=:0

	* * * * * export DISPLAY=:0 && /usr/bin/python3 /home/handy/democode/python/hhsaver/hhsaver.py >> /home/handy/democode/python/hhsaver/debug
	* * * * * /bin/date >> /home/handy/democode/python/hhsaver/datelog.txt




