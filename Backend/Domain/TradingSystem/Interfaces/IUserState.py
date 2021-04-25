
class IUserState:
    use_mock = False

    def create_guest(user):
        from Backend.Tests.stubs.member_stub import MemberStub
        from Backend.Domain.TradingSystem.States.guest import Guest

        return MemberStub(user=user) if IUserState.use_mock else Guest(user)
