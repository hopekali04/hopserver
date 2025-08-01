import os
import subprocess

class base_case(object):
    '''Parent for case handlers.'''
    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        assert False, 'Not implemented.'

    def act(self, handler):
        assert False, 'Not implemented.'

class case_no_file(object):
    def test(self, handler):
        return not os.path.exists(handler.full_path)
    def act(self, handler):
        raise Exception("'{0}' not found".format(handler.path))

class case_existing_file(base_case):
    def test(self, handler):
        return os.path.isfile(handler.full_path)
    def act(self, handler):
        self.handle_file(handler, handler.full_path)

class case_always_fail(object):
    def test(self, handler):
        return True
    def act(self, handler):
        raise Exception("Unknown object '{0}'".format(handler.path))

class case_cgi_file(object):
    def test(self, handler):
        return os.path.isfile(handler.full_path) and handler.full_path.endswith('.py')
    def act(self, handler):
        self.run_cgi(handler, handler.full_path)
    def run_cgi(self, handler, full_path):
        try:
            proc = subprocess.Popen(['python', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            if proc.returncode != 0:
                handler.handle_error(stderr.decode())
            else:
                handler.send_content(stdout)
        except Exception as e:
            handler.handle_error(str(e))

class case_directory_index_file(object):
    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')
    def test(self, handler):
        return os.path.isdir(handler.full_path) and os.path.isfile(self.index_path(handler))
    def act(self, handler):
        handler.handle_file(self.index_path(handler))

class case_directory_no_index_file(object):
    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')
    def test(self, handler):
        return os.path.isdir(handler.full_path) and not os.path.isfile(self.index_path(handler))
    def act(self, handler):
        handler.list_dir(handler.full_path)