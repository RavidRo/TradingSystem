import json
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
from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.composite_purchase_rule import PurchaseRule
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
                                              Column('type', String(50)),
                                              Column('clause', String(10)),
                                              Column('context', String(50)),
                                              Column('context_obj', String(50)),
                                              Column('context_id', String(50)),
                                              Column('comparator', String(50)),
                                              Column('constraint', Integer),
                                              Index('ix_rules_path', 'path', postgresql_using='gist'))

        mapper_registry.map_imperatively(PurchaseRule, self.__purchase_rules_table, properties={
            '_id': self.__purchase_rules_table.c.id,
            'path': self.__purchase_rules_table.c.path,
            'parent': relationship(
                'PurchaseRule',
                primaryjoin=(remote(self.__purchase_rules_table.c.path) == foreign(
                    func.subpath(self.__purchase_rules_table.c.path, 0, -1))),
                backref='_children',
                viewonly=True
            ),
            "_clause": column_property(self.__purchase_rules_table.c.clause),
            "_context_obj": column_property(self.__purchase_rules_table.c.context_obj),
            "_context_id": column_property(self.__purchase_rules_table.c.context_id),
            "_context": column_property(self.__purchase_rules_table.c.context),
            "_constraint": column_property(self.__purchase_rules_table.c.constraint),
            "_comparator": column_property(self.__purchase_rules_table.c.comparator),
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

    def remove_rule(self, rule):
        from Backend.Domain.TradingSystem.TypesPolicies.Purchase_Composites.composite_purchase_rule import PurchaseRule
        self._rwlock.acquire_write()
        res = Response(True)
        try:
            whole_subtree = session.query(PurchaseRule).filter(
                PurchaseRule.path.descendant_of(rule.path)).all()
            session.delete(rule)
            for rule_child in whole_subtree:
                session.delete(rule_child)
            res = Response(True)
        except Exception as e:
            session.rollback()
            res = Response(False, msg=str(e))
        finally:
            self._rwlock.release_write()
            return res

    def move_rule(self, rule: PurchaseRule, new_parent: PurchaseRule):
        self._rwlock.acquire_write()
        new_path = new_parent.path + Ltree(str(rule._id))
        session.flush()
        for n in rule._children:
            n.path = new_path + n.path[len(rule.path):]
        session.flush()
        rule.path = new_path
        session.flush()
        rule.parent = new_parent
        session.flush()
        new_parent._children.append(rule)
        session.flush()
        self._rwlock.release_write()

    def edit_rule(self, old_rule, edited_rule):
        self._rwlock.acquire_write()
        for n in old_rule._children:
            n.parent = edited_rule
            n.path = edited_rule.path + n.path[len(old_rule.path):]
            session.flush()
            edited_rule._children.append(n)
            session.flush()
        self._rwlock.release_write()
        self.remove_rule(old_rule)
        self.save(edited_rule)
        return Response(True)




    # def edit_rule(self, old_rule, rule_details):
    #     self._rwlock.acquire_write()
    #     res = Response(True)
    #     try:
    #         old_rule._context = json.dumps(rule_details['context'])
    #         old_rule._context_obj = rule_details['context']['obj']
    #         old_rule._context
    #         res = Response(True)
    #     except Exception as e:
    #         session.rollback()
    #         res = Response(False, msg=str(e))
    #     finally:
    #         self._rwlock.release_write()
    #         return res