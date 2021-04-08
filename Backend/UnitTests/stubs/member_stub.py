
import Backend.Domain.TradingSystem.member


class MemberStub(Backend.Member):

	def __init__(self, username = "member") -> None:
		self.store_responsibility = {}
		self.appoints = []
		self.username = username

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
		
