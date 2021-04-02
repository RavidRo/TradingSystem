
from Backend.Domain.TradingSystem.member import Member


class MemberStub(Member):

	def __init__(self) -> None:
		self.store_responsibility = {}
		self.appoints = []

	def get_username(self):
		return "member"

	def add_responsibility(self, responsibility, store_id):
		self.store_responsibility[store_id] = responsibility

	def is_appointed(self, store_id):
		return (store_id in self.store_responsibility) or (store_id in self.appoints)

	def appoint(self, store_id):
		self.appoints.append(store_id)
