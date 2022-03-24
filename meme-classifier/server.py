# from http.server import BaseHTTPRequestHandler, HTTPServer
# import json
# import os
# import logging
# import traceback
#
# import exceptions
#
# PORT = int(os.environ.get('PORT', 5000))
# LOG_LEVEL = os.environ.get('LOG_LEVEL', '')
#
# log_level = getattr(logging, LOG_LEVEL, 'DEBUG')
# logging.basicConfig(level=log_level, format='%(levelname)s :: %(message)s')
# logger = logging.getLogger('Server')
#
# import classifier
#
#
# class ClassifierServer(BaseHTTPRequestHandler):
#     def _set_response(self, code, content_type):
#         self.send_response(code)
#         self.send_header('Content-type', content_type)
#         self.end_headers()
#
#     def do_POST(self):
#         # Process request
#         try:
#             content_length = int(self.headers['Content-Length'])
#             body_raw = self.rfile.read(content_length)
#             body = json.loads(body_raw)
#             image_url = body['url']
#
#         except ValueError as e:
#             logger.error('ValueError while parsing body as JSON')
#             response_body = {'message': f'Task body not valid JSON: "{e}"'}
#             self._set_response(400, 'application/json')
#
#         except KeyError as e:
#             response_body = {'message': f'Task body missing field {e}'}
#             self._set_response(400, 'application/json')
#
#         else:
#             try:
#                 logger.info('Running classifier on URL'.format(image_url))
#                 label, score = classifier.run_on_url(image_url)
#                 response_body = {'label': label, 'score': float(f'{score:.5f}')}
#                 self._set_response(200, 'application/json')
#
#             except exceptions.RequestError as e:
#                 response_body = {'message': f'Error fetching request image, received {e.response.status_code}'}
#                 self._set_response(e.response.status_code, 'application/json')
#
#             except Exception as e:
#                 error_str = traceback.format_exc()
#                 response_body = {'message': '[x] Internal error', 'error': error_str}
#                 self._set_response(500, 'application/json')
#
#         self.wfile.write(json.dumps(response_body).encode('utf-8'))
#
#
# if __name__ == '__main__':
#     server_address = ('', PORT)
#     httpd = HTTPServer(server_address, ClassifierServer)
#     try:
#         logger.info('[+] Listening on port {}'.format(PORT))
#         httpd.serve_forever()
#     except KeyboardInterrupt:
#         pass
#     httpd.server_close()
