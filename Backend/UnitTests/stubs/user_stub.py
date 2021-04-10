from .member_stub import MemberStub
from ...Domain.TradingSystem.IUser import IUser
from ...Domain.TradingSystem.user_state import UserState


class UserStub(IUser):

    def change_state(self, new_state: UserState) -> None:
        self.state = new_state

    def __init__(self, state=None) -> None:
        if state is None:
            state = MemberStub()
        self.state = state

    def is_appointed(self, store_id):
        return self.state.is_appointed(store_id)

    def appoint(self, store_id):
        return self.state.appoint(store_id)

    def get_username(self) -> str:
        return self.state.get_username()

    def is_guest(self):
        from ...Domain.TradingSystem.guest import Guest
        return isinstance(self.state, Guest)

    def is_member(self):
        from ...Domain.TradingSystem.member import Member
        return isinstance(self.state, Member)

    def is_admin(self):
        from ...Domain.TradingSystem.admin import Admin
        return isinstance(self.state, Admin)
