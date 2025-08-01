from http.server import BaseHTTPRequestHandler
import os
from cases import (
    case_no_file,
    case_cgi_file,
    case_existing_file,
    case_directory_index_file,
    case_directory_no_index_file,
    case_always_fail
)

class RequestHandler(BaseHTTPRequestHandler):
    Cases = [
        case_no_file(),
        case_cgi_file(),
        case_existing_file(),
        case_directory_index_file(),
        case_directory_no_index_file(),
        case_always_fail()
    ]

    Page = '''<html><body><table>
    <tr><td>Header</td><td>Value</td></tr>
    <tr><td>Date and time</td><td>{date_time}</td></tr>
    <tr><td>Client host</td><td>{client_host}</td></tr>
    <tr><td>Client port</td><td>{client_port}s</td></tr>
    <tr><td>Command</td><td>{command}</td></tr>
    <tr><td>Path</td><td>{path}</td></tr>
    </table></body></html>'''

    Error_Page = '''<html><body>
    <h1>Error accessing {path}</h1>
    <p>{msg}</p>
    </body></html>'''

    Listing_Page = '''<html><body><ul>{0}</ul></body></html>'''

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content, 404)

    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        if isinstance(content, str):
            content = content.encode('utf-8')
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def handle_file(self, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(self.path, msg)
            self.handle_error(msg)

    def list_dir(self, full_path):
        try:
            entries = os.listdir(full_path)
            bullets = ['<li>{0}</li>'.format(e) for e in entries if not e.startswith('.')]
            page = self.Listing_Page.format('\n'.join(bullets))
            self.send_content(page)
        except OSError as msg:
            msg = "'{0}' cannot be listed: {1}".format(self.path, msg)
            self.handle_error(msg)

    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path
            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break
        except Exception as msg:
            self.handle_error(msg)

    def create_page(self):
        values = {
            'date_time': self.date_time_string(),
            'client_host': self.client_address[0],
            'client_port': self.client_address[1],
            'command': self.command,
            'path': self.path
        }
        page = self.Page.format(**values)
        return page

    def send_page(self, page):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(page.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(page.encode('utf-8'))