class ProxyBridge(Bridge):
    real: Bridge = None
    def __init__(self):
