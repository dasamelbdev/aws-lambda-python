import json
from urllib import response

# some JSON:
x = '{"data":{"name":"john","age":27},"city":"colombo"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
#print(y["data"]["name"])

def m():
    if 12>108: 
     reponse='a'
    elif 590<44:
     reponse='b'
    else:
     reponse='d'
    return reponse

print(m())