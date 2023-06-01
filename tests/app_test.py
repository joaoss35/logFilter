import unittest
from unittest.mock import mock_open, patch

import app
import constants.constants as constants


class LogFilterEngineTest(unittest.TestCase):

    def test_when_log_level_is_two_should_return_all_three_markers(self):
        logs = [
            "2023-05-30 15:57:55,410 WARNING: The system is running out of memory",
            "2023-05-30 15:57:50,390 INFO: The server is running smoothly",
            "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"
        ]

        engine = app.LogFilterEngine(log_file_names=["/var/log/app/mock.log"])
        engine.update_log_level(2)
        filtered_logs = engine.filter_logs(logs)
        self.assertEqual(filtered_logs, logs)

    def test_when_log_level_is_one_should_return_only_correct_markers(self):
        logs = [
            "2023-05-30 15:57:55,410 WARNING: The system is running out of memory",
            "2023-05-30 15:57:50,390 INFO: The server is running smoothly",
            "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"
        ]
        engine = app.LogFilterEngine(log_file_names=["/var/log/app/mock.log"])
        engine.update_log_level(1)
        filtered_logs = engine.filter_logs(logs)
        self.assertEqual(
            filtered_logs,
            [
                "2023-05-30 15:57:55,410 WARNING: The system is running out of memory",
                "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"
            ]
        )

    def test_when_log_level_is_five_should_return_empty_list(self):
        logs = [
            "2023-05-30 15:57:55,410 WARNING: The system is running out of memory",
            "2023-05-30 15:57:50,390 INFO: The server is running smoothly",
            "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"
        ]
        engine = app.LogFilterEngine(log_file_names=["/var/log/app/mock.log"])
        engine.update_log_level(5)
        filtered_logs = engine.filter_logs(logs)
        self.assertEqual(filtered_logs, [])

    def test_when_number_of_logs_is_five_and_last_printed_line_is_two_should_return_last_two_lines(self):
        logs = [
            "2023-05-30 15:57:55,410 WARNING: The system is running out of memory",
            "2023-05-30 15:57:50,390 INFO: The server is running smoothly",
            "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database",
            "2023-05-30 15:56:40,303 WARNING: The system is running out of memory",
            "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"
        ]
        engine = app.LogFilterEngine(log_file_names=["/var/log/app/mock.log"])
        engine.update_log_level(2)
        engine.last_printed_line = 3
        filtered_logs = engine.filter_logs(logs)
        self.assertEqual(
            filtered_logs,
            ["2023-05-30 15:56:40,303 WARNING: The system is running out of memory",
             "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"]
        )

    def test_when_log_level_is_zero_should_return_only_error_marker(self):
        logs = [
            "2023-05-30 15:57:55,410 WARNING: The system is running out of memory",
            "2023-05-30 15:57:50,390 INFO: The server is running smoothly",
            "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"
        ]
        engine = app.LogFilterEngine(log_file_names=["/var/log/app/mock.log"])
        engine.update_log_level(0)
        filtered_logs = engine.filter_logs(logs)
        self.assertEqual(
            filtered_logs,
            [
                "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"
            ]
        )

    def test_when_no_logs_are_provided_and_log_level_is_two_should_return_no_new_logs(self):
        logs = [
            "2023-05-30 15:57:55,410 WARNING: The system is running out of memory",
            "2023-05-30 15:57:50,390 INFO: The server is running smoothly",
            "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"
        ]
        engine = app.LogFilterEngine(log_file_names=["/var/log/app/mock.log"])
        engine.last_printed_line = 3
        engine.update_log_level(2)
        filtered_logs = engine.filter_logs(logs)
        self.assertEqual(
            filtered_logs,
            []
        )

    def test_when_one_new_log_is_provided_should_return_only_last_log(self):
        logs = [
            "2023-05-30 15:57:55,410 WARNING: The system is running out of memory",
            "2023-05-30 15:57:50,390 INFO: The server is running smoothly",
            "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"
        ]
        engine = app.LogFilterEngine(log_file_names=["/var/log/app/mock.log"])
        engine.last_printed_line = 2
        engine.update_log_level(2)
        filtered_logs = engine.filter_logs(logs)
        self.assertEqual(
            filtered_logs,
            ["2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"]
        )


if __name__ == "__main__":
    unittest.main()
