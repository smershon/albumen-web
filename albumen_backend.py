import os
import logging
from albumen import resolve
from albumen import storage
from albumen import download

log = logging.getLogger(__name__)

data_path = 'static/albumen/data'
s = storage.Storage(data_path)

def unique_id(n):
    return 'uid-%05d' % n

def search(artist, album):
    images = []
    all_albums = set()
    idx = 0
    log.info('%s --- %s', artist, album)
    results = resolve.search(artist, album)
    log.info(results)
    for artist_name, album_name, mbid in results:
        all_albums.add((artist_name, album_name))
        for url in download.mb.image_urls(mbid):
            images.append({
                'artist_name': artist_name,
                'album_name': album_name,
                'image': {'url': url, 'uid': unique_id(idx)}
            })
            idx += 1
    albums = []
    for artist_name, album_name in all_albums:
        albums.append({
            'artist_name': artist_name,
            'album_name': album_name,
            'image': {'url': '/static/albumen/no_image.png', 'uid': unique_id(idx)}
        })
        idx += 1
    return {'images': images, 'albums': albums}

def save(artist, album, url):
    log.info('%s %s %s', artist, album, url)
    img = download.mb.from_url(url)
    artist_path = artist.replace(' ', '_')
    album_path = album.replace(' ', '_')
    fileroot = os.path.join(s.folder, artist_path)
    os.system('mkdir -p %s' % fileroot)
    filepath = os.path.join(fileroot, '%s.png' % album_path)
    if img:
        log.info('SAVING image for %s %s - %s', artist, album, filepath)
        s.update_image(artist, album, download.mb.to_dir(img, filepath))
        return True
    else:
        log.info('IMAGE not found at %s', url)
        return False
