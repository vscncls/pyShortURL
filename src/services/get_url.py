import random
from string import ascii_letters


def get_random_url(char_num=6):
    return ''.join(random.choices(ascii_letters, k=char_num))
