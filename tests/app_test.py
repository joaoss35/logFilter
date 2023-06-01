import unittest

import app


class LogFilterEngineTest(unittest.TestCase):

    def test_when_log_level_is_two_should_return_all_three_markers(self):
        logs = [
            "2023-05-30 15:57:55,410 WARNING: The system is running out of memory",
            "2023-05-30 15:57:50,390 INFO: The server is running smoothly",
            "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"
        ]

        engine = app.LogFilterEngine()
        engine.update_log_level(2)
        filtered_logs = engine.filter_logs(logs)
        self.assertEqual(filtered_logs, logs)

    def test_when_log_level_is_one_should_return_only_correct_markers(self):
        logs = [
            "2023-05-30 15:57:55,410 WARNING: The system is running out of memory",
            "2023-05-30 15:57:50,390 INFO: The server is running smoothly",
            "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"
        ]
        engine = app.LogFilterEngine()
        engine.update_log_level(1)
        filtered_logs = engine.filter_logs(logs)
        self.assertEqual(
            filtered_logs,
            [
                "2023-05-30 15:57:55,410 WARNING: The system is running out of memory",
                "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"
            ]
        )

    def test_when_log_level_is_zero_should_return_only_error_marker(self):
        logs = [
            "2023-05-30 15:57:55,410 WARNING: The system is running out of memory",
            "2023-05-30 15:57:50,390 INFO: The server is running smoothly",
            "2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"
        ]
        engine = app.LogFilterEngine()
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
        engine = app.LogFilterEngine()
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
        engine = app.LogFilterEngine()
        engine.last_printed_line = 2
        engine.update_log_level(2)
        filtered_logs = engine.filter_logs(logs)
        self.assertEqual(
            filtered_logs,
            ["2023-05-30 15:56:40,303 ERROR: Failed to connect to the database"]
        )

    def test_when_log_level_zero_is_updated_to_one_should_update_log_level_to_one(self):
        engine = app.LogFilterEngine()
        engine.log_level = 0
        engine.update_log_level(1)
        self.assertEqual(engine.log_level, 1)

    def test_when_log_level_one_is_updated_to_three_log_level_should_be_two(self):
        engine = app.LogFilterEngine()
        engine.log_level = 1
        engine.update_log_level(2)
        self.assertEqual(engine.log_level, 2)

    def test_when_markers_level_zero_is_updated_to_one_should_update_markers_level_to_one(self):
        engine = app.LogFilterEngine()
        engine.markers = []
        engine.update_log_level(1)
        self.assertEqual(engine.log_level, 1)

    def test_when_log_level_is_zero_should_return_updated_error_marker(self):
        engine = app.LogFilterEngine()
        engine.markers = []
        engine.log_level = 0
        engine.update_markers_level()
        self.assertEqual(
            engine.markers,
            ["ERROR"]
        )

    def test_when_log_level_is_one_should_return_updated_error_and_warning_marker(self):
        engine = app.LogFilterEngine()
        engine.markers = []
        engine.log_level = 1
        engine.update_markers_level()
        self.assertEqual(
            engine.markers,
            ["ERROR", "WARNING"]
        )

    def test_when_log_level_is_two_should_return_all_markers(self):
        engine = app.LogFilterEngine()
        engine.markers = []
        engine.log_level = 2
        engine.update_markers_level()
        self.assertEqual(
            engine.markers,
            ["ERROR", "WARNING", "INFO"]
        )


if __name__ == "__main__":
    unittest.main()
