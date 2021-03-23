class Responsibility:

    def __init__(self):
        pass

    def add_new_product(store_id, product_information, quantity):
        return False

    def remove_product(store_id, product_id):
        return False

    def change_product_quantity(store_id, product_id, new_quantity):
        return False

    def edit_product_details(store_id, product_id, new_details):
        return False

    def appoint_new_store_owner(store_id, new_owner_id):
        return False

    def appoint_new_store_manager(self, store_id, new_manager_id):
        return False

    def edit_managers_responsibilities(self, store_id, manager_id, responsibilities): # TODO: Change the parameters according to responsibilities representation
        return False

    def dismiss_manager(self, store_id, manager_id):
        return False

    def get_store_personnel_info(self, store_id):
        return False

    def get_store_purchase_history(self, store_id):
        return False