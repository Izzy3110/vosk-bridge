import queue
import threading
import time

from tornado import concurrent

from components.sio.sio_stuff import sio


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

