from typing import Optional

VALID_LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LoggingSettings:
    def __init__(self, log_file: Optional[str], log_file_append: Optional[bool], log_level: Optional[str]) -> None:
        if log_level is not None and log_level not in VALID_LOG_LEVELS:
            raise ValueError(f"Invalid log level {log_level}. Valid log levels are {VALID_LOG_LEVELS}.")

        self.log_file = log_file
        self.log_file_append = log_file_append
        self.log_level = log_level
