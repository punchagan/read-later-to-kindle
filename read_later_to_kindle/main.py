from digest import DigestFactory
from pinboard import PinboardQueueConsumer


def main():
    pinboard_queue = PinboardQueueConsumer()
    factory = DigestFactory()
    entries = pinboard_queue.get_last_unread()
    factory.create_digest(entries)


if __name__ == "__main__":
    main()
