# -*- coding: UTF-8 -*-
import os

from flask import Flask, g, render_template, request, jsonify, url_for, send_file, redirect
from static.py.main import main

import settings

app = Flask(__name__, template_folder="templates")

app.config['SECRET_KEY'] = settings.SECRET_KEY


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.htm'), 404


@app.route("/<page_name>/")
def main(page_name):
    return render_template(page_name+'.htm')

@app.route("/")
def index():
    return redirect(url_for('main', page_name='main'))


if __name__ == "__main__":
##    #Еще один способ добавления статической дирректории
    from werkzeug.middleware.shared_data import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })
    app.run(host='0.0.0.0', port=5000, debug=True)
