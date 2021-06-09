from Backend.Domain.TradingSystem.Interfaces.Subscriber import Subscriber


class Publisher:
    def __init__(self):
        self.__subscribers = []

    def subscribe(self, subscriber: Subscriber):
        self.__subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: Subscriber):
        if subscriber in self.__subscribers:
            self.__subscribers.remove(subscriber)

    def notify_all(self, data, subject="message"):
        for subscriber in self.__subscribers:
            print({"subject": subject, "data": data})
            subscriber.notify({"subject": subject, "data": data})

    def get_subscribers(self):
        return self.__subscribers