import uuid
from abc import ABC
import tornado


class VideoHandler(tornado.web.RequestHandler, ABC):
    def get(self, room_uuid=None):
        room_id_set = False
        if room_uuid is not None:
            print("room-uuid: "+room_uuid)
            room_id_set = True
        else:
            room_uuid = str(uuid.uuid4())

        room_uuid_cookies = self.get_cookie("room_id_cookie")
        if room_uuid_cookies is not None:
            print("from cookie")
            if room_uuid_cookies != room_uuid:
                room_uuid = room_uuid_cookies
        else:
            self.set_cookie("room_id_cookie", room_uuid)

        print(self.application.rooms)
        # print(dir(self.app))
        if room_uuid not in self.application.rooms.keys():
            self.application.rooms[room_uuid] = {
                "clients": 1,
                "clients_": {}
           }
        else:
            self.application.rooms[room_uuid]["clients"] = self.application.rooms[room_uuid]["clients"]+1

        if room_id_set:
            self.render("video.html")
        else:
            return self.redirect("/video/" + str(room_uuid))
