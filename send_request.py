#!/usr/bin/env python3


import requests



r = requests.get('http://localhost:5000/random?seed={}'.format(input()))
print(r.text)