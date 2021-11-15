from abc import ABC
import tornado


class MainHandler(tornado.web.RequestHandler, ABC):
    def get(self):
        self.render("app.html")
