import logging
import os

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
    artist = request.args.get('artist', '')
    album = request.args.get('album', '')
    return render_template('albumen_search.html', artist=artist, album=album)

@app.route('/albumen/library', methods=['GET'])
def albumen_library():
    results_per_page = int(request.args.get('results_per_page', 50))
    page = int(request.args.get('page', 0))
    sortfield = request.args.get('sort', 'AZ') 
    return render_template('albumen_library.html', 
        albums=albumen_backend.library(sortfield, page=page, results_per_page=results_per_page),
        page=page, sortfield=sortfield)

@app.route('/albumen/search', methods=['POST'])
def albumen_post():
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

@app.route('/albumen/output', methods=['GET'])
def albumen_output():
    path = 'static/albumen/output'
    return render_template('albumen_output.html', images=[os.path.join(path, x) for x in os.listdir(path)])



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1066)
