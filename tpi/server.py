#!/usr/bin/python2

import tornado.ioloop
import tornado.web
import tornado.websocket
import gpio


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        if len(message) >= 2:
            if message[0] == 's':
                val = message[1:]
                print("Servo: " + val)
            elif message[0] == 'l':
                val = message[1:]
                print("LED: " + val)
            else:
                print("UNRECOGNIZED MESSAGE: " + message)

    def on_close(self):
        print("WebSocket closed")


def make_app():
    settings = {
        "static_path": "static",
        "static_url_prefix": "/static/",
    }

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/sock", WebSocketHandler),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(9877)
    gpio.init()
    tornado.ioloop.IOLoop.current().start()
