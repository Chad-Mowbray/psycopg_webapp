import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json

import sys
sys.path.append('../')
from database.query import get_posts_by_author

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        search = None
        query_components = parse_qs(urlparse(self.path).query)
        if 'search' in query_components:
            self.send_header("Content-type", "application/json")
            self.end_headers()
            search = get_posts_by_author(query_components["search"][0])
            response = {
                "content": search
            }
            self.wfile.write(bytes(json.dumps(response), "utf8"))

 
        else:
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open('index.html') as index_page:
                response = index_page.read()
            self.wfile.write(bytes(response, "utf8"))

handler_object = MyHttpRequestHandler

PORT = 8001
my_server = socketserver.TCPServer(("", PORT), handler_object)

my_server.serve_forever()