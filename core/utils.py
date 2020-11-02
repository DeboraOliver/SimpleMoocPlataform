import hashlib
import string
import random

#gro caracteres ramdomicos que user supercase e digitos
def random_key(size=5):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))

#pega o texto ramdomico e add alguns dados do user para evitar repetição
def generate_hash_key(salt, random_str_size=5):
    random_str = random_key(random_str_size)
    text = random_str + salt
    return hashlib.sha224(text.encode('utf-8')).hexdigest()