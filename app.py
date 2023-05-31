import logging
import os
import fnmatch
import time
import sys

import constants.constants as constants


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def get_markers_level(log_level) -> list:
    match log_level:
        case 0:
            markers = [constants.CONSTANTS.MARKERS[0]]
        case 1:
            markers = constants.CONSTANTS.MARKERS[:2]
        case 2:
            markers = constants.CONSTANTS.MARKERS
        case _:
            markers = []
    return markers



def app():
    log_file_names = find(constants.CONSTANTS.LOGS_PATTERN, constants.CONSTANTS.LOGS_DIRECTORY)
    last_printed_line = 0

    log_level = int(os.environ.get('LOG_LEVEL', '0'))
    markers = get_markers_level(log_level)

    if not log_file_names:
        print(constants.CONSTANTS.NO_LOGS_FOUND_TEXT)
        sys.exit(0)

    if not markers:
        print(constants.CONSTANTS.NO_MARKERS_FOUND_TEXT)
        sys.exit(0)

    # Keep listening on the log files for any incoming logs.
    while True:
        try:
            with open(log_file_names[0], "r") as log_file:
                file_lines = log_file.readlines()

                # Print only new unprinted lines
                for i in range(last_printed_line, len(file_lines)):
                    line = file_lines[i]
                    if any(marker in line for marker in markers):
                        sys.stdout.write(line)
                        last_printed_line = i + 1
        except (FileNotFoundError, PermissionError, OSError) as e:
            logging.error("%s: %s", constants.CONSTANTS.ERROR_OPENING_LOG_FILE_TEXT, e, exc_info=True)
            sys.exit(1)

        # Sleep for a second to avoid hogging the CPU.
        time.sleep(1)


if __name__ == "__main__":
    app()
