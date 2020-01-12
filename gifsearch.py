import tenor_api
from random import randint
from random import seed
def get_gifs_by_keyword(keyword):
    return tenor_api.gif_search(keyword, limit=20, pos=randint(0, 10), safesearch='moderate')