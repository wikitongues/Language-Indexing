import re
import unittest

import language_indexing.config.config_keys as keys
from language_indexing.config.load_configs import read_logging_settings
from language_indexing.language_indexing_config import LanguageIndexingConfiguration, Title


class TestLoadConfigs(unittest.TestCase):
    def test_read_logging_settings(self):
        config = LanguageIndexingConfiguration()
        expected_log_file = "log_file.log"
        expected_log_level = "INFO"
        setattr(config, keys.LOGGING_SECTION, Title())
        setattr(
            config[keys.LOGGING_SECTION],
            keys.LOG_FILE_KEY,
            expected_log_file,
        )
        setattr(
            config[keys.LOGGING_SECTION],
            keys.LOG_FILE_APPEND_KEY,
            "True",
        )
        setattr(
            config[keys.LOGGING_SECTION],
            keys.LOG_LEVEL_KEY,
            expected_log_level,
        )

        logging_settings = read_logging_settings(config)

        self.assertEqual(expected_log_file, logging_settings.log_file)
        self.assertTrue(logging_settings.log_file_append)
        self.assertEqual(expected_log_level, logging_settings.log_level)

    def test_read_logging_settings_no_append(self):
        config = LanguageIndexingConfiguration()
        expected_log_file = "log_file.log"
        expected_log_level = "INFO"
        setattr(config, keys.LOGGING_SECTION, Title())
        setattr(
            config[keys.LOGGING_SECTION],
            keys.LOG_FILE_KEY,
            expected_log_file,
        )
        setattr(
            config[keys.LOGGING_SECTION],
            keys.LOG_LEVEL_KEY,
            expected_log_level,
        )

        logging_settings = read_logging_settings(config)

        self.assertEqual(expected_log_file, logging_settings.log_file)
        self.assertFalse(logging_settings.log_file_append)
        self.assertEqual(expected_log_level, logging_settings.log_level)

    def test_read_logging_settings_invalid_log_level(self):
        config = LanguageIndexingConfiguration()
        expected_log_level = "INFOO"
        setattr(config, keys.LOGGING_SECTION, Title())
        setattr(
            config[keys.LOGGING_SECTION],
            keys.LOG_LEVEL_KEY,
            expected_log_level,
        )

        with self.assertRaisesRegex(
            ValueError,
            re.escape(
                "Invalid log level INFOO. Valid log levels are ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']."
            ),
        ):
            read_logging_settings(config)
