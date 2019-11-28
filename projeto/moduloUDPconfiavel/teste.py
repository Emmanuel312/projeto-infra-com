from socket import *
from os import listdir
import pickle
import json


class Cu:
    def __init__(self,cu):
        self.cu = cu


cu = Cu(0)
print(type(cu))
cu = pickle.dumps(cu)
print(type(cu))

cu = pickle.loads(cu)
print(type(cu))

print(cu.cu)