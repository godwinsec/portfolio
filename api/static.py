from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get the path from the request
        path = self.path.lstrip('/')
        
        # Check if the file exists
        if os.path.exists(path):
            # Get the file extension
            _, ext = os.path.splitext(path)
            
            # Set the content type based on the file extension
            content_types = {
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.svg': 'image/svg+xml',
                '.pdf': 'application/pdf'
            }
            
            content_type = content_types.get(ext, 'application/octet-stream')
            
            # Send the response
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            
            # Read and send the file
            with open(path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            # File not found
            self.send_response(404)
            self.end_headers() 