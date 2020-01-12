import tenor_api

def get_gifs_by_keyword(keyword):
    return tenor_api.gif_search(keyword, limit=1, safesearch='moderate')