from Backend.Domain.TradingSystem.user_state import UserState
from Backend.Domain.Authentication.authentication import Authentication

class Guest(UserState):

    def __init__(self, user):
        super().__init__(user)
        self.authentication = Authentication.get_instance()

    def login(self, username, password):
        # Assumption: User holds the function change_state and the different states of the user.
        # TODO: ask Sunshine about the return value type
        msg = self.authentication.login(username, password)
        if msg == "succeeded":
            self.user.change_state(user.member_state)
        # TODO: need to induce if an admin was logged in - ask Sunshine
        return msg

    def register(self, username, password):
        return self.authentication.register(username, password)

    def open_store(self, store_id, store_parameters): # TODO: Change the parameters according to actual store's data
        raise RuntimeError('A store cannot be opened by a guest')

    # In contrary to the requirements, guests can see their RAM history (can be complex because all store's history is saved in DB and we need to ingore if the buyer was a guest).

    # TODO: Check if cart actions should be here (e.g: member's cart needs to be saved)

    def add_new_product(self, store_id, product_information, quantity): # TODO: Change the parameters according to actual product's data
        raise RuntimeError('Guests cannot add products to stores')

    def remove_product(self, store_id, product_id):
        raise RuntimeError('Guests cannot remove products from stores')

    def change_product_quantity(self, store_id, product_id, new_quantity):
        raise RuntimeError("Guests cannot change store product's quantity")

    def edit_product_details(self, store_id, product_id, new_details): # TODO: Change the parameters according to actual product's data
        raise RuntimeError("Guests cannot edit store product's details")

    def appoint_new_store_owner(self, store_id, new_owner_id):
        raise RuntimeError("Guests cannot appoint new store owners")

    def appoint_new_store_manager(self, store_id, new_manager_id):
        raise RuntimeError("Guests cannot appoint new store managers")

    def edit_managers_responsibilities(self, store_id, manager_id, responsibilities): # TODO: Change the parameters according to responsibilities representation
        raise RuntimeError("Guests cannot edit a stores manager's responsibilities")

    def dismiss_manager(self, store_id, manager_id):
        raise RuntimeError("Guests cannot dismiss managers")

    def get_store_personnel_info(self, store_id):
        raise RuntimeError("Guests cannot get store personnel information")

    def get_store_purchase_history(self, store_id):
        raise RuntimeError("Guests cannot get store's purchase history")

    def get_any_store_purchase_history(self, store_id):
        raise RuntimeError("Guests cannot get any store's purchase history")

    def get_user_purchase_history(self, user_id):
        raise RuntimeError("Guests cannot get any user's purchase history")