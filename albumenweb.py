import logging

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import albumen_backend

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/albumen/search', methods=['GET'])
def albumen_search():
    return render_template('albumen_search.html')

@app.route('/albumen/library', methods=['GET'])
def albumen_library():
    return render_template('albumen_library.html', albums=albumen_backend.library())

@app.route('/albumen/search', methods=['POST'])
def albumen_post():
    log.info(request.form)
    artist = request.form.get('artist')
    album = request.form.get('album')
    album_info = albumen_backend.search(artist, album)
    log.info(album_info)
    return jsonify(album_info)

@app.route('/albumen/save', methods=['POST'])
def albumen_save():
    d = request.form
    log.info(d)

    for field in ('artist', 'album', 'image_url'):
        if field not in d:
            log.error('Missing field: %s' % field)
            return jsonify({'status': 'failed'})

    if albumen_backend.save(request.form['artist'], request.form['album'], request.form['image_url']):
        return jsonify({'status': 'success'})

    return jsonify({'status': 'failed'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1066)
