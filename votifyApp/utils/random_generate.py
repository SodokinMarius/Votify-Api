import random
import string

def random_pass_generator(length=4):
    password = ''.join(random.choice(string.digits) for i in range(length))
    return password