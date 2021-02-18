from Crypto.Cipher import AES
import base64


def padding(s):
    return s + (16 - len(s) % 16) * '!'


key = b'fucktheablerexla'
#cipher = AES.new(key, AES.MODE_EAX)
cipher = AES.new(key, AES.MODE_CBC)


data = [0x79, 0x95, 0x63, 0x56, 0x11, 0x56, 0x86, 0x40,
        0x86, 0x40, 0x11, 0x56, 0x63, 0x56, 0x99, 0x99]

# mac = b'E04F4302DD62'
# data = [
#     # MAC 13
#     mac[0],  mac[1], mac[2], mac[3], mac[4], mac[5], mac[6], mac[7], mac[8], mac[9],
#     mac[10], mac[11], 13,
#     # Q1 48
#     # c[6],c[5],c[4],c[3],c[2],c[1],c[0],//測試計數
#     40, 49, 49, 48, 46, 49, 32, 49, 48, 48,
#     46, 49, 32, 49, 49, 48, 46, 50, 32, 57,
#     55, 56, 32, 53, 57, 46, 57, 32, 48, 46,
#     49, 50, 32, 51, 56, 46, 56, 32, 48, 48,
#     48, 48, 48, 48, 48, 48, 13,
#     # //I 40
#     35, 65, 98, 108, 101, 114, 101, 120, 67, 111,
#     109, 112, 97, 110, 121, 32, 32, 84, 101, 115,
#     116, 77, 111, 100, 101, 108, 32, 32, 115, 111,
#     102, 116, 84, 101, 115, 116, 86, 101, 13,
#     # //F 23
#     35, 49, 49, 48, 46, 50, 32, 48, 48, 52,
#     32, 48, 49, 46, 50, 51, 32, 53, 57, 46,
#     56, 13
# ]


data2 = bytearray(data)
data3 = base64.b64encode(data2)
data4 = data3.decode('utf-8')
data5 = padding(data4)
data6 = cipher.encrypt(data5.encode('utf-8'))
#ciphertext, tag = cipher.encrypt_and_digest(data5.encode('utf-8'))
#nonce = cipher.nonce
iv = cipher.iv

print(data)
print(data2)
print(data3)
print(data4)
print(data5)
print(data6)
'''
print(ciphertext)
print(tag)
print(cipher.nonce)
'''

print('~~~ transmit ~~~')
#cipher = AES.new(key, AES.MODE_EAX, nonce)
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
#data5 = cipher.decrypt_and_verify(ciphertext, tag)
# data5 = cipher.decrypt(data6)
# data4 = data5.decode('utf-8')
# data3 = data4.rstrip('!')
# data2 = base64.b64decode(data3)
# data = list(data2)

data5 = cipher.decrypt(data6)
data4 = data5.decode('utf-8')
data3 = data4.rstrip('!')
data2 = base64.b64decode(data3)
data = list(data2)

# print(data6)
# print(data5)
# print(data4)
# print(data3)
# print(data2)
# print(data)

print(data6)
print(data5)
print(data2)
print(data)
