#!/usr/bin/python3

def chunks(s, n):
    for start in range(0, len(s), n):
        yield s[start:start+n]

def main():
    s = 'abcdefghijk'
    for chunk in chunks(s, 3):
        print(chunk)

if __name__ == '__main__':
    main()
