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


def app():
    log_file_names = find(constants.CONSTANTS.LOGS_PATTERN, constants.CONSTANTS.LOGS_DIRECTORY)
    last_printed_line = 0

    if not log_file_names:
        print(constants.CONSTANTS.NO_LOGS_FOUND_TEXT)
        sys.exit(0)

    # Keep listening on the log files for any incoming logs.
    while True:
        try:
            with open(log_file_names[0], "r") as log_file:
                file_lines = log_file.readlines()

                # Print only new unprinted lines
                for i in range(last_printed_line, len(file_lines)):
                    line = file_lines[i]
                    if any(marker in line for marker in constants.CONSTANTS.MARKERS):
                        sys.stdout.write(line)
                        last_printed_line = i + 1
        except (FileNotFoundError, PermissionError, OSError) as e:
            logging.error("%s: %s", constants.CONSTANTS.ERROR_OPENING_LOG_FILE_TEXT, e, exc_info=True)
            sys.exit(1)

        # Sleep for a second to avoid hogging the CPU.
        time.sleep(1)


if __name__ == "__main__":
    app()
