from Backend.UnitTests.stubs.member_stub import MemberStub


from Backend.Domain.TradingSystem.guest import Guest


class IUserState:

    use_mock = False

    def create_guest(user):
        return MemberStub(user=user) if IUserState.use_mock else Guest(user)
