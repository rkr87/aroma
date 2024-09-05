"""
Template script.
"""
import logging.config


def main() -> None:
    """
    Setup environment
    """
    logging.config.fileConfig(r".\logging.conf")


if __name__ == "__main__":
    main()
