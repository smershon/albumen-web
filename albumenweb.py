import logging

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import albumen_backend

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/albumen', methods=['GET'])
def albumen_get():
    return render_template('albumen.html')

@app.route('/albumen', methods=['POST'])
def albumen_post():
    log.info(request.form)
    artist = request.form.get('artist')
    album = request.form.get('album')
    album_info = albumen_backend.search(artist, album)
    return jsonify(album_info)

@app.route('/albumen/save', methods=['POST'])
def albumen_save():
    log.info(request.form)
    return jsonify({})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1066)
