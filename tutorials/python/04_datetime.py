import datetime

if __name__ == "__main__":

    now = datetime.datetime.now()
    print(now)

    s = now.strftime('%Y/%m/%d %H:%M:%S')
    print(s)


'''
$ python3 04_datetime.py
2020-12-11 16:33:42.404294
2020/12/11 16:33:42
'''
