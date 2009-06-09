from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print "Getting %s" % os.path.join(os.curdir, self.path.lstrip('/'))
        if not os.path.exists(os.path.join(os.curdir, self.path.lstrip('/'))):
            self.send_error(404, 'File not Found')
            return        
        self.send_response(200)
        if not (self.path.startswith("/static") or self.path.endswith('.css')):
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
        f = file(os.path.join(os.curdir, self.path.lstrip('/')))
        self.wfile.write(f.read())
        return

if __name__ == '__main__':
    server = HTTPServer(('', 8090), HTTPHandler)
    server.serve_forever()


            
