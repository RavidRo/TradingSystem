
from threading import Lock
from sqlalchemy import Column, Integer, Sequence, Index, String, Table, ForeignKey, ForeignKeyConstraint, Float
from sqlalchemy.orm import relationship, remote, foreign, column_property
from sqlalchemy_json import MutableJson
from sqlalchemy_utils import LtreeType, Ltree
from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import engine, session, mapper_registry
from Backend.Domain.TradingSystem.Interfaces.IDiscount import IDiscount
from Backend.Domain.TradingSystem.TypesPolicies.discounts import MaximumCompositeDiscount, AddCompositeDiscount, \
    XorCompositeDiscount, AndConditionDiscount, OrConditionDiscount, SimpleDiscount, Discounter
from Backend.response import Response
from Backend.rw_lock import ReadWriteLock
from sqlalchemy import func

discounts_id_seq = Sequence('rules_id_seq')


class DiscountsHandler(IHandler):
    _lock = Lock()
    _instance = None

    @staticmethod
    def get_instance():
        with DiscountsHandler._lock:
            if DiscountsHandler._instance is None:
                DiscountsHandler._instance = DiscountsHandler()
        return DiscountsHandler._instance

    def __init__(self):

        super().__init__(ReadWriteLock(), IDiscount)

        self.__discounts_table = Table('discounts', mapper_registry.metadata,
                                            Column('id', Integer, discounts_id_seq, primary_key=True),
                                            Column('path', LtreeType, nullable=False),
                                            Column('type', String(50)),
                                            Column('context', MutableJson),
                                            Column('context_obj', String(50)),
                                            Column('context_id', String(50)),
                                            Column('condition_id', Integer),
                                            Column('decision_rule', String(10)),
                                            Column('conditions_policy_root_id', String(10)),
                                            Column('discounter_data', MutableJson),
                                            Index('ix_discounts_path', 'path', postgresql_using='gist'))

        mapper_registry.map_imperatively(IDiscount, self.__discounts_table, properties={
            '_id': self.__discounts_table.c.id,
            'path': self.__discounts_table.c.path,
            'parent': relationship(
                'IDiscount',
                primaryjoin=(remote(self.__discounts_table.c.path) == foreign(
                    func.subpath(self.__discounts_table.c.path, 0, -1))),
                backref='_children',
                viewonly=True
            ),
            "_conditions_policy_root_id": column_property(self.__discounts_table.c.conditions_policy_root_id),
            "_context_obj": column_property(self.__discounts_table.c.context_obj),
            "_context_id": column_property(self.__discounts_table.c.context_id),
            "_context": column_property(self.__discounts_table.c.context),
            "_condition_id": column_property(self.__discounts_table.c.condition_id),
            "_decision_rule": column_property(self.__discounts_table.c.decision_rule),
            "_discounter_data": self.__discounts_table.c.discounter_data,
        }, polymorphic_on=self.__discounts_table.c.type)

        mapper_registry.map_imperatively(MaximumCompositeDiscount, self.__discounts_table, inherits=IDiscount,
                                         polymorphic_identity='MaximumCompositeDiscount')

        mapper_registry.map_imperatively(AddCompositeDiscount, self.__discounts_table, inherits=IDiscount,
                                         polymorphic_identity='AddCompositeDiscount')

        mapper_registry.map_imperatively(XorCompositeDiscount, self.__discounts_table, inherits=IDiscount,
                                         polymorphic_identity='XorCompositeDiscount')

        mapper_registry.map_imperatively(AndConditionDiscount, self.__discounts_table, inherits=IDiscount,
                                         polymorphic_identity='AndConditionDiscount')

        mapper_registry.map_imperatively(OrConditionDiscount, self.__discounts_table, inherits=IDiscount,
                                         polymorphic_identity='OrConditionDiscount')

        mapper_registry.map_imperatively(SimpleDiscount, self.__discounts_table, inherits=IDiscount,
                                         polymorphic_identity='SimpleDiscount')

    def remove_rule(self, discount_rule):
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            whole_subtree = session.query(IDiscount).filter(
                IDiscount.path.descendant_of(discount_rule.path)).all()
            session.delete(discount_rule)
            for rule_child in whole_subtree:
                session.delete(rule_child)
            res = Response(True)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res