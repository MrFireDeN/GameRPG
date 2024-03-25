from eng import request, render_template, FIELD_WIDTH, FIELD_HEIGHT, app, redirect, url_for, login_user, \
    logout_user, login_required, jsonify
from models import PersonaData, PlayerData, CharacterData, PlayerInventory, CharacterInventory, ItemData, WallData, \
    DoorData, EquipmentData, ConsumableData, QuestData, QuestProgress, db_session

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.htm'), 404

"""https//:localhost:5000/field?X=0&Y=0"""
@app.route("/field/")
def get_field():
    if not(request.args):
        x = 0
        y = 0
    else:
        x = int(request.args.get("X"))
        y = int(request.args.get("Y"))

    # Игрок
    player = db_session.query(PlayerData).first()

    # Стены
    walls = db_session.query(WallData).filter(
        WallData.x >= x - FIELD_WIDTH / 2,
        WallData.x <= x + FIELD_WIDTH / 2,
        WallData.y >= y - FIELD_HEIGHT / 2,
        WallData.y <= y + FIELD_HEIGHT / 2
    ).all()

    # Двери
    doors = db_session.query(DoorData).filter(
        DoorData.x >= x - FIELD_WIDTH / 2,
        DoorData.x <= x + FIELD_WIDTH / 2,
        DoorData.y >= y - FIELD_HEIGHT / 2,
        DoorData.y <= y + FIELD_HEIGHT / 2
    ).all()

    # Формируем данные в формате JSON
    field_data = {
        'player': player.serialize(),  # Предположим, у вас есть метод serialize() для модели
        'walls': [wall.serialize() for wall in walls],  # Предположим, у вас есть метод serialize() для модели
        'doors': [door.serialize() for door in doors]  # Предположим, у вас есть метод serialize() для модели
    }

    return jsonify(field_data)

@app.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.htm')
    login = request.form.get('username')
    password = request.form.get('password')
    player = PlayerData(login=login, password=password)
    db_session.add(player)
    db_session.commit()
    login_user(player)
    return render_template('register.htm')

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