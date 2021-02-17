from Crypto.Cipher import AES
import base64


def padding(s):
    return s + (16 - len(s)%16) * '!'


secret = 'fucktheablerexla'
cipher = AES.new(secret)


data= [0x79, 0x95, 0x63, 0x56, 0x11, 0x56, 0x86, 0x40,
       0x86, 0x40, 0x11, 0x56, 0x63, 0x56, 0x99, 0x99]

data2 = bytearray(data)
data3 = base64.b64encode(data2)
data4 = data3.decode('utf-8')
data5 = padding(data4)
data6 = cipher.encrypt(data5)

print(data)
print(data2)
print(data3)
print(data4)
print(data5)
print(data6)


print('~~~ transmit ~~~')

data5 = cipher.decrypt(data6)
data4 = data5.decode('utf8')
data3 = data4.rstrip('!')
data2 = base64.b64decode(data3)
data = list(data2)

print(data6)
print(data5)
print(data4)
print(data3)
print(data2)
print(data)


'''
handy@ubuntu:~/encrypt$ python3 encryption_demo.py 
[121, 149, 99, 86, 17, 86, 134, 64, 134, 64, 17, 86, 99, 86, 153, 153]
bytearray(b'y\x95cV\x11V\x86@\x86@\x11VcV\x99\x99')
b'eZVjVhFWhkCGQBFWY1aZmQ=='
eZVjVhFWhkCGQBFWY1aZmQ==
eZVjVhFWhkCGQBFWY1aZmQ==!!!!!!!!
b"Y\xb6S\x9eY\x16_\xdf\xe1n\xc4'\x9dH\x99\x92\xd11\xef\xbd\xb7W]@|\x15\xa4'9\x8ex."
~~~ transmit ~~~
b"Y\xb6S\x9eY\x16_\xdf\xe1n\xc4'\x9dH\x99\x92\xd11\xef\xbd\xb7W]@|\x15\xa4'9\x8ex."
b'eZVjVhFWhkCGQBFWY1aZmQ==!!!!!!!!'
eZVjVhFWhkCGQBFWY1aZmQ==!!!!!!!!
eZVjVhFWhkCGQBFWY1aZmQ==
b'y\x95cV\x11V\x86@\x86@\x11VcV\x99\x99'
[121, 149, 99, 86, 17, 86, 134, 64, 134, 64, 17, 86, 99, 86, 153, 153]

'''

