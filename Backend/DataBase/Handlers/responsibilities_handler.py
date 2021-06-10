from threading import Lock

from sqlalchemy import Column, Integer, Sequence, Index
from sqlalchemy import func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, remote, foreign
from sqlalchemy_utils import LtreeType, Ltree

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import engine, session, Base
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility
from Backend.rw_lock import ReadWriteLock

id_seq = Sequence('nodes_id_seq')


class Responsibility_DAL(Base):
    __tablename__ = 'responsibilities'

    id = Column(Integer, id_seq, primary_key=True)
    # name = Column(String, nullable=False)
    path = Column(LtreeType, nullable=False)

    parent = relationship(
                'Responsibility_DAL',
                primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
                backref='children',
                viewonly=True
            )

    __table_args__ = (
        Index('ix_nodes_path', path, postgresql_using='gist'),)

    def __init__(self, parent=None):
        _id = engine.execute(id_seq)
        self.id = _id
        ltree_id = Ltree(str(_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id

Base.metadata.create_all(engine)

class ResponsibilitiesHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock(), Responsibility)

    @staticmethod
    def get_instance():
        with ResponsibilitiesHandler._lock:
            if ResponsibilitiesHandler._instance is None:
                ResponsibilitiesHandler._instance = ResponsibilitiesHandler()
        return ResponsibilitiesHandler._instance

    def save_res(self, parent=None):
        responsibility_dal = Responsibility_DAL(parent)
        session.add(responsibility_dal)
        session.commit()
        return responsibility_dal
