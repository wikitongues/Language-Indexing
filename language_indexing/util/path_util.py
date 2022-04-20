import os


def abspath(path: str) -> str:
    return os.path.expanduser(path) if path else None
