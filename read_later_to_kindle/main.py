from digest import DigestFactory
from pinboard import PinboardQueueConsumer
from send_to_kindle import send_to_kindle


def main(digest_size):
    pinboard_queue = PinboardQueueConsumer(digest_size)
    factory = DigestFactory()
    entries = pinboard_queue.get_last_unread()
    digest_path, log_path = factory.create_digest(entries)
    send_to_kindle(digest_path, log_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Create and send Kindle-readable digests from a read-it-later service"
    )
    parser.add_argument(
        "--digest-size",
        type=int,
        default="25",
        help="number of links to process for the digest",
    )
    args = parser.parse_args()
    main(args.digest_size)
