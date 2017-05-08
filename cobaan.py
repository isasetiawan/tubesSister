from itertools import product
from string import ascii_lowercase
import json
import bcrypt

# membangkitkan kombinasi karakter
keywords = [''.join(i) for i in product(ascii_lowercase, repeat=2)]
njobs = len(keywords) / 10
for i in range(0, len(keywords), njobs):
    a = i
    b = 0
    if (i + njobs) < len(keywords):
        b = i + njobs - 1
    else:
        b = len(keywords) - 1
    print a, b
