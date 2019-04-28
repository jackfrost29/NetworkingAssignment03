from http.server import BaseHTTPRequestHandler
from routes.main import routes
from pathlib import Path
import os
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler

class Server(BaseHTTPRequestHandler):

    '''
    In order to respond, our class will need to be able to send, at minimum, three things:

    - the response’s Content-type,
    - the response’s status code,
    - and finally the actual content of the site

    '''

    def do_HEAD(self):
        return


    def do_POST(self):
        return


    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]
        if request_extension is "" or request_extension is ".html":
            if self.path in routes:
                handler = TemplateHandler()
                handler.find(routes[self.path])
            else:
                handler = BadRequestHandler()

            self.respond({
                'handler':handler
            })


    def handle_http(self, handler):
        status_code = handler.get_status()

        self.send_response(status_code)
        if status_code is 200:
            content = handler.get_content
            self.send_header('Content-type', handler.getContentType())
        else:
            content = '404 Not Found'

        self.end_headers()

        return bytes(content, "UTF-8")


    def respond(self, opts):
        '''
        in charge of sending the actual response out
        '''
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)
