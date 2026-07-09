import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8080))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="frontend", **kwargs)
    
    def do_GET(self):
        # Serve index.html for root
        if self.path == "/":
            self.path = "/index.html"
        # Serve admin.html for /admin
        elif self.path == "/admin":
            self.path = "/admin.html"
        return super().do_GET()
    
    def log_message(self, format, *args):
        pass

print(f"Senex frontend serving on port {PORT}")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
