import pytest

from Backend.Domain.Notifications.Publisher import Publisher
from Backend.Tests.Unit.stubs.Subscriber_stub import Subscriber_stub


def test_subscribe():
    publisher = Publisher()
    subscriber = Subscriber_stub(lambda: ())
    subscriber_count = len(publisher.get_subscribers())
    publisher.subscribe(subscriber)
    assert len(publisher.get_subscribers()) == subscriber_count + 1

def test_unsubscribe():
    publisher = Publisher()
    subscriber = Subscriber_stub(lambda: ())
    subscriber_count = len(publisher.get_subscribers())
    publisher.subscribe(subscriber)
    publisher.remove_subscriber(subscriber)
    assert len(publisher.get_subscribers()) == subscriber_count


def test_notify():
    has_been_notified = ""
    publisher = Publisher()

    def notified(message):
        nonlocal has_been_notified
        has_been_notified = message
    subscriber = Subscriber_stub(lambda message: notified(message))
    publisher.subscribe(subscriber)
    publisher.notify_all("message")
    assert has_been_notified == "message"
