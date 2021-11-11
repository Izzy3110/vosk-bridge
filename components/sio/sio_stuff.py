import base64
from threading import Lock

from config import QOS
from components.modules import mqtt_client
from components.mytasks import background_task

import socketio
from components.modules import VoskServer
thread = None
thread_lock = Lock()

sio = socketio.AsyncServer(async_mode='tornado')


@sio.event
async def get_my_sid(sid):
    await sio.emit('my_sid', sid, to=sid)

mqtt_client_ = mqtt_client()
mqtt_client_.start()

@sio.event
async def my_voice(sid, message):
    global mqtt_client_
    print(message.keys())
    TOPIC = message["room_uuid"]
    mqtt_client_.client_.subscribe(TOPIC)
    mqtt_client_.client_.publish(TOPIC, base64.b64encode(message["data"]).decode(), qos=QOS)
    await sio.emit('my_response_voice', {'data': base64.b64encode(message["data"]).decode(), "sid": message["sid"], "room_uuid": TOPIC},broadcast=True)


@sio.event
async def my_event(sid, message):
    await sio.emit('my_response', {'data': message['data']}, room=sid)


@sio.event
async def my_broadcast_event(sid, message):
    await sio.emit('my_response', {'data': message['data']},broadcast=True)


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
async def close_room(sid, message):
    await sio.emit('my_response',
                   {'data': 'Room ' + message['room'] + ' is closing.'},
                   room=message['room'])
    await sio.close_room(message['room'])


@sio.event
async def my_room_event(sid, message):
    await sio.emit('my_response', {'data': message['data']},
                   room=message['room'])

@sio.event
async def init_ctrl(sid, message):
    if message["data"] == "get_last_vosk_logs":
        await sio.emit("last_vosk_lines",{"data": vs_.vosk_lines}, to=sid)

@sio.event
async def disconnect_request(sid):
    await sio.disconnect(sid)

vs_ = None
clients_recording_status = {}

@sio.event
async def connect(sid, environ, _):
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
    print('Client disconnected')

