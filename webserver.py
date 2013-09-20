#!/usr/bin/env python

import web

urls = ("/req", "RequestHandler")
app = web.application(urls, globals())


class RequestHandler():
    def POST(self):
        data = web.data() # you can get data use this method
        print data
        return data
    def GET(self):
                
        return str(data)


if __name__ == "__main__":
    app.run()
