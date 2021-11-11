import asyncio
import base64
import os
import subprocess
import sys
import threading
import time
from datetime import datetime
import paho.mqtt.client as mqtt
import tornado
import websocket
import websockets

from config import *

f = None
arr_ = []
blocking = False


async def run_test(uri, data):
    async with websockets.connect(uri) as websocket:
        global f,arr_, blocking
        wf = open("components/vosk-server/websocket/test16k.wav", "rb")
        while True:
            data = wf.read(8000)

            if len(data) == 0:
                break

            await websocket.send(data)
            print (await websocket.recv())

        await websocket.send('{"eof" : 1}')
        print (await websocket.recv())
        blocking = False




class mqtt_client(threading.Thread):
    class MQTTEvents:
        def on_message(client, userdata, message):
            msg = str(message.payload.decode("utf-8"))
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            asyncio.get_event_loop().run_until_complete(run_test('ws://localhost:2700', msg))

            #print("message received: ", msg)
            #print("message topic: ", message.topic)

        def on_connect(client, userdata, flags, rc):
            print("Connected to MQTT Broker: " + BROKER_ADDRESS)
            client.subscribe(TOPIC)

    client_ = None

    def __init__(self):
        super(mqtt_client, self).__init__()

    def run(self):
        global client_
        self.client_ = mqtt.Client()
        self.client_.username_pw_set("Izzy3110", "qwert")
        self.client_.on_connect = self.MQTTEvents.on_connect
        self.client_.on_message = self.MQTTEvents.on_message
        self.client_.connect(BROKER_ADDRESS, PORT)
        self.client_.loop_forever()


class VoskServer(threading.Thread):
    started = False
    running = True
    vosk_log_file_f = None
    vosk_lines = None
    vosk_start_t = None
    socketio = None
    ps = None

    def log_to_file(self, line):
        # print("ltf: "+line)
        if self.vosk_log_file_f is None:
            self.vosk_log_file_f = open("logs/vosk.log", "a")
        self.vosk_log_file_f.write(line + "\n")

        self.vosk_lines.append(line)
        self.vosk_log_file_f.close()
        self.vosk_log_file_f = None

    def __init__(self, socketio_):
        self.socketio = socketio_

        self.vosk_log_file_f = open("logs/vosk.log", "a")
        self.vosk_start_t = time.time()
        self.vosk_lines = []
        super(VoskServer, self).__init__()

    def run(self) -> None:
        print("VS")
        while self.running is True:
            if self.started is False:
                with subprocess.Popen("python components/asr_server.py", shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE) as self.ps:
                    while True:
                        error = self.ps.stderr.readline()
                        output = error
                        msg_ = output.decode().rstrip("\r\n")
                        date_ = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
                        data_ = date_ + ": " + msg_
                        self.log_to_file(data_)
                        if self.ps.poll() is not None:
                            break

                    rc = self.ps.poll()
                self.started = True
            time.sleep(1)
        self.vosk_log_file_f.close()


class Radio(threading.Thread):
    started = False
    running = True

    def __init__(self):
        super(Radio, self).__init__()

    def run(self) -> None:
        # print("Radio_")
        while self.running is True:
            if self.started is False:
                with subprocess.Popen("python radio.py", shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE) as ps:
                    out, err = ps.communicate()
                    print(err)
                self.started = True
            time.sleep(1)


'''
import queue
def worker():
    global q_done
    while True:
        item = q.get()
        time.sleep(.125)
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()
        if q.empty():
            q_done = True


q = queue.Queue()
q_done = False
threading.Thread(target=worker, daemon=True).start()
'''
'''
for item in range(0, 10):
    q.put(item)
print('All task requests sent\n', end='')
while q_done is False:
    time.sleep(.001)
print("done")

executor = concurrent.futures.ThreadPoolExecutor(16)


@sio.event
async def my_q_add(sid, message):
    print(message["data"])
    q.put(message["data"])
    await sio.emit('my_response', {'data': message['data']}, room=sid)

'''
