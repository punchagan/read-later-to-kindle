from digest import DigestFactory
from pinboard import PinboardQueueConsumer


def main(digest_size, dry_run):
    pinboard_queue = PinboardQueueConsumer(digest_size)
    factory = DigestFactory(dry_run)
    entries = pinboard_queue.get_last_unread()
    factory.create_digest(entries)


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
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="do a dry run of the digest creation",
    )
    args = parser.parse_args()
    main(args.digest_size, args.dry_run)
