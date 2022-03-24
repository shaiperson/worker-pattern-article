import json
import traceback
from http import server
import logging

from .discovery import get_handler
from .settings import PORT

logger = logging.getLogger(f'Server')


class AnalysisRequestHandler(server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Get algorithm handler
        algorithm = self.get_path_algorithm()
        handler = get_handler(algorithm)

        if not handler:
            self.send_response(404, message=f'Path {self.path} not supported')
            self.end_headers()
            return

        # Parse request body
        try:
            body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        except:
            traceback.print_exc()
            self.send_response(400, message=f'Unable to parse JSON body')
            self.end_headers()
            return

        if not handler.validate_body(body):
            self.send_response(400, message=f'Invalid body. Expected fields: {handler.get_expected_args()}')
            self.end_headers()
            return

        # Run handler passing body
        result = handler.call(**body)

        # Respond with result
        self.wfile.write(bytes(json.dumps(dict(result=result)), 'utf-8'))
        self.send_header('Content-Type', 'application/json')
        self.send_response(200)
        self.end_headers()

    def get_path_algorithm(self):
        return self.path[1:].split('/')[2]


def run_server():
    logger.info('Building server instance')
    server_address = ('', PORT)
    httpd = server.HTTPServer(server_address, AnalysisRequestHandler)

    logger.info('Starting server on port', PORT)
    httpd.serve_forever()
