'''
/index.html -> Home Page, if user is admin, you can upload files
/dashboard.html -> Redirect to /login (301)
/login.html -> Login Page, input username, the cookie will be set to user=username
'''

import socket

HOST = '0.0.0.0'
PORT = 8000
Not_Found_Page = 'public/404.html'
ENCODING = 'iso-8859-1'

class HTTPServer:

    responses = {
        200: ' 200 OK\r\n',
        301: ' 301 Moved Permanently\r\n',
        400: ' 400 Bad Request\r\nContent-Type: text/html\r\n\r\n<html><body><h1>400 Bad Request</h1></body></html>',
        404: ' 404 Not Found\r\nContent-Type: text/html\r\n\r\n',
        505: ' 505 HTTP Version Not Supported\r\nContent-Type: text/html\r\n\r\n<html><body><h1>505 HTTP Version Not Supported</h1></body></html>',
    }

    CONTENT_TYPES = {
        'html': 'Content-Type: text/html ; charset=utf-8\r\n\r\n',
        'css': 'Content-Type: text/css ; charset=utf-8\r\n\r\n',
        'js': 'Content-Type: text/javascript ; charset=utf-8\r\n\r\n',
        'jpg': 'Content-Type: image/jpeg\r\n\r\n',
        'jpeg': 'Content-Type: image/jpeg\r\n\r\n',
        'png': 'Content-Type: image/png\r\n\r\n',
        'gif': 'Content-Type: image/gif\r\n\r\n',
        'ico': 'Content-Type: image/x-icon\r\n\r\n',
        'json': 'Content-Type: application/json\r\n\r\n',
        'pdf': 'Content-Type: application/pdf\r\n\r\n',
        'zip': 'Content-Type: application/zip\r\n\r\n',
        'xml': 'Content-Type: application/xml\r\n\r\n',
        'mp3': 'Content-Type: audio/mpeg\r\n\r\n',
        'mp4': 'Content-Type: video/mp4\r\n\r\n',
        'wav': 'Content-Type: audio/wav\r\n\r\n',
        'txt': 'Content-Type: text/plain ; charset=utf-8\r\n\r\n',
        'csv': 'Content-Type: text/csv ; charset=utf-8\r\n\r\n',
        'doc': 'Content-Type: application/msword\r\n\r\n',
        'xls': 'Content-Type: application/vnd.ms-excel\r\n\r\n',
    }


    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.request_queue_size = 5
        self.protocol = 'HTTP/1.1'
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.request_queue_size)
        except Exception as e:
            print('Error: ', e)
            self.socket.close()

    def server_entrance(self):
        print(f'Server is running on {self.host}:{self.port}')
        while True:
            # Get request
            try:
                client_socket, client_address = self.socket.accept()
                print('Connected to ', client_address)
                self._process_request(client_socket, client_address)
            except KeyboardInterrupt:
                print('Server is shutting down...')
                break
            #except Exception as e:
            #    print('Error: ', e)
            #    client_socket.sendall((self.protocol + ' 500 Internal Server Error\r\n\r\n').encode())
            try:
                client_socket.shutdown(socket.SHUT_WR)
            except Exception as e:
                pass
            client_socket.close()

    def authenticate(self):
        for header in self.headers:
            if header == 'Cookie':
                cookie = self.headers[header].strip().split(';')
                for c in cookie:
                    if c.startswith('user='):
                        return True
                
        return False
    
    def is_admin(self):
        for header in self.headers:
            if header == 'Cookie':
                cookie = self.headers[header].strip().split(';')
                for c in cookie:
                    if c == 'user=admin':
                        return True
        return False
    
    def _response_404(self, reason = 'File Not Found'):
        print(f"Responsed: 404 Not Found ({reason})")
        response = self.protocol + self.responses[404]
        page = open(Not_Found_Page, 'r')
        response += page.read()
        return response
    
    def _get_favicon(self):
        return self._response_404('Favicon Not Found') # TODO
    
    def _get_content_type(self, path):
        if path.endswith('.html'):
            return self.CONTENT_TYPES['html']
        elif path.endswith('.css'):
            return self.CONTENT_TYPES['css']
        elif path.endswith('.js'):
            return self.CONTENT_TYPES['js']
        elif path.endswith('.jpg') or path.endswith('.jpeg'):
            return self.CONTENT_TYPES['jpg']
        elif path.endswith('.png'):
            return self.CONTENT_TYPES['png']
        elif path.endswith('.gif'):
            return self.CONTENT_TYPES['gif']
        elif path.endswith('.ico'):
            return self.CONTENT_TYPES['ico']
        elif path.endswith('.json'):
            return self.CONTENT_TYPES['json']
        elif path.endswith('.pdf'):
            return self.CONTENT_TYPES['pdf']
        elif path.endswith('.zip'):
            return self.CONTENT_TYPES['zip']
        elif path.endswith('.xml'):
            return self.CONTENT_TYPES['xml']
        elif path.endswith('.mp3'):
            return self.CONTENT_TYPES['mp3']
        elif path.endswith('.mp4'):
            return self.CONTENT_TYPES['mp4']
        elif path.endswith('.wav'):
            return self.CONTENT_TYPES['wav']
        elif path.endswith('.txt'):
            return self.CONTENT_TYPES['txt']
        elif path.endswith('.csv'):
            return self.CONTENT_TYPES['csv']
        elif path.endswith('.doc'):
            return self.CONTENT_TYPES['doc']
        elif path.endswith('.xls'):
            return self.CONTENT_TYPES['xls']
        else:
            return self.CONTENT_TYPES['txt']
        
        

    def _do_GET(self):
        if self.path.startswith('/favicon'):
            return self._get_favicon()
        elif self.path == '/':
            response = self.protocol + self.responses[200] + self.CONTENT_TYPES['html']
            page = open('public/index.html', 'r', encoding='utf-8')
            response += page.read()
            return response
        elif self.path == '/dashboard':
            return self.protocol + self.responses[301] + f'Location: http://{self.headers.get("Host").strip()}/login\r\n\r\n'
        else:
            try:
                response = self.protocol + self.responses[200] + self.CONTENT_TYPES['html']
                page = open('public' + self.path + '.html', 'r', encoding='utf-8')
                response += page.read()
                return response
            except FileNotFoundError:
                try:
                    response = self.protocol + self.responses[200] + self._get_content_type(self.path)
                    page = open(self.path[1:], 'rb')
                    response = response.encode(ENCODING) + page.read()
                    return response
                except FileNotFoundError:
                    return self._response_404()
                except PermissionError:
                    return self._response_404('Permission Denied')
                except IsADirectoryError:
                    return self._response_404('Is a Directory')
            except PermissionError:
                return self._response_404('Permission Denied')
            except IsADirectoryError:
                return self._response_404('Is a Directory')

    def _do_POST(self, http_data):
        
        if self.path != '/upload' and self.path != '/login':
            return self._response_404('Invalid POST Request')
        
        
        header_segments, body = http_data.split('\r\n\r\n', 1)
        content_type = self.headers.get('Content-Type', '')
        content_length = int(self.headers.get('Content-Length', 0))

        if 'multipart/form-data;' in content_type:
            if not self.is_admin():
                return self._response_404('Only Admin can upload files')
            boundary = content_type.split('boundary=')[1]
            body = body.split('--' + boundary)
            for b in body:
                if (not b) or b == '' or b.strip() == '--':
                    continue
                print('Body: ', b, '<<')
                body_headers, body_content = b.split('\r\n\r\n', 1)
                body_headers = body_headers.split('\r\n')
                file_name = ''
                for header in body_headers:
                    if 'filename=' in header:
                        file_name = header.split('filename="')[1].split('"')[0]
                        break
                if file_name:
                    with open('uploads/' + file_name, 'wb') as f:
                        f.write(body_content.encode(ENCODING))
            response = self.protocol + self.responses[200] + self.CONTENT_TYPES['html']
            page = open('public/success_upload.html', 'r', encoding='utf-8')
            response += page.read()
            return response
        elif 'application/x-www-form-urlencoded' in content_type:
            form_data = {}
            for data in body.split('&'):
                if (not data) or data == '':
                    continue
                key, value = data.split('=')
                form_data[key] = value
            if self.path == '/login':
                form_username = form_data.get('username', '')
                if form_username != '':
                    response = self.protocol + self.responses[200] + self.CONTENT_TYPES['html']
                    response = response.rstrip('\r\n') + f'\r\nSet-Cookie: user={form_username}\r\n\r\n'
                    page = open('public/success_login.html', 'r', encoding='utf-8')
                    response += page.read()

                    return response
                else:
                    return self.protocol + self.responses[400]
            else:
                return self._response_404('Invalid POST Request')
            
        # TODO: json, text/plain
        else:
            return self._response_404('Invalid POST Request')

        
            


    def _do_PUT(self, http_data):

        if not self.is_admin():
            return self.protocol + self.responses[400]

        if self.path == '/':
            return self.protocol + self.responses[400] # Cannot PUT to root
        path = '.' + self.path
        header_segments, body = http_data.split('\r\n\r\n', 1)

        try:
            file = open(path, 'wb')
            file.write(body.encode(ENCODING))
            file.close()
        except PermissionError:
            return self.protocol + self.responses[400] # Cannot write to file
        response = self.protocol + self.responses[200] + self.CONTENT_TYPES['html']
        response += '<html><body><h1>File Updated</h1></body></html>'
        return response
        


    def _do_DELETE(self):
        if not self.is_admin():
            return self.protocol + self.responses[400]

        if self.path == '/':
            return self.protocol + self.responses[400] # Cannot DELETE root
        path = '.' + self.path
        os = __import__('os')
        if os.path.exists(path):
            os.remove(path)
            response = self.protocol + self.responses[200] + self.CONTENT_TYPES['html']
            response += '<html><body><h1>File Deleted</h1></body></html>'
            return response
        else:
            return self._response_404('File Not Found')



    def _do_HEAD(self):
        if self.path == '/':
            response = self.protocol + self.responses[200] + self.CONTENT_TYPES['html']
            response = response.rstrip('\r\n')
            file = open('public/index.html', 'r', encoding='utf-8')
            content_length = len(file.read())
            response += f'\r\nDate: Sun, 1, Jan 2024 00:00:00 GMT\r\n'
            response += f'Content-Length: {content_length}\r\n\r\n'
            return response
        elif self.path == '/dashboard':
            return self.protocol + self.responses[301] + f'Location: http://{self.headers.get("Host").strip()}/login\r\n\r\n'
        else:
            try:
                response = self.protocol + self.responses[200] + self.CONTENT_TYPES['html']
                file = open('public' + self.path + '.html', 'r', encoding='utf-8')
                content_length = len(file.read())
                response += f'Date: Sun, 1, Jan 2024 00:00:00 GMT\r\n'
                response += f'Content-Length: {content_length}\r\n\r\n'
                return response
            except FileNotFoundError:
                try:
                    response = self.protocol + self.responses[200] + self._get_content_type(self.path)
                    file = open(self.path.strip('/'), 'r', encoding='utf-8')
                    content_length = len(file.read())
                    response += f'Date: Sun, 1, Jan 2024 00:00:00 GMT\r\n'
                    response += f'Content-Length: {content_length}\r\n\r\n'
                    return response
                except FileNotFoundError:
                    return self._response_404()
            


    def _get_response(self, request):
        
        
        if self.method == 'GET':
            return self._do_GET()
        elif self.method == 'POST':
            return self._do_POST(request)
        elif self.method == 'PUT':
            return self._do_PUT(request)
        elif self.method == 'DELETE':
            return self._do_DELETE()
        elif self.method == 'HEAD':
            return self._do_HEAD()
        else:
            print("Responsed: 400 Bad Request")
            return self.protocol + self.responses[400]

    def _parse_header(self, http_data):

        """
        {HTTP Method} {PATH} {HTTP Version}\r\n
        {Header Name}: {Header Value}\r\n
        ...
        \r\n
        {Body}
        """
        headers = {}
        header_segments = http_data.split('\r\n\r\n', 1)[0]
        for header in header_segments.split('\r\n'):
            if ':' not in header:
                continue
            key, value = header.split(':', 1)
            headers[key] = value

        return headers
        

    def _process_request(self, client_socket, client_address):
        http_data = client_socket.recv(4096)
        #print('Request: \n', http_data)
        self.headers = self._parse_header(str(http_data, ENCODING))
        content_length = int(self.headers.get('Content-Length', 0))
        while len(http_data) < content_length:
            http_data += client_socket.recv(4096)

        http_data = str(http_data, ENCODING)
        print('Request: ', http_data if len(http_data) < 1000 else http_data[:1000])

       # http_data = http_data.decode()
        method_path_version = http_data.split('\r\n')[0].split(' ')
        if len(method_path_version) == 3:
            method, path, version = method_path_version
            if version[:5] != 'HTTP/':
                print("Responsed: 400 Bad Request")
                client_socket.sendall((self.protocol + self.responses[400]).encode(ENCODING))
                return
            try:
                version = float(version[5:])
                if version < 1.0 or version > 1.1:
                    print("Responsed: 505 HTTP Version Not Supported")
                    client_socket.sendall((self.protocol + self.responses[505]).encode(ENCODING))
                    return
            except ValueError:
                print("Responsed: 400 Bad Request")
                client_socket.sendall((self.protocol + self.responses[400]).encode(ENCODING))
                return
        elif len(method_path_version) == 2:
            method, path = method_path_version
            version = 'HTTP/1.1'
        else:
            print("Responsed: 400 Bad Request")
            client_socket.sendall((self.protocol + self.responses[400]).encode(ENCODING))
            return
        
        self.method = method

        # if there is argument in path, parse it
        if '?' in path:
            self.args = {}
            path, arguments = path.split('?')
            arguments = arguments.split('&')
            for arg in arguments:
                key, value = arg.split('=')
                self.args[key] = value

        self.path = path
        self.version = version

        response = self._get_response(http_data)
        print("Responsed: ", response if len(response) < 1000 else response[:1000])
        client_socket.sendall(response.encode() if type(response) == str else response)


if __name__ == '__main__':
    server = HTTPServer(HOST, PORT)
    server.server_entrance()
