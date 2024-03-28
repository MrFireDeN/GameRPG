import time

from eng import request, render_template, FIELD_WIDTH, FIELD_HEIGHT, app, redirect, url_for, login_user, \
    logout_user, login_required, jsonify
from models import PersonaData, PlayerData, CharacterData, PlayerInventory, CharacterInventory, ItemData, WallData, \
    DoorData, EquipmentData, ConsumableData, QuestData, QuestProgress, db_session, ENEMY, FRIEND, WEAPON, ARMOR

GAME_STATUS = ('WALKING', 'FIGHTING', 'TALKING', 'LOOKING')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.htm'), 404


@app.route("/get-field/")
def get_field():
    # if not(request.args):
    #     x = 0
    #     y = 0
    # else:
    #     x = int(request.args.get("X"))
    #     y = int(request.args.get("Y"))

    # Игрок
    player = db_session.query(PlayerData).first()
    x = player.x
    y = player.y

    # Стены
    walls = db_session.query(WallData).filter(
        WallData.x >= x - FIELD_WIDTH / 2,
        WallData.x < x + FIELD_WIDTH / 2,
        WallData.y >= y - FIELD_HEIGHT / 2,
        WallData.y < y + FIELD_HEIGHT / 2
    ).all()

    # Двери
    doors = db_session.query(DoorData).filter(DoorData.id == player.id).filter(
        DoorData.x >= x - FIELD_WIDTH / 2,
        DoorData.x < x + FIELD_WIDTH / 2,
        DoorData.y >= y - FIELD_HEIGHT / 2,
        DoorData.y < y + FIELD_HEIGHT / 2
    ).all()

    # Формируем данные в формате JSON
    field_data = {
        'player': player.serialize_coordinates(),
        'walls': [wall.serialize_coordinates() for wall in walls],
        'doors': [door.serialize_coordinates() for door in doors]
    }

    return jsonify(field_data)

@app.route("/move", methods=['POST'])
def move():
    key = request.form['key']

    # Получаем игрока из базы данных
    player = db_session.query(PlayerData).first()

    if key == 'ArrowUp':
        player.y -= 1  # Сдвигаем игрока вверх
    elif key == 'ArrowDown':
        player.y += 1  # Сдвигаем игрока вниз
    elif key == 'ArrowLeft':
        player.x -= 1  # Сдвигаем игрока влево
    elif key == 'ArrowRight':
        player.x += 1  # Сдвигаем игрока вправо

    # В этом месте также можно добавить проверки на границы поля,
    # чтобы игрок не мог выйти за его пределы
    wall = db_session.query(WallData).filter(WallData.x == player.x, WallData.y == player.y).first()
    door = db_session.query(DoorData).filter(DoorData.id == player.id, not(DoorData.is_open), DoorData.x == player.x, DoorData.y == player.y).first()

    print(door)

    if wall or door:
        return jsonify({'status': 'failure'})

    # Сохраняем изменения в базе данных
    db_session.commit()
    time.sleep(0.2)

    print(player.serialize_coordinates())

    return jsonify({'status': 'success'})

@app.route('/get-window', methods=['GET'])
def get_window():
    player = db_session.query(PlayerData).first()
    game_status = game_satus(player)
    if game_status == GAME_STATUS[0]:
        return jsonify('')
    elif game_status == GAME_STATUS[1]:
        return jsonify('')
    elif game_status == GAME_STATUS[2]:
        return jsonify('')
    elif game_status == GAME_STATUS[3]:
        return jsonify('')

    return jsonify('')

def walking_info(player):
    pass

@app.route("/attack/", methods=['POST'])
def attack():
    #player = db_session.query(PlayerData).first()
    pass

def game_satus(player):
    # Если игрок стоит рядом с персонажем
    character = (db_session.query(CharacterData).filter(CharacterData.player_id == player.id).
                 filer(CharacterData.x == player.x, CharacterData.y == player.y))
    if (character):
        if character.loyalty == ENEMY:
            return GAME_STATUS[1]
        else:
            return GAME_STATUS[2]

    return GAME_STATUS[0]


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
    return render_template(page_name + '.htm')


@app.route("/")
def index():
    return redirect(url_for('main', page_name='main'))


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
