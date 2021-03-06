import os
import logging

import Image

from albumen import resolve
from albumen import storage
from albumen import download
from albumen import image_analysis
from albumen import util
from albumen.produce import squarepack

log = logging.getLogger(__name__)

data_root = 'static/albumen'
data_path = 'static/albumen/data'
s = storage.Storage(data_path)

def unique_id(n):
    return 'uid-%05d' % n

def _sortkey(doc, field):
    def dval(x):
        image = doc.get('image') or {}
        return image.get(x, 0.0)

    lookup = {
        'AZ': (doc['artist'], doc['album']),
        'ZA': (doc['artist'], doc['album']),
        'red': dval('red'),
        'green': dval('green'),
        'blue': dval('blue'),
        'cyan': dval('red'),
        'magenta': dval('green'),
        'yellow': dval('blue'),
        'black': dval('lightness'),
        'white': dval('lightness'),
        'gray': dval('saturation'),
        'color': dval('saturation'),
        'complexity': dval('complexity'),
        'smoothness': dval('complexity')
    }

    return lookup[field]

def library(sortfield, page=0, results_per_page=50, version='data'):
    ss = storage.Storage('%s/%s' % (data_root, version))

    album_rows = ss.all_albums()
    albums = []

    for row in album_rows:
        album = {'artist': row[0].decode('utf-8'), 'album': row[1].decode('utf-8'), 'image': None}
        if row[2]:
            images = ss.get_images_for_album(album['artist'], album['album'])
            if images:
                image = images[0]
                image['path'] = image['path'].decode('utf-8')
                album['image'] = image
        albums.append(album)

    total = len(albums)
    reverse_fields = ['ZA', 'red', 'green', 'blue', 'white', 'color', 'complexity']
    albums.sort(key=lambda x: _sortkey(x, sortfield), reverse=sortfield in reverse_fields)
    albums = albums[page*results_per_page:(page+1)*results_per_page]

    for idx, row in enumerate(albums):
        row['row_type'] = 'trodd' if idx % 2 else 'treven'

    return albums, total

def search(artist, album):
    if artist and album:
        return dict(search_type='full', **search_artist_album(artist.encode('utf-8'), album.encode('utf-8')))
    else:
        return dict(search_type='artist', **search_artist(artist.encode('utf-8')))

def search_artist(artist):
    results = set([(x[0], x[1]) for x in resolve.search(artist=artist)])
    return {'albums': sorted([{'artist': x[0], 'album': x[1]} for x in results], key=lambda x: (x['artist'], x['album']))}

def search_artist_album(artist, album):
    images = []
    all_albums = set([(artist, album)])
    idx = 0
    log.info('%s --- %s', artist, album)
    results = resolve.search(artist=artist, title=album)
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
    artist_path = util.scrub(artist).replace(' ', '_').replace("'", '_')
    album_path = util.scrub(album).replace(' ', '_').replace("'", '_')
    fileroot = os.path.join(s.folder, artist_path)
    os.system('mkdir -p %s' % fileroot)
    filepath = os.path.join(fileroot, '%s.png' % album_path)
    if img:
        log.info('SAVING image for %s %s - %s', artist_path, album_path, filepath)
        new_img = download.mb.to_dir(img, filepath)
        analysis = image_analysis.analyze(new_img)
        s.update_album(artist, album, has_image=True)
        s.update_image(artist, album, analysis, replace=True)
        return True
    else:
        log.info('IMAGE not found at %s', url)
        return False

def img_generator(attr, num):
    albums, _ = library(attr, results_per_page=num)
    for src in [x['image']['path'] for x in albums]:
        yield Image.open(src)

def gen_bg(attr, width, height, num):
    im = squarepack.build_image(width, height, num, img_generator(attr, num))
    im.save('static/albumen/output/bg_%dx%d_%s.png' % (width, height, attr), format='PNG')


