
class MemberStub():

	def __init__(self) -> None:
		self.store_responsibility = {}

	def get_username(self):
		return "member"

	def add_responsibility(self, responsibility, store_id):
		self.store_responsibility[store_id] = responsibility
