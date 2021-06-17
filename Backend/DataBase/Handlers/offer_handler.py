from threading import Lock

from sqlalchemy import Column, String, Float, ForeignKey, Table, ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy_json import MutableJson

from Backend.DataBase.IHandler import IHandler
from Backend.DataBase.database import mapper_registry
from Backend.Domain.TradingSystem.offer import Offer, OfferStatus, UndeclaredOffer, AwaitingApprovalOffer, \
    CounteredOffer, ApprovedOffer, RejectedOffer, UsedOffer, CanceledOffer
from Backend.rw_lock import ReadWriteLock


class OfferHandler(IHandler):
    _lock = Lock()
    _instance = None

    def __init__(self):
        super().__init__(ReadWriteLock(), Offer)

        self.__offer_statuses = Table('offer_statuses', mapper_registry.metadata,
                                      Column('status', String(30)),
                                      Column('offer_id', String(50), ForeignKey("offers.offer_id"), primary_key=True))

        mapper_registry.map_imperatively(OfferStatus, self.__offer_statuses,
                                         polymorphic_on=self.__offer_statuses.c.status,
                                         polymorphic_identity='status')

        mapper_registry.map_imperatively(UndeclaredOffer, self.__offer_statuses, inherits=OfferStatus,
                                         polymorphic_identity='undeclared')

        mapper_registry.map_imperatively(AwaitingApprovalOffer, self.__offer_statuses, inherits=OfferStatus,
                                         polymorphic_identity='awaiting manager approval')

        mapper_registry.map_imperatively(CounteredOffer, self.__offer_statuses, inherits=OfferStatus,
                                         polymorphic_identity='counter offered')

        mapper_registry.map_imperatively(ApprovedOffer, self.__offer_statuses, inherits=OfferStatus,
                                         polymorphic_identity='approved')

        mapper_registry.map_imperatively(RejectedOffer, self.__offer_statuses, inherits=OfferStatus,
                                         polymorphic_identity='rejected')

        mapper_registry.map_imperatively(UsedOffer, self.__offer_statuses, inherits=OfferStatus,
                                         polymorphic_identity='used')

        mapper_registry.map_imperatively(CanceledOffer, self.__offer_statuses, inherits=OfferStatus,
                                         polymorphic_identity='canceled')

        self.__offers = Table('offers', mapper_registry.metadata,
                              Column('offer_id', String(50), primary_key=True),
                              Column('price', Float(50)),
                              Column('product_id', String(50), ForeignKey("products.product_id")),
                              Column('product_name', String(30)),
                              Column('store_id', String(50), ForeignKey("stores.store_id")),
                              Column('store_name', String(50)),
                              Column('username', String(30), ForeignKey('members.username')),
                              Column('pending_owners_approval', MutableJson)
                              )

        mapper_registry.map_imperatively(Offer, self.__offers, properties={
            '_Offer__id': self.__offers.c.offer_id,
            '_Offer__price': self.__offers.c.price,
            '_Offer__store_id': self.__offers.c.store_id,
            '_Offer__store_name': self.__offers.c.store_name,
            '_Offer__product_id': self.__offers.c.product_id,
            '_Offer__product_name': self.__offers.c.product_name,
            '_Offer__username': self.__offers.c.username,
            '_Offer__status': relationship(OfferStatus, uselist=False, backref=backref("_offer", uselist=False),
                                           cascade="save-update, merge, delete, delete-orphan"),
            '_Offer__pending_owners_approval': self.__offers.c.pending_owners_approval
        })

    @staticmethod
    def get_instance():
        with OfferHandler._lock:
            if OfferHandler._instance is None:
                OfferHandler._instance = OfferHandler()
        return OfferHandler._instance
