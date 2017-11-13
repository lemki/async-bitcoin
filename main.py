import tornadoredis
import tornado.ioloop
import tornado.web
import tornado.gen
from tornado.escape import json_decode
from tornado import httpclient

c = tornadoredis.Client()
c.connect()

class MainHandler(tornado.web.RequestHandler):
     async def get(self):
         http_client = httpclient.AsyncHTTPClient()
         rate = await tornado.gen.Task(c.get, 'rate')
         if rate:
             self.render("template.html", rate=rate)
         else:
             r = await http_client.fetch("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
             decoded = json_decode(r.body)
             await tornado.gen.Task(c.set, 'rate', decoded['bpi']['USD']['rate'], 60)
             self.render("index.html", rate=decoded['bpi']['USD']['rate'])


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
      app = make_app()
      app.listen(8887)
      tornado.ioloop.IOLoop.current().start()
