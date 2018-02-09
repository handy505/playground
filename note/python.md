## Unit test  - doctest
reference: https://docs.python.org/3.4/library/doctest.html  

### 1) use interpreter to try function.

    handy@handy-dell ~/democode/pycrc $ python3
    Python 3.4.3 (default, Oct 14 2015, 20:28:29)
    [GCC 4.8.4] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from crc import crc16
    >>> lst = [0x01,0x03,0x00,0x00,0xaa,0xbb,0xaa,0xbb]
    >>> ret = crc16(lst)
    >>> hex(ret)
    '0xdde9'
    >>>



### 2) copy and paste the interpreter result to py source file as document string

    def crc16(buf):
        ''' return crc, port from DDC team.
        >>> lst = [0x01,0x03,0x00,0x00,0xaa,0xbb,0xaa,0xbb]
        >>> hex(crc16(lst))
        '0xdde9'
        >>> lst = [0x01,0x03,0x00,0x00,0xaa,0xbb,0xcc,0xdd]
        >>> hex(crc16(lst))
        '0x7663'
        >>> lst = [0x01,0x03,0xc0,0x20,0x00,0x18]
        >>> hex(crc16(lst))
        '0x780a'
        '''


### 3) module test  
`python3 -m doctest crc.py -v`  

result as bellow:  

    Trying:
        lst = [0x01,0x03,0x00,0x00,0xaa,0xbb,0xaa,0xbb]
    Expecting nothing
    ok
    Trying:
        hex(crc16(lst))
    Expecting:
        '0xdde9'
    ok
    Trying:
        lst = [0x01,0x03,0x00,0x00,0xaa,0xbb,0xcc,0xdd]
    Expecting nothing
    ok
    Trying:
        hex(crc16(lst))
    Expecting:
        '0x7663'
    ok
    Trying:
        lst = [0x01,0x03,0xc0,0x20,0x00,0x18]
    Expecting nothing
    ok
    Trying:
        hex(crc16(lst))
    Expecting:
        '0x780a'
    ok
    1 items had no tests:
        crc
    1 items passed all tests:
       6 tests in crc.crc16
    6 tests in 2 items.
    6 passed and 0 failed.
    Test passed.


## compile pyc to hide source code

### 1) use compileall module

    handy@handy-dell ~/solarpi/dev2 $ python3
    Python 3.4.3 (default, Oct 14 2015, 20:28:29) 
    [GCC 4.8.4] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import compileall
    >>> compileall.compile_dir(".", force=True)

### 2) rename the file names

    handy@handy-dell ~/solarpi/dev2/__pycache__ $ ls
    crc.cpython-34.pyc        hearbeat.cpython-34.pyc  pvinverter.cpython-34.pyc
    debug.cpython-34.pyc      __init__.cpython-34.pyc  serial2.cpython-34.pyc
    debug_off.cpython-34.pyc  logging2.cpython-34.pyc  upload.cpython-34.pyc
    gui.cpython-34.pyc        main.cpython-34.pyc
    handy@handy-dell ~/solarpi/dev2/__pycache__ $ rename 's/\.cpython-34//' *
    handy@handy-dell ~/solarpi/dev2/__pycache__ $ ls
    crc.pyc        gui.pyc       logging2.pyc    serial2.pyc
    debug_off.pyc  hearbeat.pyc  main.pyc        upload.pyc
    debug.pyc      __init__.pyc  pvinverter.pyc

