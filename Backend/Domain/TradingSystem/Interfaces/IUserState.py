class IUserState:

    use_mock = False

    def create_guest(user):
        from Backend.Domain.TradingSystem.States.guest import Guest
        from Backend.Tests.Unit.stubs.member_stub import MemberStub

        return MemberStub(user=user) if IUserState.use_mock else Guest(user)
