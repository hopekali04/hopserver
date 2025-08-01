from http.server import HTTPServer
from request_handler import RequestHandler

if __name__ == '__main__':
    serverAddress = ('', 7000)
    print(f'server Started on port {serverAddress[1]}...')
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
