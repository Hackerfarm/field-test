#!/usr/bin/env python
# -*- coding: utf-8

from datetime import datetime
from pymongo.connection import Connection

from bson.objectid import ObjectId
import json
 
import os.path
import tornado.httpserver
import tornado.options
import tornado.web
import tornado.ioloop
import time
import io

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
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
		

class GraphHandler(tornado.web.RequestHandler):
	def get(self):
		db = self.application.database
		epoc=datetime(2016,1,9)
		t = list()
		vbat = list()
		vsol = list()
		temp = list()
		for r in db.records.find():
			if r.has_key("content"):
				c=json.loads(r["content"])
				t.append((r["timestamp"]-epoc).total_seconds()/3600.0)
				vbat.append(c["vbat"])
				vsol.append(c["vsol"])
				temp.append(c["temperature"])
		fig = plt.figure()
		ax1 = fig.add_subplot(111)
		l1 = ax1.plot(t, vsol, '-', linewidth=1, label="Vsol (mV)")
		l2 = ax1.plot(t, vbat, '-', linewidth=1, label="Vbat (mV)")
		ax2 = plt.twinx()
		l3 = ax2.plot(t, temp, '-', linewidth=1, label=u"Temperature (°C)", color="r")
		ax1.legend(loc=0)
		ax2.legend()

		buf = io.BytesIO()
		plt.savefig(buf, format='png')
		self.set_header("Content-Type", "image/png")
		self.write(buf.getvalue())
		buf.close()
		
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
            (r"/post", PostHandler),
            (r"/graph", GraphHandler)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

        self.con = Connection('localhost', 27017)
        self.database = self.con["field-test"]


def main():
	tornado.options.parse_command_line()
	app = Application()
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
