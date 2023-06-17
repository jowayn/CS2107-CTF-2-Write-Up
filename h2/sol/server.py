from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

print(os.listdir())

os.chdir('html')

port = 8000
httpd = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
print(f"Serving on port {port}")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down server...")
    httpd.shutdown()

