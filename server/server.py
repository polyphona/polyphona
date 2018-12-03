# server.py

import falcon


class Listener(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = ('Hello world !\n\n')


app = falcon.API()

listener = Listener()

app.add_route('/qsd', listener)


"""
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
"""