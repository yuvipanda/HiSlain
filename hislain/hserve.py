from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import sys

serve_from = os.curdir

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not os.path.exists(os.path.join(serve_from, self.path.lstrip('/'))):
            self.send_error(404, 'File not Found')
            return        
        self.send_response(200)
        if not self.path.startswith("/static"):
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
        f = file(os.path.join(serve_from, self.path.lstrip('/')), 'rb+')
        s = f.read()
        print s
        self.wfile.write(s)
        return

if __name__ == '__main__':
    serve_from = sys.argv[1]
    serve_port = int(sys.argv[2])
    server = HTTPServer(('', serve_port), HTTPHandler)
    server.serve_forever()


            
