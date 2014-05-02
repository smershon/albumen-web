import os
import logging
from albumen import resolve
from albumen import storage
from albumen import download
from albumen import image_analysis

log = logging.getLogger(__name__)

data_path = 'static/albumen/data'
s = storage.Storage(data_path)

def unique_id(n):
    return 'uid-%05d' % n

def library():
    album_rows = s.all_albums()
    albums = []
    for idx, row in enumerate(sorted(album_rows)):
        album = {'artist': row[0], 'album': row[1], 'image': None}
        if row[2]:
            images = s.get_images_for_album(album['artist'], album['album'])
            if images:
                album['image'] = images[0]
        album['row_type'] = 'trodd' if idx % 2 else 'treven'
        albums.append(album)
    return albums

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
    
    if not url or url == 'null':
        s.update_album(artist, album, has_image=False)
        return True

    img = download.mb.from_url(url)
    artist_path = artist.replace(' ', '_')
    album_path = album.replace(' ', '_')
    fileroot = os.path.join(s.folder, artist_path)
    os.system('mkdir -p %s' % fileroot)
    filepath = os.path.join(fileroot, '%s.png' % album_path)
    if img:
        log.info('SAVING image for %s %s - %s', artist, album, filepath)
        new_img = download.mb.to_dir(img, filepath)
        analysis = image_analysis.analyze(new_img)
        s.update_image(artist, album, analysis)
        return True
    else:
        log.info('IMAGE not found at %s', url)
        return False
