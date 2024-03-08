# -*- coding: UTF-8 -*-
from sqlalchemy import Column,  Integer, Float, Date,  DateTime, Text, Boolean, String, ForeignKey, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, query_expression
from sqlalchemy.sql import func
from database import Base, db_session, engine as db_engine
import datetime

class PersonaData(Base):
    __tablename__ = 'personas'
    id = Column(Integer, primary_key=True)

    # Поля персонажа
    name        = Column(String(20), nullable=False, default="")
    level       = Column(Integer, nullable=False, default=1)
    ep          = Column(Integer, nullable=False, default=0)
    health      = Column(Integer, nullable=False)
    max_health  = Column(Integer, nullable=False, default=100)
    is_alive    = Column(Boolean, default=True)

    # Координаты
    x = Column(Integer, nullable=False, default=0)
    y = Column(Integer, nullable=False, default=0)

    # Снаряжение
    weapon_id       = Column(Integer, ForeignKey('weapons.id'), doc="Оружие")
    armor_id        = Column(Integer, ForeignKey('armors.id'), doc="Оружие")
    consumable1_id  = Column(Integer, ForeignKey('consumables.id'), doc="Оружие")
    consumable2_id  = Column(Integer, ForeignKey('consumables.id'), doc="Оружие")
    consumable3_id  = Column(Integer, ForeignKey('consumables.id'), doc="Оружие")
    weapon          = relationship("WeaponData", back_populates="persona")
    armor           = relationship("ArmorData", back_populates="persona")
    consumable1     = relationship("ConsumableData", back_populates="persona")
    consumable2     = relationship("ConsumableData", back_populates="persona")
    consumable3     = relationship("ConsumableData", back_populates="persona")

    # Инвентарь
    items = relationship("InventoryData", back_populates="persona")

    # Описание
    note = Column(Text, doc="Описание")

class InventoryData(Base):
    __tablename__ = 'inventories'
    id = Column(Integer, primary_key=True)

    capacity = Column(Integer, nullable=False, default=10)
    is_eqiup = Column(Boolean, default=False)

    actor_id    = Column(Integer, ForeignKey('personas.id'), doc="Персонаж")
    item_id     = Column(Integer, ForeignKey('items.id'), doc="Предмет")
    actor       = relationship("PersonaData", back_populates="items")
    item        = relationship("ItemData", back_populates="personas")

class ItemData(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)

    name    = Column(String(20), nullable=False, default="")
    level   = Column(Integer, nullable=False, default=1)
    value   = Column(Integer, nullable=False, default=1)

    # Координаты
    x = Column(Integer, nullable=False, default=0)
    y = Column(Integer, nullable=False, default=0)

    actor = relationship("InventoryData", back_populates="item")

    note = Column(Text, doc="Описание")

class PlayerData(PersonaData):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)

    persona_id = Column(Integer, ForeignKey('personas.id'))
    persona = relationship("PersonaData", back_populates="players")

class EnemyData(PersonaData):
    __tablename__ = 'enemies'
    id = Column(Integer, primary_key=True)

    persona_id = Column(Integer, ForeignKey('personas.id'))
    persona = relationship("PersonaData", back_populates="enemies")

class WeaponData(Base):
    __tablename__ = "weapons"
    id = Column(Integer, primary_key=True)

    item_id = Column(Integer, ForeignKey('items.id'))
    item = relationship("ItemData", back_populates="weapons")

    slash = Column(Integer, nullable=False, default=0)
    pierce = Column(Integer, nullable=False, default=0)
    blunt = Column(Integer, nullable=False, default=0)
    fire = Column(Integer, nullable=False, default=0)
    ice = Column(Integer, nullable=False, default=0)
    poison = Column(Integer, nullable=False, default=0)
    electric = Column(Integer, nullable=False, default=0)

class ArmorData(Base):
    __tablename__ = "armors"
    id = Column(Integer, primary_key=True)

    item_id = Column(Integer, ForeignKey('items.id'))
    item = relationship("ItemData", back_populates="armors")

    slash = Column(Integer, nullable=False, default=0)
    pierce = Column(Integer, nullable=False, default=0)
    blunt = Column(Integer, nullable=False, default=0)
    fire = Column(Integer, nullable=False, default=0)
    ice = Column(Integer, nullable=False, default=0)
    poison = Column(Integer, nullable=False, default=0)
    electric = Column(Integer, nullable=False, default=0)

class ConsumableData(Base):
    __tablename__ = "consumables"
    id = Column(Integer, primary_key=True)

    item_id = Column(Integer, ForeignKey('items.id'))
    item = relationship("ItemData", back_populates="weapons")

    type = Column(Integer, default=0)

#Стены
class WallData(Base):
    __tablename__ = 'walls'
    id = Column(Integer, primary_key=True)

    # Координаты
    x = Column(Integer, nullable=False, default=0)
    y = Column(Integer, nullable=False, default=0)

# Двери
class DoorData(Base):
    __tablename__ = 'doors'
    id = Column(Integer, primary_key=True)

    # Координаты
    x = Column(Integer, nullable=False, default=0)
    y = Column(Integer, nullable=False, default=0)

    is_open     = Column(Boolean, default=False)
    is_locked   = Column(Boolean, default=False)

    def __init__(self):
        super().__init__()
    def open_door(self):
        self.is_open = True

    def close_door(self):
        self.is_open = False

    def lock_door(self):
        self.is_locked = True

    def unlock_door(self):
        self.is_locked = False

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
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
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
