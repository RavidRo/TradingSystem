from Backend.Domain.TradingSystem.States.member import Member


def update_field(function):
    def inner(self, *args, **kwargs):
        self.__setattr__(f"_{function.__name__}", True)
        return True

    return inner


class MemberStub(Member):
    def __init__(self, username="member", user=None) -> None:
        self.store_responsibility = {}
        self.appoints = []
        self.username = username
        self.user = user

    def get_username(self):
        return self.username

    def add_responsibility(self, responsibility, store_id):
        self.store_responsibility[store_id] = responsibility

    def is_appointed(self, store_id):
        return (store_id in self.store_responsibility) or (store_id in self.appoints)

    def appoint(self, store_id):
        self.appoints.append(store_id)

    def dismiss_from_store(self, store_id):
        if store_id in self.appoints:
            self.appoints.remove(store_id)
        if store_id in self.store_responsibility:
            del self.store_responsibility[store_id]

    @update_field
    def register():
        pass

    @update_field
    def login():
        pass

    @update_field
    def save_product_in_cart():
        pass

    @update_field
    def show_cart():
        pass

    @update_field
    def delete_from_cart():
        pass

    @update_field
    def change_product_quantity_in_cart():
        pass

    @update_field
    def buy_cart():
        pass

    @update_field
    def delete_products_after_purchase():
        pass

    @update_field
    def get_cart_price():
        pass

    @update_field
    def open_store():
        pass

    @update_field
    def get_purchase_history():
        pass

    @update_field
    def add_new_product():
        pass

    @update_field
    def remove_product():
        pass

    @update_field
    def change_product_quantity_in_store():
        pass

    @update_field
    def edit_product_details():
        pass

    @update_field
    def appoint_new_store_owner():
        pass

    @update_field
    def appoint_new_store_manager():
        pass

    @update_field
    def add_manager_permission():
        pass

    @update_field
    def remove_manager_permission():
        pass

    @update_field
    def dismiss_manager():
        pass

    @update_field
    def get_store_personnel_info():
        pass

    @update_field
    def get_store_purchase_history():
        pass

    @update_field
    def get_user_purchase_history_admin():
        pass

    @update_field
    def get_any_store_purchase_history_admin():
        pass
