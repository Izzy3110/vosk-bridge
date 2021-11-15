import os
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from config import Vosk as VoskEnv


class VoskServer(threading.Thread):
    started = False
    running = True
    vosk_log_file_f = None
    vosk_log_file_name = "vosk.log"
    vosk_lines = []
    vosk_start_t = None
    socketio = None
    ps = None
    python_version = None
    logger_ = None

    def get_lines(self):
        return self.vosk_lines

    def log_to_file(self, line):
        if self.vosk_log_file_f is None:
            if not os.path.isdir("logs"):
                os.mkdir("logs")

            if not os.path.isfile(self.vosk_log_file_path):
                self.vosk_log_file_f = open(self.vosk_log_file_path, "w")
            else:
                self.vosk_log_file_f = open(self.vosk_log_file_path, "a")

        self.vosk_log_file_f.write(line + "\n")
        self.vosk_lines.append(line)
        self.vosk_log_file_f.close()
        self.vosk_log_file_f = None

    def __init__(self, socketio_):
        self.socketio = socketio_
        if self.vosk_log_file_f is None:
            parent_two = Path(__file__).parents[2]
            self.vosk_log_file_path = os.path.join(parent_two, "logs", self.vosk_log_file_name.rstrip(".log")+"-"+datetime.now().strftime("%Y%m%d_%H%M%S")+".log")
        print("logging to: "+self.vosk_log_file_path)
        if not os.path.isfile(self.vosk_log_file_path):
            from components.system.utils.logger import Logger
            self.logger_ = Logger("vosk", self.vosk_log_file_path)
        if os.path.isfile(self.vosk_log_file_path):
            self.vosk_log_file_f = open(self.vosk_log_file_path, "a")
        else:
            self.vosk_log_file_f = open(self.vosk_log_file_path, "w")

        self.vosk_start_t = time.time()
        self.vosk_lines = []
        super(VoskServer, self).__init__()

    def run(self) -> None:
        while self.running is True:
            if self.started is False:
                self.log_to_file("=> Starting Vosk Server ("+VoskEnv.script_filename+")")
                if sys.platform == "win32":
                    out_python_version = subprocess.check_output(["python", "-V"]).decode().rstrip("\r\n")
                    if len(out_python_version.splitlines()) == 1:
                        self.python_version = out_python_version.split("Python ")[1]
                        self.log_to_file("Python-Version: "+self.python_version)
                        self.logger_.log_to_prefix("vosk", "Python-Version: "+self.python_version)

                parent_one = Path(__file__).parents[1]
                vosk_server_filepath = os.path.join(parent_one, VoskEnv.script_foldername, VoskEnv.script_filename) if \
                    os.path.isfile(os.path.join(parent_one, VoskEnv.script_foldername, VoskEnv.script_filename)) else \
                    os.path.join("components", VoskEnv.script_foldername, VoskEnv.script_filename)
                if os.path.isfile(vosk_server_filepath):
                    self.log_to_file("platform: "+sys.platform)
                    py_executable_name = "python" if sys.platform == "win32" else "python3"
                    self.log_to_file("CMD-Exec: " + py_executable_name)
                    self.vosk_lines = [] if self.vosk_lines is None else self.vosk_lines
                    with subprocess.Popen(" ".join([py_executable_name, vosk_server_filepath]), shell=True,
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE) as self.ps:
                        while True:
                            error = self.ps.stderr.readline()
                            output = error
                            data_ = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3] + ": " + \
                                output.decode().rstrip("\r\n")
                            self.log_to_file(data_)
                            self.vosk_lines.append(data_)
                            if self.ps.poll() is not None:
                                break
                else:
                    print("File does not exist: " + vosk_server_filepath)
                self.started = True
            time.sleep(1)
        self.vosk_log_file_f.close()
