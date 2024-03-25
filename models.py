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
ENEMY = False
FRIEND = True

# Игкрок
class PlayerData(Base, UserMixin):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)

    login = Column(String(32), unique=True)
    password = Column(String(64))

    # Поля персонажа
    level       = Column(Integer, default=1)
    ep          = Column(Integer, default=0)
    max_health  = Column(Integer, default=100)
    health      = Column(Integer, default=max_health)
    is_alive    = Column(Boolean, default=True)

    # Координаты
    x = Column(Integer, default=0)
    y = Column(Integer, default=0)

    # Снаряжение
    weapon_id = Column(Integer, ForeignKey('items.id'), doc="Оружие")
    armor_id = Column(Integer, ForeignKey('items.id'), doc="Броня")
    consumable1_id = Column(Integer, ForeignKey('items.id'), doc="Предмет 1")
    consumable2_id = Column(Integer, ForeignKey('items.id'), doc="Предмет 2")
    consumable3_id = Column(Integer, ForeignKey('items.id'), doc="Предмет 3")
    weapon = relationship("ItemData", foreign_keys=[weapon_id])
    armor = relationship("ItemData", foreign_keys=[armor_id])
    consumable1 = relationship("ItemData", foreign_keys=[consumable1_id])
    consumable2 = relationship("ItemData", foreign_keys=[consumable2_id])
    consumable3 = relationship("ItemData", foreign_keys=[consumable3_id])

    # Инвентарь
    #items = relationship("PlayerInventory", back_populates="player")

    @manager.user_loader
    def load_player(player_id):
        return PlayerData.query.get(player_id)

# Персонаж
class PersonaData(Base):
    __tablename__ = 'personas'
    id = Column(Integer, primary_key=True)

    # Поля персонажа
    name        = Column(String(20), nullable=False)
    level       = Column(Integer, default=1)
    max_health  = Column(Integer, default=100)
    note = Column(Text, doc="Описание")

# НПС
class CharacterData(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)

    # С каким игроком связан
    persona_id = Column(Integer, ForeignKey('personas.id'))
    persona = relationship("PersonaData")

    # Поля персонажа
    health      = Column(Integer, nullable=False)
    is_alive    = Column(Boolean, default=True)
    loyalty     = Column(Boolean, default=FRIEND)

    # Координаты
    x = Column(Integer, default=0)
    y = Column(Integer, default=0)

    # Инвентарь
    items = relationship("CharacterInventory")

    # С каким игроком связан
    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship("PlayerData")

# Предмет
class ItemData(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)

    # Поля предмета
    name    = Column(String(20), nullable=False)
    value   = Column(Integer, default=1)

    equipment_id = Column(Integer, ForeignKey('equipments.id'))
    equipment = relationship("EquipmentData")
    consumable_id = Column(Integer, ForeignKey('consumables.id'))
    consumable = relationship("ConsumableData")

    note = Column(Text, doc="Описание")

class PlayerInventory(Base):
    __tablename__ = 'players_inventory'
    id = Column(Integer, primary_key=True)

    level       = Column(Integer, default=1)
    is_eqiup    = Column(Boolean, default=False)

    player_id   = Column(Integer, ForeignKey('players.id'))
    item_id     = Column(Integer, ForeignKey('items.id'), doc="Предмет")

class CharacterInventory(Base):
    __tablename__ = 'characters_inventory'
    id = Column(Integer, primary_key=True)

    level       = Column(Integer, default=1)
    is_eqiup    = Column(Boolean, default=False)

    character_id= Column(Integer, ForeignKey('characters.id'))
    item_id     = Column(Integer, ForeignKey('items.id'), doc="Предмет")
    characters  = relationship("CharacterData")
    item        = relationship("ItemData")

# Снаряжение
class EquipmentData(Base):
    __tablename__ = "equipments"
    id = Column(Integer, primary_key=True)

    type = Column(Boolean, nullable=WEAPON)

    slash       = Column(Integer, default=0)
    pierce      = Column(Integer, default=0)
    blunt       = Column(Integer, default=0)
    fire        = Column(Integer, default=0)
    ice         = Column(Integer, default=0)
    poison      = Column(Integer, default=0)
    electric    = Column(Integer, default=0)

class ConsumableData(Base):
    __tablename__ = "consumables"
    id = Column(Integer, primary_key=True)

    type = Column(Integer, nullable=False)

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

    # С каким игроком связан
    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship("PlayerData")

    def open_door(self):
        self.is_open = True

    def close_door(self):
        self.is_open = False

    def lock_door(self):
        self.is_locked = True

    def unlock_door(self):
        self.is_locked = False

# Квесты
class QuestData(Base):
    __tablename__ = 'quests'
    id = Column(Integer, primary_key=True)

    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)

    # Связь с прогрессом квеста для каждого игрока
    progress = relationship("QuestProgress")

# Прогресс квеста для каждого игрока
class QuestProgress(Base):
    __tablename__ = 'quests_progress'
    id = Column(Integer, primary_key=True)

    # Состояние квеста для конкретного игрока
    is_completed = Column(Boolean, default=False)

    player_id = Column(Integer, ForeignKey('players.id'))
    quest_id = Column(Integer, ForeignKey('quests.id'))
    player = relationship("PlayerData")
    quest = relationship("QuestData")

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
