import uuid

from Backend.response import Parsable, Response

from Backend.Service.DataObjects.offer_data import OfferData

from Backend.Domain.Notifications.Publisher import Publisher


class Offer(Parsable):
    def __init__(self, user, store, product) -> None:
        self.__id: str = str(uuid.uuid4())
        self.__price: float = None
        self.__status: OfferStatus = UndeclaredOffer(self)
        product.add_offer(self)

        # used for parsing
        self.__store_id = store.get_id()
        self.__store_name = store.get_name()
        self.__product_name = product.get_name()
        self.__product_id = product.get_id()
        self.__username = user.get_username().get_obj().value

        self.__user_publisher = Publisher()
        self.__user_publisher.subscribe(user)
        self.__managers_publisher = Publisher()
        self.__managers_publisher.subscribe(store)
        self.__pending_owners_approval = {}
        owners_names = store.get_owners_names()
        for id in owners_names:
            self.__pending_owners_approval[id] = False

    def declare_price(self, price) -> Response[None]:
        for id in self.__pending_owners_approval:
            self.__pending_owners_approval[id] = False
        response = self.__status.declare_price(price)
        if response.succeeded():
            self.__managers_publisher.notify_all(
                f"{self.__username} has submitted a price offer for {self.__product_name}"
            )
        return response

    def suggest_counter_offer(self, price) -> Response[None]:
        response = self.__status.suggest_counter_offer(price)
        if response.succeeded():
            self.__user_publisher.notify_all(
                f"Your price offer for {self.__product_name} has been countered"
            )
        return response

    def approve_manager_offer(self) -> Response[None]:
        return self.__status.approve_manager_offer()

    def approve_user_offer(self, owner_id) -> Response[None]:
        self.__pending_owners_approval[owner_id] = True
        notify = lambda: self.__user_publisher.notify_all(
            f"Your price offer for {self.__product_name} has been approved"
        )
        return self.__status.approve_user_offer(self.__pending_owners_approval, notify)

    def reject_user_offer(self) -> Response[None]:
        response = self.__status.reject_user_offer()
        if response.succeeded():
            self.__user_publisher.notify_all(
                f"Your price offer for {self.__product_name} has been rejected"
            )
        return response

    def cancel_offer(self) -> Response[None]:
        return self.__status.cancel_offer()

    def use(self) -> Response[None]:
        return self.__status.use()

    def is_approved(self) -> bool:
        return self.__status.is_approved()

    def get_status_name(self) -> str:
        return self.__status.get_name()

    def change_status(self, status):
        self.__status = status

    def get_id(self) -> str:
        return self.__id

    def set_price(self, price) -> Response[None]:
        if price < 0:
            return Response(False, msg="Can't set an offer price to a negative value")
        self.__price = price
        return Response(True)

    def get_price(self) -> float:
        return self.__price

    def get_username(self) -> str:
        return self.__username

    def parse(self):
        owners = list(self.__pending_owners_approval.keys())
        awaiting_owners = list(
            filter(lambda owner: not self.__pending_owners_approval[owner], owners)
        )

        return OfferData(
            self.__id,
            self.__price,
            self.__status.get_name(),
            self.__store_id,
            self.__store_name,
            self.__product_id,
            self.__product_name,
            self.__username,
            awaiting_owners,
        )


class OfferStatus:
    def __init__(self, offer: Offer) -> None:
        self._offer = offer

    def declare_price(self, price) -> Response[None]:
        return Response(
            False,
            msg=f"Can't declare a price on an offer with {self.get_name()} status",
        )

    def suggest_counter_offer(self, price) -> Response[None]:
        return Response(
            False,
            msg=f"Can't suggest a counter offer to an offer with {self.get_name()} status",
        )

    def approve_manager_offer(self) -> Response[None]:
        return Response(
            False,
            msg=f"Can't approve an offer with {self.get_name()} status",
        )

    def approve_user_offer(self, pending_owners, notify) -> Response[None]:
        return Response(
            False,
            msg=f"Can't approve an offer with {self.get_name()} status",
        )

    def reject_user_offer(self) -> Response[None]:
        return Response(
            False,
            msg=f"Can't reject an offer with {self.get_name()} status",
        )

    def cancel_offer(self) -> Response[None]:
        return Response(
            False,
            msg=f"Can't cancel an offer with {self.get_name()} status",
        )

    def use(self) -> Response[None]:
        return Response(
            False,
            msg=f"Can't use an offer with {self.get_name()} status",
        )

    def get_name(self) -> str:
        raise NotImplementedError

    def is_approved(self) -> bool:
        return False

    def change_status(self, status_class) -> Response[None]:
        self._offer.change_status(status_class(self._offer))
        return Response(True)


class UndeclaredOffer(OfferStatus):
    def declare_price(self, price) -> Response[None]:
        response = self._offer.set_price(price)
        if not response.succeeded():
            return response
        return self.change_status(AwaitingApprovalOffer)

    def cancel_offer(self) -> Response[None]:
        return self.change_status(CancledOffer)

    def get_name(self) -> str:
        return "undeclared"


class AwaitingApprovalOffer(OfferStatus):
    def suggest_counter_offer(self, price) -> Response[None]:
        response = self._offer.set_price(price)
        if not response.succeeded():
            return response
        return self.change_status(CounteredOffer)

    def approve_user_offer(self, owners_dict, notify) -> Response[None]:
        if all(owners_dict.values()):
            notify()
            return self.change_status(ApprovedOffer)
        else:
            return Response(True)

    def reject_user_offer(self) -> Response[None]:
        return self.change_status(RejectedOffer)

    def cancel_offer(self) -> Response[None]:
        return self.change_status(CancledOffer)

    def get_name(self) -> str:
        return "awaiting manager approval"


class CounteredOffer(OfferStatus):
    def declare_price(self, price) -> Response[None]:
        response = self._offer.set_price(price)
        if not response.succeeded():
            return response
        return self.change_status(AwaitingApprovalOffer)

    def approve_manager_offer(self) -> Response[None]:
        return self.change_status(ApprovedOffer)

    def cancel_offer(self) -> Response[None]:
        return self.change_status(CancledOffer)

    def get_name(self) -> str:
        return "counter offered"


class ApprovedOffer(OfferStatus):
    def use(self) -> Response[None]:
        return self.change_status(UsedOffer)

    def get_name(self) -> str:
        return "approved"

    def is_approved(self) -> bool:
        return True


class RejectedOffer(OfferStatus):
    def get_name(self) -> str:
        return "rejected"


class UsedOffer(OfferStatus):
    def get_name(self) -> str:
        return "used"


class CancledOffer(OfferStatus):
    def get_name(self) -> str:
        return "cancled"
