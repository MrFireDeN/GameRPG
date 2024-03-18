# -*- coding: UTF-8 -*-
from sqlalchemy import Column,  Integer, Float, Date,  DateTime, Text, Boolean, String, ForeignKey, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, query_expression
from sqlalchemy.sql import func
from database import Base, db_session, engine as db_engine
import datetime

# логин
from flask_login import UserMixin
from eng import manager

WEAPON = False
ARMOR = True

# Персонаж
class PersonaData(Base):
    __tablename__ = 'personas'
    id = Column(Integer, primary_key=True)

    # Поля персонажа
    name        = Column(String(20), nullable=False)
    level       = Column(Integer, default=1)
    ep          = Column(Integer, default=0)
    max_health  = Column(Integer, default=100)
    health      = Column(Integer, default=max_health)
    is_alive    = Column(Boolean, default=True)

    # Координаты
    x = Column(Integer, default=0)
    y = Column(Integer, default=0)

    # Снаряжение
    weapon_id       = Column(Integer, ForeignKey('items.id'), doc="Оружие")
    armor_id        = Column(Integer, ForeignKey('items.id'), doc="Броня")
    consumable1_id  = Column(Integer, ForeignKey('items.id'), doc="Предмет 1")
    consumable2_id  = Column(Integer, ForeignKey('items.id'), doc="Предмет 2")
    consumable3_id  = Column(Integer, ForeignKey('items.id'), doc="Предмет 3")
    weapon          = relationship("ItemData", back_populates="persona")
    armor           = relationship("ItemData", back_populates="persona")
    consumable1     = relationship("ItemData", back_populates="persona")
    consumable2     = relationship("ItemData", back_populates="persona")
    consumable3     = relationship("ItemData", back_populates="persona")

    # Инвентарь
    items = relationship("InventoryData", back_populates="persona")

    # Описание
    note = Column(Text, doc="Описание")

# Игкрок
class PlayerData(Base, UserMixin):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)

    login = Column(String(32), unique=True)
    password = Column(String(64))

    persona_id = Column(Integer, ForeignKey('personas.id'))
    persona = relationship("PersonaData", back_populates="players")

    # Прогресс квестов для игрока
    quest_progress = relationship("QuestProgress", back_populates="player")

# Персонаж
class CharacterData(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)

    persona_id = Column(Integer, ForeignKey('personas.id'))
    persona = relationship("PersonaData", back_populates="characters")


class PlayerEnemyAssociation(Base):
    __tablename__ = 'player_enemy_association'

    player_id = Column(Integer, ForeignKey('players.id'))
    enemy_id = Column(Integer, ForeignKey('enemies.id'))
    player = relationship("")

# Инвентарь
class InventoryData(Base):
    __tablename__ = 'inventories'
    id = Column(Integer, primary_key=True)

    is_eqiup = Column(Boolean, default=False)

    persona_id    = Column(Integer, ForeignKey('personas.id'), doc="Персонаж")
    item_id     = Column(Integer, ForeignKey('items.id'), doc="Предмет")
    actor       = relationship("PersonaData", back_populates="items")
    item        = relationship("ItemData", back_populates="personas")

# Предмет
class ItemData(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)

    name    = Column(String(20), nullable=False)
    value   = Column(Integer, default=1)

    # Координаты
    x = Column(Integer, default=0)
    y = Column(Integer, default=0)

    persona = relationship("InventoryData", back_populates="item")

    # Ссылки на друние сущности
    equipment_id = Column(Integer, ForeignKey('equipments.id'))
    consumable_id = Column(Integer, ForeignKey('consumables.id'))
    equipment = relationship("EquipmentData", back_populates="items")
    consumable = relationship("ConsumableData", back_populates="items")

    note = Column(Text, doc="Описание")

# Снаряжение
class EquipmentData(Base):
    __tablename__ = "equipments"
    id = Column(Integer, primary_key=True)

    type = Column(Boolean, nullable=False)

    level = Column(Integer, default=1)

    slash = Column(Integer, default=0)
    pierce = Column(Integer, default=0)
    blunt = Column(Integer, default=0)
    fire = Column(Integer, default=0)
    ice = Column(Integer, default=0)
    poison = Column(Integer, default=0)
    electric = Column(Integer, default=0)

# Расходник
class ConsumableData(Base):
    __tablename__ = "consumables"
    id = Column(Integer, primary_key=True)

    level = Column(Integer, default=1)

    type = Column(Integer, default=0)

#Стены
class WallData(Base):
    __tablename__ = 'walls'
    id = Column(Integer, primary_key=True)

    # Координаты
    x = Column(Integer, default=0)
    y = Column(Integer, default=0)

