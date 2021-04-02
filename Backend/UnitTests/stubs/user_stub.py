
from .member_stub import MemberStub
from ...Domain.TradingSystem.IUser import IUser

class UserStub(IUser):

	def __init__(self) -> None:
		self.state = MemberStub()

	def is_appointed(self, store_id):
		return self.state.is_appointed(store_id)
		return store_id in self.appoints

	def appoint(self, store_id):
		return self.state.appoint(store_id)
		self.appoints.append(store_id)
		