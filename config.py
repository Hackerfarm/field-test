#!/usr/bin/env python
# -*- coding: utf-8

from tornado.options import define, options

define("port", default=4489, type=int)


define("home_url", help="The URL the website will be at", 
                   default="http://localhost:4489")  
 
define("cookie_secret", help="Some entropy for the cookie_secret", 
                   default="Not in use now, but let's change it when we have authentication")
 
