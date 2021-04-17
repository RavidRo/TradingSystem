class IUserState:

    use_mock = False

    def create_guest(user):
        from Backend.Domain.TradingSystem.States.guest import Guest
        from Backend.Tests.stubs import MemberStub

        return MemberStub(user=user) if IUserState.use_mock else Guest(user)
