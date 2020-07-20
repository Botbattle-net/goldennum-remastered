import random
import string

key = ''.join([random.SystemRandom().choice(string.ascii_lowercase)
               for i in range(0, 50)])

with open('web/web/secret_key.py', 'w') as File:
    File.write("secret_key = '" + key + "'")
