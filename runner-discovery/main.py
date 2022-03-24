from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import logging
import traceback

PORT = int(os.environ.get('PORT', 5099))
LOG_LEVEL = os.environ.get('LOG_LEVEL', '')

log_level = getattr(logging, LOG_LEVEL, 'DEBUG')
logging.basicConfig(level=log_level, format='%(levelname)s :: %(message)s')
logger = logging.getLogger('Server')

registry = {}


class ClassifierServer(BaseHTTPRequestHandler):
    def _set_response(self, code, content_type):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_POST(self):
        # Process request
        response_body = {}
        try:
            content_length = int(self.headers['Content-Length'])
            body_raw = self.rfile.read(content_length)
            body = json.loads(body_raw)
            algorithm = body['algorithm']
            host = body['host']

        except ValueError as e:
            logger.error('ValueError while parsing body as JSON')
            response_body = {'message': f'Body not valid JSON: "{e}"'}
            self._set_response(400, 'application/json')

        except KeyError as e:
            response_body = {'message': f'Body missing field {e}'}
            self._set_response(400, 'application/json')

        else:
            try:
                logger.info(f'Registering algorithm {algorithm} as hosted on {host}')
                registry[algorithm] = host
                self._set_response(200, 'application/json')

            except Exception as e:
                error_str = traceback.format_exc()
                response_body = {'message': '[x] Internal error', 'error': error_str}
                self._set_response(500, 'application/json')

        self.wfile.write(json.dumps(response_body).encode('utf-8'))

    def do_GET(self):
        self._set_response(200, 'application/json')
        self.wfile.write(json.dumps(registry).encode('utf-8'))


if __name__ == '__main__':
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, ClassifierServer)
    try:
        logger.info('[+] Listening on port {}'.format(PORT))
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
