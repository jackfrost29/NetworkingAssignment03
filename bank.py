import socketserver
import sqlite3
import sys
import threading

# accept one command line inputs: BANK_PORT

def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our bank server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication with the
    client.
    """

    

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        s = str(self.data)
        s = s.replace("\"", "")
        s = s.replace("bb'", "")
        s = s.replace("\'", "")
        


        s = s.replace("id=", "")
        s = s.replace("quantity=", "")
        s = s.replace("first_name=", "")
        s = s.replace("last_name=", "")
        s = s.replace("post_code=", "")
        s = s.replace("card_no=", "")

        x = s.split("&")

        con = sqlite3.connect("database.db")
        con.row_factory = dict_factory
        cur = con.cursor()

        command = "select * from buyer where first_name=\"" + x[2] + "\" and last_name=\"" + x[3]+"\";"
        cur.execute(command)
        dic1 = cur.fetchone()
        print(dic1)

        command = "select * from store where id=\"" + x[0] + "\";"
        cur.execute(command)
        dic2 = cur.fetchone()
        print(dic2)

        if dic1 != None and dic2 != None:

            post_code = str(dic1["post_code"])
            credit_no = str(dic1["credit_no"])
            balance = int(dic1["balance"])
            if post_code == x[4] and credit_no == x[5]:
                # all information valid
                price = int(dic2["price"])
                quantity = int(x[1])
                
                if balance >= (price * quantity):
                    print("balance: " + str(balance))
                    print("cost: " + str(price*quantity))
                    
                    # transaction can be approved
                    balance -= price*quantity
                    command = "update buyer set balance="+str(balance)+" where credit_no=\""+credit_no+"\";"
                    cur.execute(command)
                    self.request.sendall(bytes("1&"+str(balance)+"&"+str(price*quantity), "utf-8"))
                else:
                    # insufficient balance
                    self.request.sendall(bytes("0", "utf-8"))
        
        else:
            # invalid information
            self.request.sendall(bytes("-1", "utf-8"))

        con.commit()
        con.close()
        
        # shutdown the server
        assassin = threading.Thread(target=server.shutdown)
        assassin.daemon = True
        assassin.start()


HOST, PORT = "localhost", int(sys.argv[1])
server = socketserver.TCPServer((HOST, PORT), MyTCPHandler, bind_and_activate=False)
server.allow_reuse_address = True
server.daemon_threads = True
server.server_bind()
server.server_activate()


if __name__ == "__main__":
    print("Bank server running on localhost port: " + sys.argv[1])

    try:
        while True:
            server.serve_forever()
            print("Bank server restart on localhost at port: " + sys.argv[1])

            server = socketserver.TCPServer((HOST, PORT), MyTCPHandler, bind_and_activate=False)
            server.allow_reuse_address = True
            server.daemon_threads = True
            server.server_bind()
            server.server_activate()


    except KeyboardInterrupt:
        pass
