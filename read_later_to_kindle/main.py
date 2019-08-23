from digest import DigestFactory
from pinboard import PinboardQueueConsumer
from send_to_kindle import send_to_kindle


def main():
    pinboard_queue = PinboardQueueConsumer()
    factory = DigestFactory()
    entries = pinboard_queue.get_last_unread()
    digest_path, log_path = factory.create_digest(entries)
    send_to_kindle(digest_path, log_path)


if __name__ == "__main__":
    main()
