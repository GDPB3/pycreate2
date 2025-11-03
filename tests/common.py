import pytest
import logging
import sys


@pytest.fixture(scope="session", autouse=True)
def logging_setup():
    # To stderr
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
    )
    yield
