
from threading import Lock
from sqlalchemy import Column, Integer, Sequence, Index, String, Table, ForeignKey, ForeignKeyConstraint, Float
from sqlalchemy.orm import relationship, remote, foreign, column_property
from sqlalchemy_utils import LtreeType, Ltree
from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import engine, session, mapper_registry, db_fail_response
from Backend.Domain.TradingSystem.Interfaces.IDiscount import IDiscount
from Backend.Domain.TradingSystem.TypesPolicies.discounts import MaximumCompositeDiscount, AddCompositeDiscount, \
    XorCompositeDiscount, AndConditionDiscount, OrConditionDiscount, SimpleDiscount, Discounter
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
                                            Column('context', String(50)),
                                            Column('context_obj', String(50)),
                                            Column('context_id', String(50)),
                                            Column('condition_id', Integer),
                                            Column('decision_rule', String(10)),
                                            Column('conditions_policy_root_id', String(10)),
                                            Index('ix_rules_path', 'path', postgresql_using='gist'),
                                            ForeignKeyConstraint(('id', 'context_obj'), ['discounters.discount_id', 'discounters.type']))

        self.__discounters_table = Table('discounters', mapper_registry.metadata,
                                            Column('discount_id', Integer, discounts_id_seq, foreign_key=ForeignKey('discounts.id') ,primary_key=True),
                                            Column('identifier', String(50)),
                                            Column('type', String(50), primary_key=True),
                                            Column('multiplier', Float))

        mapper_registry.map_imperatively(IDiscount, self.__discounts_table, properties={
            '_id': self.__discounts_table.c.id,
            'path': self.__discounts_table.c.path,
            'parent': relationship(
                'PurchaseRule',
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
            "_discount_strategy": relationship(Discounter, uselist=False)
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

