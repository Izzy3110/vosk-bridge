import asyncio
import os
import sys
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
from components.handler import VideoHandler, MainHandler
from components.sio.sio_stuff import *

define("port", default=5000, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")

if sys.platform == "win32":
    # https://github.com/tornadoweb/tornado/issues/2608
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    asyncio.set_event_loop_policy(
        tornado.platform.asyncio.AnyThreadEventLoopPolicy()
    )


def make_app():
    parse_command_line()
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/video/?", VideoHandler),
            (r"/video/(.*?)/?", VideoHandler),
            (r"/socket.io/", socketio.get_tornado_handler(sio)),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=options.debug,
        cookie_secret=base64.b64encode("testest".encode()).decode().lstrip("==")

    )


def main():
    app = make_app()
    app.__setattr__("rooms", {})
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    sio.start_background_task(background_task)


if __name__ == "__main__":
    main()
