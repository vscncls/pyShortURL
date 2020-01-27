import random
from string import ascii_letters
from src.models.urls import Url


def get_random_url(char_num=6):
    url = ''.join(random.choices(ascii_letters, k=char_num))
    while True:
        q = Url.query.filter_by(shortenend_url=url).first()
        if not q:
            break
        url.shortenend_url = get_random_url()
    return url
