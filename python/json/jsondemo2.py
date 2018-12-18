
import json
import collections


# encode
d = {'A':1, 'B':2}

s = json.dumps(d)
print(s)



# decode
s = '{"A": 1, "B": 2, "C":3}'

d = json.loads(s)
print(type(d))
print(d)
