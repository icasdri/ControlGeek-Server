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
        print("Received: " + message)

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
