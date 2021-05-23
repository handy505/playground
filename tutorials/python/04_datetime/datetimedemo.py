import datetime

if __name__ == "__main__":

    now = datetime.datetime.now()
    print(now)

    s = now.replace(microsecond=0)
    print(s)

    s = now.strftime('%Y/%m/%d %H:%M:%S')
    print(s)


'''
2021-05-22 23:27:52.992784
2021-05-22 23:27:52
2021/05/22 23:27:52
'''
