import socketio
from threading import Lock
from components.tasks.mytasks import background_task
from components.modules.thread_vosk import VoskServer
import base64
import websockets
# from components.modules.thread_mqttClient import MQTTClient
# mqtt_client_ = None
# # -------------- in def connect(): ---------------- #
# mqtt_client_ = MQTTClient()
# mqtt_client_.start()
# # ------------------------------------------------- #


thread = None
thread_lock = Lock()

sio = socketio.AsyncServer(async_mode='tornado')

vs_ = None

clients_recording_status = {}


@sio.event
async def get_my_sid(sid):
    await sio.emit('my_sid', sid, to=sid)


@sio.event
async def audioData(sid, message):
    #await send_data_vosk('ws://127.0.0.1:2700', message["data"])
    print(len(message["data"]))
    # print(sid)
    with open("localfile.wav", "wb") as target_file_f:
        target_file_f.write(message["data"])
        target_file_f.close()
        
    

@sio.event
async def my_voice(message):
    tmp_ = b''
    from datetime import datetime
    with open("../tmp_wav-" + datetime.now().strftime("%d.%m.%Y_%H_%M_%S") + ".wav", "wb") as wav_file:
        for item in message["data"]:
            tmp_ = tmp_ + item
            wav_file.write(item)
        wav_file.close()
    await sio.emit('my_response_voice', {'data': tmp_, "sid": message["sid"], "room_uuid": message["room_uuid"]},
                   broadcast=True)


@sio.event
async def my_event(sid, message):
    await sio.emit('my_response', {'data': message['data']}, room=sid)


@sio.event
async def my_broadcast_event(message):
    await sio.emit('my_response', {'data': message['data']}, broadcast=True)


@sio.event
async def join(sid, message):
    sio.enter_room(sid, message['room'])
    await sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
                   room=sid)


@sio.event
async def leave(sid, message):
    sio.leave_room(sid, message['room'])
    await sio.emit('my_response', {'data': 'Left room: ' + message['room']},
                   room=sid)


@sio.event
async def close_room(message):
    await sio.emit('my_response',
                   {'data': 'Room ' + message['room'] + ' is closing.'},
                   room=message['room'])
    await sio.close_room(message['room'])


@sio.event
async def my_room_event(message):
    await sio.emit('my_response', {'data': message['data']},
                   room=message['room'])


# noinspection PyUnresolvedReferences
@sio.event
async def init_ctrl(sid, message):
    global vs_
    if vs_ is not None:
        if message["data"] == "get_last_vosk_logs":
            vosk_lines = vs_.get_lines()
            if vosk_lines is not None:
                await sio.emit("last_vosk_lines", {"data": vosk_lines}, to=sid)


@sio.event
async def disconnect_request(sid):
    await sio.disconnect(sid)


@sio.event
async def connect(sid, _):
    global vs_
    if vs_ is None:

        vs_ = VoskServer(sio)
        vs_.start()
    global thread
    with thread_lock:
        if thread is None:
            thread = sio.start_background_task(background_task)
    await sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected: ' + str(sid))
