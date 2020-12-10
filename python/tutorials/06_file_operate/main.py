#!/usr/bin/env python3
# -*- coding:utf-8 -*-


def main():

    # file1
    fout = open('file1.txt', 'w', encoding='utf-8')
    fout.write("abcdefg\n")
    fout.close()

    # file2
    with open('file2.txt', 'w', encoding='utf-8') as fh:
        fh.write('abcdefghijk\n')

if __name__ == "__main__":
    main()


'''
pi@raspberrypi:~/demo/python/lessons/06_file_operate $ python3 main.py 
pi@raspberrypi:~/demo/python/lessons/06_file_operate $ ls
file1.txt  file2.txt  main.py
pi@raspberrypi:~/demo/python/lessons/06_file_operate $ cat file1.txt 
abcdefg
pi@raspberrypi:~/demo/python/lessons/06_file_operate $ cat file2.txt 
abcdefghijk
'''
