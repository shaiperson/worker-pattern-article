from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import logging

import exceptions

PORT = int(os.environ.get('PORT', 5000))
LOG_LEVEL = os.environ.get('LOG_LEVEL', '')

log_level = getattr(logging, LOG_LEVEL, 'DEBUG')
logging.basicConfig(level=log_level, format='%(asctime)s :: %(levelname)s :: %(message)s')
logger = logging.getLogger('Server')

import classifier


class ClassifierServer(BaseHTTPRequestHandler):
    def _set_response(self, code, content_type):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_POST(self):
        # Process request
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_json = json.loads(post_data)
            image_url = post_json['url']

        except ValueError as e:
            logger.error('ValueError while parsing body as JSON')
            response_body = {'message': f'Task body not valid JSON: "{e}"'}
            self._set_response(400, 'application/json')

        except KeyError as e:
            response_body = {'message': f'Task body missing field {e}'}
            self._set_response(400, 'application/json')

        else:
            try:
                logger.debug('Running algorithm on URL {}'.format(image_url))
                result = classifier.run_on_url(image_url)
                response_body = {'result': result}
                self._set_response(200, 'application/json')

            except exceptions.RequestError as e:
                response_body = {'message': f'Error fetching request image, received {e.response.status_code}'}
                self._set_response(e.response.status_code, 'application/json')

            except Exception as e:
                response_body = {'message': 'Internal error'}
                self._set_response(500, 'application/json')

        self.wfile.write(json.dumps(response_body).encode('utf-8'))


if __name__ == '__main__':
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, ClassifierServer)
    try:
        logger.info('Listening on port {}'.format(PORT))
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
