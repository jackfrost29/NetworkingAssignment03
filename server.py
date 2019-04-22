import http.server
import socketserver

PORT = 8080
handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print('Serving at port ', PORT)
    httpd.serve_forever()