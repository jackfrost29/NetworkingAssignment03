from requestHandler import RequestHandler

class BadRequestHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.content_type = 'text/html'
        self.setStatus(404)