# Двери
class DoorData(Base):
    __tablename__ = 'doors'
    id = Column(Integer, primary_key=True)

    # Координаты
    x = Column(Integer, default=0)
    y = Column(Integer, default=0)

    is_open     = Column(Boolean, default=False)
    is_locked   = Column(Boolean, default=False)

    def open_door(self):
        self.is_open = True

    def close_door(self):
        self.is_open = False

    def lock_door(self):
        self.is_locked = True

    def unlock_door(self):
        self.is_locked = False

# Мир
class WorldData(Base):
    __tablename__ = 'worlds'
    id = Column(Integer, primary_key=True)

    # Связь с игроком
    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship("PlayerData", back_populates="worlds")



# Сообщения
class MessageData(Base):
    """реалмзует диалогувую систему"""
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)

    message = Column(Text, doc="Сообщение")

    author_id = Column(Integer, ForeignKey('characters.id'))
    quest_id = Column(Integer, ForeignKey('quests.id'))

    author = relationship("CharacterData", back_populates="messages")
    quest = relationship("QuestData", back_populates="messages")

# Квесты
class QuestData(Base):
    __tablename__ = 'quests'
    id = Column(Integer, primary_key=True)

    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)

    # Связь с прогрессом квеста для каждого игрока
    progress = relationship("QuestProgress", back_populates="quest")

# Прогресс квеста для каждого игрока
class QuestProgress(Base):
    __tablename__ = 'quest_progress'
    id = Column(Integer, primary_key=True)

    # Состояние квеста для конкретного игрока
    is_completed = Column(Boolean, default=False)
    player_id = Column(Integer, ForeignKey('players.id'))
    quest_id = Column(Integer, ForeignKey('quests.id'))

    player = relationship("PlayerData", back_populates="quest_progress")
    quest = relationship("QuestData", back_populates="progress")

@manager.user_loader
def load_player(player_id):
    return PlayerData.query.get(player_id)

# def example_1():
#     """
#     Добавляем группу в базу данных
#     """
#     g = Group(label = "ИСТ22-1", year=2022)
#     db_session.add(g)
#     db_session.commit()
#     print(g.id) # В этот момент у нас уже есть Id
#     # Добавляем студента
#     s = Student(
#             fio="Иванов И.И.",
#             birthday = datetime.date(1987, 4, 2),
#             sex = True,
#             group_id = g.id
#
#         )
#     db_session.add(s)
#     db_session.commit()
#     print(s.id) # Теперь у нас есть id студента
#
#
# def example_2():
#     """
#     Все тоже самое что и в 1 примере, но в одной транзакции
#     """
#     g = Group(label = "ИСТ22-1", year=2022)
#     db_session.add(g)
#     db_session.flush() # Вместо подтверждения транзакции мы вызываем данный метод
#     print(g.id) # В этот момент у нас уже есть Id
#     # Добавляем студента
#     s = Student(
#             fio="Иванов И.И.",
#             birthday = datetime.date(1987, 4, 2),
#             sex = True,
#             group_id = g.id
#
#         )
#     db_session.add(s)
#     db_session.commit()
#     print(s.id) # Теперь у нас есть id студента
#
# def example_3():
#     """
#     выборка данных
#     """
#     # Выбираем фамилии студенток и сортрируем по фио и идентификатору (последний в обратном порядке)
#     query = db_session.query(Student.fio)\
#                 .filter(Student.sex == True)\
#                 .order_by(Student.fio)\
#                 .order_by(Student.id.desc())
#     for fio, in query.all():
#         print(fio)
#
#     # Выбираем всех студентов поступивших после 2022 года
#     query = db_session.query(Student)\
#                 .join(Group)\
#                 .filter(Group.year >= 2022)
#     for s in query.all():
#         print(s.fio, s.group.year)

def init_db():
    from database import engine
    Base.metadata.create_all(bind=engine)
    db_session.commit()

def print_schema(table_class):
    from sqlalchemy.schema import CreateTable, CreateColumn
    print(str(CreateTable(table_class.__table__).compile(db_engine)))

def print_columns(table_class, *attrNames):
   from sqlalchemy.schema import CreateTable, CreateColumn
   c = table_class.__table__.c
   print( ',\r\n'.join((str( CreateColumn(getattr(c, attrName)).compile(db_engine)) \
                            for attrName in attrNames if hasattr(c, attrName)
               )))

if __name__ == "__main__":
    init_db()
    #print_columns(Payment, "created")
    #print_schema(SoltButton)
