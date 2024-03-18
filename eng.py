# -*- coding: UTF-8 -*-
import os
import settings

from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, logout_user, login_required, login_user

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = settings.SECRET_KEY
manager = LoginManager(app)

import models
from models import db_session, PersonaData, PlayerData, EnemyData, CharacterData, InventoryData, ItemData, \
    EquipmentData, ConsumableData, WallData, DoorData

FIELD_HEIGHT = 20
FILED_WIDTH = 40

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.htm'), 404
#
# """field?X=0&Y=0"""
# @app.route("/field/")
# def get_field():
#     x = int(request.args.get("X"))
#     y = int(request.args.get("Y"))
#
#     # Игрок
#     player = db_session.query(PersonaData).first()
#
#     # Враги
#     enemies = db_session.query(EnemyData).filter(
#         x + FILED_WIDTH / 2 < EnemyData.persona.x < x - FILED_WIDTH / 2 and
#         y + FIELD_HEIGHT / 2 < EnemyData.persona.y < y - FIELD_HEIGHT / 2)
#
#     # Персонажи
#     characters = db_session.query(CharacterData).filter(
#         x + FILED_WIDTH / 2 < CharacterData.persona.x < x - FILED_WIDTH / 2 and
#         y + FIELD_HEIGHT / 2 < CharacterData.persona.y < y - FIELD_HEIGHT / 2 )
#
#     # Стены
#     walls = db_session.query(WallData).filter(
#         x + FILED_WIDTH / 2 < WallData.persona.x < x - FILED_WIDTH / 2 and
#         y + FIELD_HEIGHT / 2 < WallData.persona.y < y - FIELD_HEIGHT / 2)
#
#     # Двери
#     doors = db_session.query(CharacterData).filter(
#         x + FILED_WIDTH / 2 < DoorData.persona.x < x - FILED_WIDTH / 2 and
#         y + FIELD_HEIGHT / 2 < DoorData.persona.y < y - FIELD_HEIGHT / 2)
#
#     # Предметы
#     items = db_session.query(CharacterData).filter(
#         x + FILED_WIDTH / 2 < ItemData.persona.x < x - FILED_WIDTH / 2 and
#         y + FIELD_HEIGHT / 2 < ItemData.persona.y < y - FIELD_HEIGHT / 2)
#
#     return render_template("field.htm", player, enemies, characters, walls, doors, items)

@app.route("/<page_name>/")
def main(page_name):
    return render_template(page_name+'.htm')

@app.route("/")
def index():
    return redirect(url_for('main', page_name='main'))

@app.route("/attack/")
def attack():
    print("attack\n"*10)
    #Battle().player_turn()
    return redirect(url_for('main', page_name='window'))

@app.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.htm')
    login = request.form.get('username')
    password = request.form.get('password')
    player = models.PlayerData(login=login, password=password)
    db_session.add(player)
    db_session.commit()
    login_user(player)
    return render_template('register.htm')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))

@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('register'))
    return response


if __name__ == "__main__":
##    #Еще один способ добавления статической дирректории
    from werkzeug.middleware.shared_data import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'static')
    })
    app.run(debug=True)
