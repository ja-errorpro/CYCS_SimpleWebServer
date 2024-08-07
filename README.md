# Simple HTTP Web Server

* Python 3.10

## TODO

1. Opera Browser cannot post form data to server
2. favicon

## Usage

```bash
python3 server.py
```

### And test your methods in Postman 

## Available Paths

* / - (GET)index.html, Home page, if user is admin, will show upload button
* /dashboard - (GET)Will redirect to login page
* /login - (GET)Change username here
* /upload - (POST)Upload files here(Only admin can upload)


## Available HTTP Status Codes

* 200 - OK
* 301 - Moved Permanently
* 400 - Bad Request
* 404 - Not Found
* 505 - HTTP Version Not Supported

## Available HTTP Methods

* GET
* POST
* HEAD
* PUT
* DELETE



## Available Content Types

```python
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
```

