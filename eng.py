# -*- coding: UTF-8 -*-
import os
import settings

from flask import Flask, render_template, url_for, redirect, request, jsonify, flash
from flask_login import LoginManager, logout_user, login_required, login_user, current_user

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = settings.SECRET_KEY
manager = LoginManager(app)

FIELD_HEIGHT = 25
FIELD_WIDTH = 45

if __name__ == "__main__":
    from controller import app
    from werkzeug.middleware.shared_data import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })
    app.run(debug=True)
