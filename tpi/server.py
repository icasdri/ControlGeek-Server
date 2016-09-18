#!/usr/bin/python2

import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import gpio

gpio_servo = None
gpio_led = None

targets = None


def load_json_config():
    result = {}
    with open('static/config.json') as config_file:
        config = json.load(config_file)
        for t in config:
            tp = getattr(gpio, t['cls'])(t['pin'])
            tp.name = t['name']
            result[t['prefix']] = tp
    return result


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('static/index.html')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('WebSocket opened')

    def on_message(self, message):
        if len(message) >= 2:
            p = message[0]
            if p in targets:
                tp = targets[p]
                print(tp.name + ': ' + message[1:])
                if message[1] == '+':
                    tp.inc_val(int(message[2:]))
                elif message[1] == '-':
                    tp.dec_val(int(message[2:]))
                else:
                    tp.set_val(int(message[1:]))
            else:
                print('UNRECOGNIZED: ' + message)

    def on_close(self):
        print('WebSocket closed')


def make_app():
    settings = {
        'static_path': 'static',
        'static_url_prefix': '/static/',
    }

    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/sock', WebSocketHandler),
    ], **settings)


if __name__ == "__main__":
    gpio.init()
    targets = load_json_config()

    app = make_app()
    app.listen(9877)

    tornado.ioloop.IOLoop.current().start()
