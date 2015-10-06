#!/usr/bin/env python
# -*- coding: utf-8

from datetime import datetime
from pymongo.connection import Connection

from bson.objectid import ObjectId
 
import os.path
import tornado.httpserver
import tornado.options
import tornado.web
import tornado.ioloop
import time

from tornado.options import define, options

import config


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("""Hi!<hr>""")
		db = self.application.database
		records = db.records.find()
		for r in records:
			self.write("""At <i>{0}</i> the node <b>{1}</b> sent the content: <br><i>{2}</i><br><br>\n"""
				.format(r["timestamp"], r["sender"], r["content"]))
		
class PostHandler(tornado.web.RequestHandler):
	def post(self):
		timestamp = datetime.now()
		self.write("""You posted:<br>
			{0}<br>
			You identify as: {1}<br>
			Timestamp will be: {2}
			""".format(
				self.request.arguments.get("content", [""])[0],
				self.request.arguments.get("identity", [""])[0],
				timestamp
				))
		db = self.application.database
		db.records.insert({
			"sender":self.request.arguments.get("identity",[""])[0],
			"timestamp":timestamp,
			"content":self.request.arguments.get("content",[""])[0]})
		

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            autoescape=None,
            cookie_secret=options.cookie_secret,
            home_url=options.home_url,
            debug=True,
        )

        handlers = [
            (r"/", MainHandler),
            (r"/post", PostHandler)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

        self.con = Connection('localhost', 27017)
        self.database = self.con["field-test"]


def main():
	tornado.options.parse_command_line()
	app = Application()
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()
if __name__ == "__main__":
    main()
