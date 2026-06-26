# Create a simple api endpoint for the three math operations
# add
# subtract
# multiply

# def add(a,b):
#     return a+b

# GET http://localhost:5000/add?a=5&b=3

# result: {'a':4, 'b':3, 'operation':'addition', 'result': 8}

# You are going to use the builtin HTTP Server library
# Read how to use it, but don't vibe code the whole thing

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json


class MathHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Split the path from the query string
        parsed = urlparse(self.path)
        operation = parsed.path.strip("/")          # e.g. "add"
        params = parse_qs(parsed.query)             # e.g. {'a': ['5'], 'b': ['3']}

        # parse_qs returns lists, so grab the first value and convert to number
        def to_number(value):
            num = float(value)
            return int(num) if num.is_integer() else num

        try:
            a = to_number(params["a"][0])
            b = to_number(params["b"][0])
        except (KeyError, ValueError):
            self.send_error(400, "Missing or invalid 'a'/'b' parameters")
            return

        # Map the URL path to an operation
        operations = {
            "add":      ("addition",       a + b),
            "subtract": ("subtraction",    a - b),
            "multiply": ("multiplication", a * b),
        }

        if operation not in operations:
            self.send_error(404, f"Unknown operation: {operation}")
            return

        op_name, result = operations[operation]

        # Build the response dict
        response = {
            "a": a,
            "b": b,
            "operation": op_name,
            "result": result,
        }

        # Send a proper JSON response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))


def run(port=5000):
    server = HTTPServer(("localhost", port), MathHandler)
    print(f"Server running on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()