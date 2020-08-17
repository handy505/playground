#!/usr/bin/env python3

def main():
    for i in range(1, 10):
        for j in range(1, 10):
            print('{}*{}={:>2} '.format(j, i, i*j), end='')
        print('\n')

if __name__ == '__main__':
    main()