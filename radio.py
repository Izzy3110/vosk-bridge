import threading
import uuid
import requests
import json
import sys
import hashlib
import os
from urllib.parse import urlparse
from settings import config


def task_id():
    return uuid.uuid5(uuid.NAMESPACE_DNS, config["uuid_NAMESPACE_DNS"])


def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


class RadioManager(threading.Thread):
    current_task_id = None
    current_task = None
    cache_filename = None
    req_session = None

    tmp_sum = None
    current_tasks = {}

    element_start_marker = "File"

    def __init__(self, url):
        self.url = url
        super(RadioManager, self).__init__()

    def get_playlist(self):
        self.current_task_id = str(task_id())
        self.current_task = {
            "url": self.url
        }

        self.cache_filename = urlparse(self.url).path.lstrip("/")
        self.current_task["_cache_filename"] = self.cache_filename
        self.req_session = requests.session()
        self.current_tasks[self.current_task_id] = self.current_task

        self.test_for_update()

    def get_playlist_items(self):
        with open("cached/"+self.current_task["_cache_filename"]) as playlist_fíle:
            items = {}
            i_l = 0
            lines_ = playlist_fíle.read().splitlines()
            for line in lines_:
                if "[playlist]" in line:
                    playlist_start = i_l
                if playlist_start is not None and line.startswith(RM.element_start_marker):
                    id_ = int(line.split("File")[1].split("=")[0])
                    url = line
                    title_ = lines_[i_l + 1]
                    len_ = lines_[i_l + 2]
                    items[str(id_)] = {
                        "url": url.split("File" + str(id_) + "=")[1],
                        "title": title_.split("Title" + str(id_) + "=")[1],
                        "len": int(len_.split("Length" + str(id_) + "=")[1])
                    }

                i_l += 1
            self.current_tasks[self.current_task_id]["playlist_items"] = items
            return self.current_tasks[self.current_task_id]["playlist_items"] if ("playlist_items" in self.current_tasks[self.current_task_id].keys()) else None

    def test_for_update(self):
        len_ = int(self.req_session.head(self.current_task["url"]).headers.__dict__["_store"]["content-length"][1])
        if os.path.isfile("cached/" + self.current_task["_cache_filename"]):
            if int(os.stat("cached/" + self.current_task["_cache_filename"]).st_size) == len_:
                with open("tmp.pls", "wb") as tmp_file:
                    tmp_file.write(self.req_session.get(self.current_task["url"]).content)
                    tmp_file.close()
                    self.tmp_sum = sha256sum("tmp.pls")
                    self.current_task["tmp_sum"] = self.tmp_sum

                    if self.tmp_sum == sha256sum("cached/" + self.current_task["_cache_filename"]):
                        print("no need for redownload")

                    else:
                        print("redownload")
                        with open("cached/" + self.current_task["_cache_filename"] + ".sha256", "w") as sum_file:
                            new_sum = sha256sum("cached/" + self.current_task["_cache_filename"])
                            self.tmp_sum = new_sum
                            self.current_task["tmp_sum"] = self.tmp_sum
                            sum_file.write(new_sum)
                            sum_file.close()
                    self.current_tasks[self.current_task_id] = self.current_task
        else:
            with open("cached/"+self.current_task["_cache_filename"], "wb") as tmp_file:
                tmp_file.write(self.req_session.get(self.current_task["url"]).content)
                tmp_file.close()
                self.tmp_sum = sha256sum("cached/"+self.current_task["_cache_filename"])
                self.current_task["tmp_sum"] = self.tmp_sum
                self.current_tasks[self.current_task_id] = self.current_task
                if not os.path.isfile("cached/"+self.current_task["_cache_filename"]+".sha256"):
                    with open("cached/" + self.current_task["_cache_filename"] + ".sha256", "w") as sum_file:
                        sum_file.write(self.tmp_sum)
                        sum_file.close()

    def run(self) -> None:
        while self.is_running is True:
            print("rm")

if __name__ == '__main__':
    RM = RadioManager("https://dnbradio.com/hi.pls")
    RM.get_playlist()
    playlist_items = RM.get_playlist_items()
    stream_url = None
    chunk_size = 1024
    for k in playlist_items.keys():
        if "192K" in playlist_items[k]["title"]:
            if "DE" in playlist_items[k]["title"]:
                stream_url = playlist_items[k]["url"]
    if stream_url is not None:
        req_stream = requests.session()

        resp = req_stream.get(stream_url, stream=True)
        if os.path.isfile("cached/stream.mp3"):
            mode_ = "ab"
        else:
            mode_ = "wb"
        tmp_chunks = []
        with open('cached/stream.mp3', mode_) as f:
            chunks_ = 0
            for chunk in resp.iter_content(chunk_size):
                if chunks_ >= (chunk_size * 1024):
                    f.close()
                    f = open('cached/stream.mp3', "ab")
                    chunks_ = 0
                f.write(chunk)
                tmp_chunks.append(chunk)
                chunks_ += chunk_size
            f.close()


        '''
        f = None
        with open('cached/stream.mp3', 'wb') as f:
            print("open")
            try:
                for block in resp.iter_content(1024):
                    print(1024)
            except KeyboardInterrupt:
                pass
        '''

    else:
        print(" iss none")