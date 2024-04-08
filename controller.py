import time

from eng import request, render_template, FIELD_WIDTH, FIELD_HEIGHT, app, redirect, url_for, login_user, \
    logout_user, login_required, jsonify, flash, manager, current_user
from models import PersonaData, PlayerData, CharacterData, PlayerInventory, CharacterInventory, ItemData, WallData, \
    DoorData, EquipmentData, ConsumableData, QuestData, QuestProgress, db_session, ENEMY, FRIEND, WEAPON, ARMOR
from re import match

GAME_STATUS = ('WALKING', 'FIGHTING', 'TALKING', 'LOOKING')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.htm'), 404

@app.route("/get-player-status")
def get_player_status():
    # Игрок
    player = db_session.query(PlayerData).first()

    player_status = {
        "health": player.health,
        "max_health": player.max_health,
        "level": player.level,
        "ep": player.ep,
        "money": 0
    }

    return jsonify(player_status)


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

    # Персонажи
    characters = db_session.query(CharacterData).filter(CharacterData.player_id == player.id).filter(
        CharacterData.x >= x - FIELD_WIDTH / 2,
        CharacterData.x < x + FIELD_WIDTH / 2,
        CharacterData.y >= y - FIELD_HEIGHT / 2,
        CharacterData.y < y + FIELD_HEIGHT / 2
    ).all()

    # Инициализация списков для друзей и врагов
    friends = []
    enemies = []

    # Разделение персонажей на друзей и врагов
    for character in characters:
        print(character.loyalty)
        if character.loyalty:
            friends.append(character)
        else:
            enemies.append(character)

    print(friends)
    print(enemies)

    # Стены
    walls = db_session.query(WallData).filter(
        WallData.x >= x - FIELD_WIDTH / 2,
        WallData.x < x + FIELD_WIDTH / 2,
        WallData.y >= y - FIELD_HEIGHT / 2,
        WallData.y < y + FIELD_HEIGHT / 2
    ).all()

    # Двери
    doors = db_session.query(DoorData).filter(DoorData.player_id == player.id).filter(
        DoorData.x >= x - FIELD_WIDTH / 2,
        DoorData.x < x + FIELD_WIDTH / 2,
        DoorData.y >= y - FIELD_HEIGHT / 2,
        DoorData.y < y + FIELD_HEIGHT / 2
    ).all()

    # Формируем данные в формате JSON
    field_data = {
        'player': player.serialize_coordinates(),
        'friends': [friend.serialize_coordinates() for friend in friends],
        'enemies': [enemy.serialize_coordinates() for enemy in enemies],
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
        return walking_info(player)
    if game_status == GAME_STATUS[1]:
        return dialog_info(player)
    if game_status == GAME_STATUS[2]:
        return dialog_info(player)
    if game_status == GAME_STATUS[3]:
        return jsonify('')

    return jsonify('')

def walking_info(player):
    level = 'Природа'
    level_note = 'Кароче очь красиво, мамой клянусб'

    walking_data = {
        'game_status': GAME_STATUS[0],
        'player': player.serialize(),
        'note': level_note if level_note else None,
        'name': level if level else None
    }

    return jsonify(walking_data)

def dialog_info(player):
    enemy = (db_session.query(CharacterData).filter(CharacterData.player_id == player.id).
             filter(CharacterData.x == player.x, CharacterData.y == player.y)).first()

    window_data = {
        'game_status': GAME_STATUS[1],
        'player': player.serialize(),
        'player_weapon': player.weapon.serialize() if player.weapon else None,
        'player_armor': player.armor.serialize() if player.armor else None,
        'player_consumable1': player.consumable1.serialize() if player.consumable1 else None,
        'player_consumable2': player.consumable2.serialize() if player.consumable2 else None,
        'player_consumable3': player.consumable3.serialize() if player.consumable3 else None,
        'enemy': enemy.serialize() if enemy else None,
        'name': enemy.persona.name if enemy else None
    }

    return jsonify(window_data)

@app.route("/attack/", methods=['POST', 'GET'])
def attack():
    player = db_session.query(PlayerData).first()

    enemy = (db_session.query(CharacterData).filter(CharacterData.player_id == player.id).
             filter(CharacterData.x == player.x, CharacterData.y == player.y)).first()

    weapon = player.weapon.equipment
    #armor = enemy.armor.equipment
    armor = None

    damage = (
        max(0, (weapon.slash if weapon else 0)     * player.level - (armor.slash if armor else 0)    * enemy.persona.level) +
        max(0, (weapon.pierce if weapon else 0)    * player.level - (armor.pierce if armor else 0)   * enemy.persona.level) +
        max(0, (weapon.blunt if weapon else 0)     * player.level - (armor.blunt if armor else 0)    * enemy.persona.level) +
        max(0, (weapon.fire if weapon else 0)      * player.level - (armor.fire if armor else 0)     * enemy.persona.level) +
        max(0, (weapon.ice if weapon else 0)       * player.level - (armor.poison if armor else 0)   * enemy.persona.level) +
        max(0, (weapon.poison if weapon else 0)    * player.level - (armor.poison if armor else 0)   * enemy.persona.level) +
        max(0, (weapon.electric if weapon else 0)  * player.level - (armor.electric if armor else 0) * enemy.persona.level)
    )

    print(f'damage: {damage}')

    print(f'enemy health: {enemy.health}')
    enemy.health -= damage
    print(f'enemy health: {enemy.health}')

    player_message = f'Вы атаковали {enemy.persona.name} и нанесили {damage} урона.'
    enemy_message = f'{enemy.persona.name} атаковал Вас нанеся {damage} урона.'

    if (enemy.health <= 0):
        enemy.health = 0
        enemy.is_alive = False

    # Сохраняем изменения в базе данных
    db_session.commit()
    time.sleep(0.2)

    attack_data = {
        'name': enemy.persona.name,
        'player_message': player_message,
        'character_message': enemy_message
    }

    return jsonify(attack_data)

def game_satus(player):
    # Если игрок стоит рядом с персонажем
    character = (db_session.query(CharacterData).filter(CharacterData.player_id == player.id).
                 filter(CharacterData.x == player.x, CharacterData.y == player.y)).first()

    if (character):
        if character.loyalty == ENEMY:
            return GAME_STATUS[1]
        else:
            return GAME_STATUS[2]

    return GAME_STATUS[0]


@app.route('/get-inventory/', methods=['GET'])
def get_inventory():
    player = db_session.query(PlayerData).first()

    # Retrieve inventories and items
    inventories = player.items
    items = [inventory.item for inventory in inventories]

    # Serialize inventories and items
    inventories_data = [inventory.serialize() for inventory in inventories]
    items_data = [item.serialize() for item in items]

    # Prepare response data
    response_data = {
        "inventory": inventories_data,
        "items": items_data,
        "weapon": player.weapon.serialize() if player.weapon else None,
        "armor": player.armor.serialize() if player.armor else None,
        "consumable1": player.consumable1.serialize() if player.consumable1 else None,
        "consumable2": player.consumable2.serialize() if player.consumable2 else None,
        "consumable3": player.consumable3.serialize() if player.consumable3 else None
    }

    return jsonify(response_data)

@app.route('/get-item/', methods=['GET', 'POST'])
def get_item():
    player = db_session.query(PlayerData).first()

    if request.method == 'POST':
        item_index = int(request.form.get('item'))  # Assuming 'item' is an index
        if 0 <= item_index < len(player.items):
            return jsonify(player.items[item_index].item.serialize())
        else:
            return jsonify({'error': 'Invalid item index'})

@app.route("/register/", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Проверка на совпадение паролей
        if password != confirm_password:
            error = 'Пароли не совпадают!'

        # Проверка на длину пароля
        elif len(password) < 8:
            error = 'Пароль должен содержать как минимум 8 символов!'

        # Проверка наличия заглавных и строчных букв, а также цифр в пароле
        elif not any(char.isupper() for char in password) or \
             not any(char.islower() for char in password) or \
             not any(char.isdigit() for char in password):
            error = 'Пароль должен содержать хотя бы одну заглавную букву, одну строчную букву и одну цифру!'

        # Проверка уникальности логина
        elif PlayerData.query.filter_by(login=login).first():
            error = 'Такой логин уже существует!'

        # Проверка логина на соответствие критериям
        elif not match("^[a-zA-Z][a-zA-Z0-9]{3,15}$", login):
            error = 'Логин должен начинаться с буквы, состоять только из букв и цифр и иметь длину от 4 до 16 символов!'


        else:
            player = PlayerData(login=login, password=password)
            db_session.add(player)
            db_session.commit()
            login_user(player)
            flash('Успешная регистрация!', 'success')
            return redirect(url_for('index'))  # Redirect to another page after successful registration
    return render_template('register.htm', error=error)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        player = PlayerData.query.filter_by(login=username).first()
        # Проверка ваших пользователей и паролей, например:
        if not player or not player.check_password(password):
            error = 'Неправильное имя пользователя или пароль. Пожалуйста, попробуйте еще раз.'
        else:
            # Здесь вы можете добавить логику для входа пользователя, например, установить сеанс входа
            login_user(player)
            flash('Успешный вход!', 'success')
            return redirect(url_for('index'))
    return render_template('login.htm', error=error)

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
    flash('Вы успешно вышли!', 'success')
    return redirect(url_for('index'))


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('register'))
    return response
