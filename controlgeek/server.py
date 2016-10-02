#!/usr/bin/python2
#
# Copyright 2016 icasdri
#
# This file is part of ControlGeek Server. The original source code for
# ControlGeek Server can be found at <https://github.com/icasdri/ControlGeek-
# Server>. See COPYING for licensing details.
#

import threading
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


socket_counter_lock = threading.Lock()
open_sockets = {}
socket_counter = 0


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        global socket_counter
        with socket_counter_lock:
            self.socket_counter_id = socket_counter
            open_sockets[socket_counter] = self
            socket_counter += 1

        for k, v in targets.items():
            self.write_message(k + str(v.val))

        print('WebSocket opened')

    def _send_gpio_val(self, tp, message):
        if message[1] == '+':
            return tp.inc_val(int(message[2:]))
        elif message[1] == '-':
            return tp.dec_val(int(message[2:]))
        else:
            return tp.set_val(int(message[1:]))

    def on_message(self, message):
        if len(message) >= 2:
            p = message[0]
            if p in targets:
                tp = targets[p]
                print(tp.name + ': ' + message[1:])
                val = self._send_gpio_val(tp, message)
                for s in filter(lambda i: i != self.socket_counter_id,
                                open_sockets):
                    open_sockets[s].write_message(p + str(val))
            else:
                print('UNRECOGNIZED: ' + message)

    def on_close(self):
        with socket_counter_lock:
            del open_sockets[self.socket_counter_id]

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
