import logging
import sys


def get_logger(name: str = "quantumleap"):
    """
    Centralized production logger.

    ✔ timestamped logs
    ✔ readable in Railway/Vercel logs
    ✔ reusable across app
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # prevent duplicate handlers

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "[%(asctime)s] | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
