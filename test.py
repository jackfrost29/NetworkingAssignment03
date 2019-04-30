from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import jinja2
import sys

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if self.path == '/images/flamingo.jpg':
            self.path = 'images/flamingo.jpg'
            content = open(self.path, 'rb')
            self.wfile.write(content.read())
            return


        content = open('index.html', 'rb')
        self.wfile.write(content.read())
        
        return
        
        current_path = os.path.dirname(os.path.abspath(__file__))
        template_file_path = os.path.join(current_path, 'sample.html.j2')
        rendered_file_path = os.path.join(current_path, 'index.html')

        environment = jinja2.Environment(loader=jinja2.FileSystemLoader(current_path))
        output = environment.get_template('sample.html.j2').render(name='Abid Vai')

        #print(output)

        # save the rendered template to index.html
        with open(rendered_file_path, 'w') as result_file:
            result_file.write(output)

        with open(rendered_file_path, 'rb') as file:
            self.wfile.write(file.read())

httpd = HTTPServer(('localhost', 8000), MyHandler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass