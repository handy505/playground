from Crypto.Cipher import AES
import base64


def padding(s):
    return s + (16 - len(s)%16) * '!'


key = b'fucktheablerexla'
cipher = AES.new(key, AES.MODE_EAX)


data= [0x79, 0x95, 0x63, 0x56, 0x11, 0x56, 0x86, 0x40,
       0x86, 0x40, 0x11, 0x56, 0x63, 0x56, 0x99, 0x99]

data2 = bytearray(data)
data3 = base64.b64encode(data2)
data4 = data3.decode('utf-8')
data5 = padding(data4)
ciphertext, tag = cipher.encrypt_and_digest(data5.encode('utf-8'))
nonce = cipher.nonce

print(data)
print(data2)
print(data3)
print(data4)
print(data5)
print(ciphertext)
print(tag)
print(cipher.nonce)


print('~~~ transmit ~~~')
cipher = AES.new(key, AES.MODE_EAX, nonce)
data5 = cipher.decrypt_and_verify(ciphertext, tag)
data4 = data5.decode('utf8')
data3 = data4.rstrip('!')
data2 = base64.b64decode(data3)
data = list(data2)

print(data5)
print(data4)
print(data3)
print(data2)
print(data)
