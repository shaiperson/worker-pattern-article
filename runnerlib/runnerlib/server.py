import json
import traceback
from http import server
import logging

from .discovery import get_handler
from .settings import PORT

logger = logging.getLogger(f'Server')


class AnalysisRequestHandler(server.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get algorithm handler
            logger.info(f'Received request with path {self.path}')
            algorithm = self.get_path_algorithm()
            logger.debug(f'Detected algorithm {algorithm}')

            handler = get_handler(algorithm)

        except:
            traceback.print_exc()
            logger.info(f'Error trying to parse path')
            self.send_response(500, message=f'Internal error')
            self.end_headers()
            return

        if not handler:
            logger.info(f'No handler found for algorithm {algorithm}, responding 404')
            self.send_response(404, message=f'Path {self.path} not supported')
            self.end_headers()
            return

        # Parse request body
        try:
            logger.debug('Parsing body')
            body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            logger.debug(f'Parsed body {body}')
        except:
            message = f'Unable to parse JSON body'
            logger.info(message)
            traceback.print_exc()
            self.send_response(400, message=message)
            self.end_headers()
            return

        if not handler.validate_body(body):
            message = f'Invalid body. Expected fields: {handler.get_expected_args()}'
            logger.info(message)
            self.send_response(400, message=message)
            self.end_headers()
            return

        logger.debug(f'Parsed body successfully, calling handler {handler}')

        # Run handler passing body
        try:
            result = handler.call(**body)
        except:
            message = f'Internal error'
            logger.info(message)
            traceback.print_exc()
            self.send_response(500, message=message)
            self.end_headers()
            return

        # Respond with result
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(dict(result=result)), 'utf-8'))

    def get_path_algorithm(self):
        return self.path.split('/')[1]


def run_server():
    logger.info('Building server instance')
    server_address = ('', PORT)
    httpd = server.HTTPServer(server_address, AnalysisRequestHandler)

    logger.info(f'Starting server on port {PORT}')
    httpd.serve_forever()
