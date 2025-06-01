from http.server import BaseHTTPRequestHandler
from godwin.wsgi import application
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Get the response from Django
        response = application(self.environ, self.start_response)
        
        # Send the response
        for chunk in response:
            self.wfile.write(chunk)