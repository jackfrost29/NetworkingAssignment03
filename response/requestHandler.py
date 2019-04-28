class MockFile():
    def read(self):
        return False

class RequestHandler():
    def __init__(self):
        self.content_type = ""
        self.contents = MockFile()

    def getContents(self):
        return self.contents.read()

    def read(self):
        return self.read()

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def getContentType(self):
        return self.content_type

    def getType(self):
        return 'static'