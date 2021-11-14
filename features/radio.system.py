import subprocess
import threading
import time


class Radio(threading.Thread):
    started = False
    running = True

    def __init__(self):
        super(Radio, self).__init__()

    def run(self) -> None:
        while self.running is True:
            if self.started is False:
                with subprocess.Popen("python radio.py", shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE) as ps:
                    out, err = ps.communicate()
                    print(err)
                self.started = True
            time.sleep(1)
