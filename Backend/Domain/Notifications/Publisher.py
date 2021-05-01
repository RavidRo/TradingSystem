from Backend.Domain.TradingSystem.Interfaces.Subscriber import Subscriber


class Publisher:

    def __init__(self):
        self.subscribers = []

    def subscribe(self,  subscriber: Subscriber):
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: Subscriber):
        self.subscribers.remove(subscriber)

    def notify_all(self, message):
        for subscriber in self.subscribers:
            subscriber.notify(message)
