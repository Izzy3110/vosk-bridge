import os
import sys
import time


class Logger:
    _current_prefix = None
    _current_filepath = None
    loggers = {}

    def __init__(self, log_prefix, log_filepath):
        self._current_prefix = log_prefix
        self._current_filepath = log_filepath
        self.add_prefix()

    def add_prefix(self):
        print("log: "+self._current_prefix)
        print("pth: "+self._current_filepath)
        if self._current_prefix not in self.loggers.keys():
            self.loggers[self._current_prefix] = {
                "filepath": self._current_filepath,
                "f": None
            }

    def log_to_prefix(self, prefix, message):
        if prefix in self.loggers:
            current_t = time.time()

            if "messages" not in self.loggers[prefix].keys():
                self.loggers[prefix]["messages"] = {}
            self.loggers[prefix]["messages"][str(int(current_t))] = message
            if self.loggers[prefix]["f"] is None:
                self.loggers[prefix]["f"] = open(self.loggers[prefix]["filepath"], "a" if os.path.isfile(self.loggers[prefix]["filepath"]) else "w")
            if sys.platform == "win32":
                self.loggers[prefix]["f"].write(message + "\r\n")
            else:
                self.loggers[prefix]["f"].write(message+"\n")
            if self.loggers[prefix]["f"] is not None:
                self.loggers[prefix]["f"].close()
