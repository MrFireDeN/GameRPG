# -*- coding: UTF-8 -*-
from sqlalchemy import Column,  Integer, Float, Date,  DateTime, Text, Boolean, String, ForeignKey, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, query_expression
from sqlalchemy.sql import func
from database import Base, db_session, engine as db_engine
import datetime

class ActorData(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)

    # Поля персонажа
    name = Column(String(20), nullable=False, default="")
    level = Column(Integer, nullable=False, default=1)
    ep = Column(Integer, nullable=False, default=0)
    health = Column(Integer, nullable=False)
    max_health = Column(Integer, nullable=False, default=100)
    is_alive = Column(Boolean, default=True)

    # Координаты
    x = Column(Integer, nullable=False, default=0)
    y = Column(Integer, nullable=False, default=0)

    items = relationship("Inventory", back_populates="actor")

    #battle_id = Column(Integer, ForeignKey('battles.id'), doc="Сражение")
    #battle = relationship("BattleData", back_populates="actors")

    note = Column(Text, doc="Описание")

class InventoryData(Base):
    __tablename__ = 'inventories'
    id = Column(Integer, primary_key=True)

    capacity = Column(Integer, nullable=False, default=10)
    is_eqiup = Column(Boolean, default=False)

    actor_id = Column(Integer, ForeignKey('actors.id'), doc="Персонаж")
    item_id = Column(Integer, ForeignKey('items.id'), doc="Предмет")
    actor = relationship("ActorData", back_populates="items")
    item = relationship("ItemData", back_populates="actors")

class ItemData(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)

    name = Column(String(20), nullable=False, default="")
    level = Column(Integer, nullable=False, default=1)
    value = Column(Integer, nullable=False, default=1)

    actor = relationship("InventoryData", back_populates="item")

    #transform_id = Column(Integer, ForeignKey('transforms.id'), doc="Координаты")
    #transform = relationship("TransformData", back_populates="items")

    note = Column(Text, doc="Описание")

class PlayerData(ActorData):
    pass

class EnemyData(ActorData):
    pass

# class EquipmentData(Base):
#     __tablename__ = 'equipments'
#     id = Column(Integer, primary_key=True)
#
#     weapon_id = Column(Integer, ForeignKey('weapons.id'), doc="Оружие")
#     armor_id = Column(Integer, ForeignKey('armors.id'), doc="Броня")
#     consumable_id = Column(Integer, ForeignKey('consumables.id'), doc="Расходник")
#
#     weapon = relationship("WeaponData", back_populates="equipments")
#     armor = relationship("ArmorData", back_populates="equipments")
#     consumable = relationship("ConsumableData", back_populates="equipments")

# class BattleData(Base):
#     __tablename__ = 'battles'
#     id = Column(Integer, primary_key=True)
#
#     player_id = Column(Integer, ForeignKey('player.id'), doc="Персонаж")
#     enemy_id = Column(Integer, ForeignKey('enemies.id'), doc="Персонаж")
#
#     player = relationship("PlayerData", back_populates="battles")
#     enemy = relationship("EnemyData", back_populates="battles")



# class WeaponData(ItemData):
#     super.__tablename__ = "weapons"
#
#     slash = Column(Integer, nullable=False, default=0)
#     pierce = Column(Integer, nullable=False, default=0)
#     blunt = Column(Integer, nullable=False, default=0)
#     fire = Column(Integer, nullable=False, default=0)
#     ice = Column(Integer, nullable=False, default=0)
#     poison = Column(Integer, nullable=False, default=0)
#     electric = Column(Integer, nullable=False, default=0)
#
# class ArmorData(ItemData):
#     super.__tablename__ = "armors"
#
#     slash = Column(Integer, nullable=False, default=0)
#     pierce = Column(Integer, nullable=False, default=0)
#     blunt = Column(Integer, nullable=False, default=0)
#     fire = Column(Integer, nullable=False, default=0)
#     ice = Column(Integer, nullable=False, default=0)
#     poison = Column(Integer, nullable=False, default=0)
#     electric = Column(Integer, nullable=False, default=0)
#
# class ConsumableData(ItemData):
#     super.__tablename__ = "consumables"
#
#     type = Column(Integer, default=0)
#
#     pass

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
