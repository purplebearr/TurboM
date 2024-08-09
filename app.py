import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from urls import url_patterns, get_controller

class MVCHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        for pattern, controller_name, _ in url_patterns:
            if pattern == parsed_path.path:
                controller_func = get_controller(controller_name)
                response = controller_func(query_params)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(response.encode())
                return

        # If no pattern matches, serve static files
        if self.path.startswith('/static/'):
            super().do_GET()
        else:
            self.send_error(404)

def run(port=8000):
    with socketserver.TCPServer(("", port), MVCHandler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
