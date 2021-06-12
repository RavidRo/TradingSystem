from threading import Lock

from sqlalchemy import Column, Integer, Sequence, Index, String, Table, ForeignKey
from sqlalchemy import func, create_engine
from sqlalchemy import TypeDecorator, cast
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.orm import relationship, remote, foreign, column_property
from sqlalchemy_utils import LtreeType, Ltree
import re
from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import engine, session, mapper_registry, db_fail_response
from Backend.Domain.TradingSystem.Responsibilities.responsibility import Responsibility, Permission
from Backend.response import Response, PrimitiveParsable
from Backend.rw_lock import ReadWriteLock

rules_id_seq = Sequence('rules_id_seq')


class PurchaseRulesHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.composite_purchase_rule import PurchaseRule
        from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.concrete_composites import \
            OrCompositePurchaseRule, \
            AndCompositePurchaseRule, ConditioningCompositePurchaseRule
        from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.concrete_leaf import UserLeafPurchaseRule, \
            ProductLeafPurchaseRule, CategoryLeafPurchaseRule, BagLeafPurchaseRule
        super().__init__(ReadWriteLock(), PurchaseRule)

        self.__purchase_rules_table = Table('purchase_rules', mapper_registry.metadata,
                                              Column('id', Integer, rules_id_seq, primary_key=True),
                                              Column('path', LtreeType, nullable=False),
                                              Column('type', String(10)),
                                              Column('store_id', ForeignKey('stores.store_id', ondelete="CASCADE")),
                                              Index('ix_rules_path', 'path', postgresql_using='gist'))

        mapper_registry.map_imperatively(PurchaseRule, self.__purchase_rules_table, properties={
            'id': self.__purchase_rules_table.c.id,
            'path': self.__purchase_rules_table.c.path,
            'parent': relationship(
                'PurchaseRule',
                primaryjoin=(remote(self.__purchase_rules_table.c.path) == foreign(
                    func.subpath(self.__purchase_rules_table.c.path, 0, -1))),
                backref='_children',
                viewonly=True
            ),
        }, polymorphic_on=self.__purchase_rules_table.c.type)

        mapper_registry.map_imperatively(OrCompositePurchaseRule, self.__purchase_rules_table, inherits=PurchaseRule,
                                         polymorphic_identity='OrComposite')

        mapper_registry.map_imperatively(AndCompositePurchaseRule, self.__purchase_rules_table, inherits=PurchaseRule,
                                         polymorphic_identity='AndComposite')

        mapper_registry.map_imperatively(ConditioningCompositePurchaseRule, self.__purchase_rules_table, inherits=PurchaseRule,
                                         polymorphic_identity='ConditioningComposite')

        mapper_registry.map_imperatively(UserLeafPurchaseRule, self.__purchase_rules_table,
                                         inherits=PurchaseRule,
                                         polymorphic_identity='UserLeaf')

        mapper_registry.map_imperatively(ProductLeafPurchaseRule, self.__purchase_rules_table,
                                         inherits=PurchaseRule,
                                         polymorphic_identity='ProductLeaf')

        mapper_registry.map_imperatively(CategoryLeafPurchaseRule, self.__purchase_rules_table,
                                         inherits=PurchaseRule,
                                         polymorphic_identity='CategoryLeaf')

        mapper_registry.map_imperatively(BagLeafPurchaseRule, self.__purchase_rules_table,
                                         inherits=PurchaseRule,
                                         polymorphic_identity='BagLeaf')

    @staticmethod
    def get_instance():
        with PurchaseRulesHandler._lock:
            if PurchaseRulesHandler._instance is None:
                PurchaseRulesHandler._instance = PurchaseRulesHandler()
        return PurchaseRulesHandler._instance

