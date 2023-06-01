import os
import fnmatch
import time
import sys

import constants.constants as constants

class LogFilterEngine:
    log_file_names: list
    last_printed_line: int = 0
    log_level: int
    markers: list
    error: str = ""

    # log_file_names needs to be None by default because of the tests and to be able to mock the logs files
    def __init__(self, log_file_names=None):
        if log_file_names is None:
            log_file_names = self.find(constants.CONSTANTS.LOGS_PATTERN, constants.CONSTANTS.LOGS_DIRECTORY)

        self.log_file_names = log_file_names

        self.update_log_level(int(os.environ.get('LOG_LEVEL', '0')))

        if not self.log_file_names:
            self.error = constants.CONSTANTS.NO_LOGS_FOUND_TEXT

        if not self.markers:
            self.error = constants.CONSTANTS.NO_MARKERS_FOUND_TEXT

    def find(self, pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result

    def run(self):
        file_line = self.get_log_files()

        if self.error != "":
            return

        for log in self.filter_logs(file_line):
            sys.stdout.write(log)

    def update_markers_level(self):
        match self.log_level:
            case 0:
                self.markers = [constants.CONSTANTS.MARKERS[0]]
            case 1:
                self.markers = constants.CONSTANTS.MARKERS[:2]
            case 2:
                self.markers = constants.CONSTANTS.MARKERS
            case _:
                self.markers = []

    def update_log_level(self, log_level: int):
        self.log_level = log_level
        self.update_markers_level()

    def get_log_files(self) -> list:
        try:
            with open(self.log_file_names[0], "r") as log_file:
                return log_file.readlines()
        except (FileNotFoundError, PermissionError, OSError) as e:
            self.error = constants.CONSTANTS.ERROR_OPENING_LOG_FILE_TEXT
        except Exception as e:
            self.error = constants.CONSTANTS.ERROR_UNKNOWN_EXCEPTION

    def filter_logs(self, log_lines) -> list:
        if self.error != "":
            return []

        new_filtered_logs = []
        for i in range(self.last_printed_line, len(log_lines)):
            line = log_lines[i]
            if any(marker in line for marker in self.markers):
                new_filtered_logs.append(line)
                self.last_printed_line = i + 1
        return new_filtered_logs


def app():
    log_engine = LogFilterEngine()

    # Keep listening on the log files for any incoming logs.
    while True:
        if log_engine.error != "":
            print(log_engine.error)
            sys.exit(1)

        log_engine.run()
        # Sleep for a second to avoid hogging the CPU.
        time.sleep(1)


if __name__ == "__main__":
    app()
