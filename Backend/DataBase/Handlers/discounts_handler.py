discounts_id_seq = Sequence('rules_id_seq')

class DiscountsHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):

        super().__init__(ReadWriteLock(), Discount)

        self.__discounts_table = Table('discounts', mapper_registry.metadata,
                                            Column('id', Integer, rules_id_seq, primary_key=True),
                                            Column('path', LtreeType, nullable=False),
                                            Column('type', String(50)),
                                            Column('context', String(50)),
                                            Column('context_obj', String(50)), #TODO: check about those fields
                                            Column('context_id', String(50)),
                                            Column('condition_id', Integer),
                                            Column('decision_rule', String(10)),
                                            Index('ix_rules_path', 'path', postgresql_using='gist'),
                                            ForeignKeyConstraint(('id', 'context_obj'), ['discounters.discount_id', 'discounters.type']))

        self.__discounters_table = Table('discounters', mapper_registry.metadata,
                                            Column('discount_id', Integer, discounts_id_seq, foreign_key=ForeignKey('discounts.id') ,primary_key=True),
                                            Column('identifier', String(50)),
                                            Column('type', String(50), primary_key=True),
                                            Column('multiplier', Float))