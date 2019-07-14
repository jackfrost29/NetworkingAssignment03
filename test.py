from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import os
import jinja2
import sys
import cgi
import sqlite3


# accept three command line inputs: STORE_PORT, BANK_HOST_IP, BANK_PORT

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class MyHandler(BaseHTTPRequestHandler):

    def verify(self, data):
        
        p = sys.argv[2]
        HOST, PORT = sys.argv[1], int(p)


        # Create a socket (SOCK_STREAM means a TCP socket)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(bytes(data, "utf-8"))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-8")
            return received

    def scanDB(self):
        con = sqlite3.connect("database.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("select * from store;")

        return cur.fetchall()

    def do_POST(self):
        form = cgi.FieldStorage()
        print(form)
        req = str(form.getvalue("id")) + ":" + str(form.getvalue("quantity")) + ":" + str(form.getvalue("first_name")) \
            + ":" + str(form.getvalue("last_name")) + ":" + str(form.getvalue("post_code")) + ":" + str(form.getvalue("card_no"))
        
        response = self.verify(req)

        res = None

        if response == "0":
            # insufficient balance
            print("insufficient balance")
            res = "Sorry, insufficient balance"
        elif response == "-1":
            # invalid info
            print("invalid info")
            res = "Sorry, invalid information"
        else:
            # successfull
            print("successful")
            res = "Sorry, insufficient balance"

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        current_path = os.path.dirname(os.path.abspath(__file__))
        template_file_path = os.path.join(current_path, 'response_template.html.j2')
        rendered_file_path = os.path.join(current_path, 'response.html')

        dic = self.scanDB()

        environment = jinja2.Environment(loader=jinja2.FileSystemLoader(current_path))
        output = environment.get_template('response_template.html.j2').render(response=res)

        # save the rendered template to index.html
        with open(rendered_file_path, 'w') as result_file:
            result_file.write(output)

        with open(rendered_file_path, 'rb') as file:
            self.wfile.write(file.read())



    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if 'images' in self.path or 'success' in self.path:
            current_path = os.path.dirname(os.path.abspath(__file__))
            output_file_path = current_path + '/' + self.path

            '''
            print(current_path)
            print("printed path in first condition " + self.path)
            print("rendered file path " + output_file_path)
            '''

            with open(output_file_path, 'rb') as file:
                self.wfile.write(file.read())

            return

        # other wise the index file is to be sent

        current_path = os.path.dirname(os.path.abspath(__file__))
        template_file_path = os.path.join(current_path, 'sample.html.j2')
        rendered_file_path = os.path.join(current_path, 'index.html')

        dic = self.scanDB()

        environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(current_path))
        output = environment.get_template('sample.html.j2').render(dic=dic)

        # save the rendered template to index.html
        with open(rendered_file_path, 'w') as result_file:
            result_file.write(output)

        with open(rendered_file_path, 'rb') as file:
            self.wfile.write(file.read())

        '''
        print(current_path)
        print("printed path in second condition " + self.path)
        print("rendered file path " + rendered_file_path)
        '''

httpd = HTTPServer(('localhost', 8000), MyHandler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
