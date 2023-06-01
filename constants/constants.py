class CONSTANTS(enumerate):
    LOGS_DIRECTORY = "/var/log/app"
    LOGS_PATTERN = "*.log"
    NO_LOGS_FOUND_TEXT = "No log files found. Exiting..."
    NO_MARKERS_FOUND_TEXT = "Please define a valid LOG_LEVEL value. Exiting..."
    MARKERS = ["ERROR", "WARNING", "INFO"]
    ERROR_OPENING_LOG_FILE_TEXT = "Error opening log file"
