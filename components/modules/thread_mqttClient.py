import socket
import threading
import paho.mqtt.client as mqtt
import websockets

from config import *

f = None
arr_ = []
blocking = False
client_ = None


async def run_test(uri, data):
    async with websockets.connect(uri) as websocket:
        wf = open("components/vosk-server/websocket/test16k.wav", "rb")
        while True:
            data = wf.read(8000)

            if len(data) == 0:
                break

            await websocket.send(data)
            print (await websocket.recv())

        await websocket.send('{"eof" : 1}')
        print (await websocket.recv())


class MQTTClient(threading.Thread):
    client_ = None

    class MQTTEvents:
        def on_message(self, client, userdata, message):
            msg = str(message.payload.decode("utf-8"))
            print(len(msg))
            #loop = asyncio.new_event_loop()
            #asyncio.set_event_loop(loop)
            #asyncio.get_event_loop().run_until_complete(run_test('ws://localhost:2700', msg))

            #print("message received: ", msg)
            #print("message topic: ", message.topic)

        def on_connect(self, client, userdata, flags, rc):
            print("Connected to MQTT Broker: " + BROKER_ADDRESS)
            client.subscribe(TOPIC)

    def __init__(self):
        super(MQTTClient, self).__init__()

    def run(self):
        self.client_ = mqtt.Client()
        self.client_.username_pw_set("Izzy3110", "qwert")
        self.client_.on_connect = self.MQTTEvents.on_connect
        self.client_.on_message = self.MQTTEvents.on_message
        try:
            self.client_.connect(BROKER_ADDRESS, PORT)
            self.client_.loop_forever()
        except socket.timeout as ste:
            print("error with mqtt: "+str(ste))
            self.join()
            pass
