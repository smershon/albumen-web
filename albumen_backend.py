from albumen import resolve
from albumen import storage
from albumen import download

s = storage.Storage('static/albumen')

def unique_id(n):
    return 'uid-%05d' % n

def search(artist, album):
    mbids = resolve.search(artist, album)
    image_urls = [x for x in download.mb.image_urls(mbids)]
    return {
        'artist_name': artist,
        'album_name': album,
        'images': [{'url': v, 'uid': unique_id(i)} for i,v in enumerate(image_urls)]
    }
