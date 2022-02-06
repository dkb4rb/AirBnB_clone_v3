#!/usr/bin/python3
"""Module: DBStorage, new engine"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.orm import Session, query
from sqlalchemy.sql.functions import user
from models.base_model import Base, BaseModel
from os import getenv
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity


class DBStorage:
    """New engine DBStorage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializing DBStorage"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, db),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """all method, to querying on current d.base"""
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit al changesof the current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current db session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_f = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_f)
        self.__session = Session()
