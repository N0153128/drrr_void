import sys
import requests
import mimetypes
from os import path
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import click


class Uploader:
    def __init(self, filename, file_host_url):
        self.filename = filename
        self.file_host_url = file_host_url

    def _multipart_post(self, data):
        encoder = MultipartEncoder(fields=data)
        monitor = MultipartEncoderMonitor(encoder)
        r = requests.post(self.file_host_url,
                          data=monitor,
                          headers={'Content-Type': monitor.content_type})
        return r

class FileioUploader(Uploader):
    def __init__(self, filename):
        self.filename = filename
        self.file_host_url = "https://file.io"

    def execute(self):
        file = open(self.filename, 'rb')
        try:
            data = {'file': (file.name, file, self._mimetype())}
            response = self._multipart_post(data)
        finally:
            file.close()

        return response.json()['link']


class CatboxUploader(Uploader):
    def __init__(self, filename):
        self.filename = filename
        self.file_host_url = "https://catbox.moe/user/api.php"

    def execute(self):
        file = open(self.filename, 'rb')
        try:
            data = {
                'reqtype': 'fileupload',
                'userhash': 'd4536907ecfa84d32cb37d993',
                'fileToUpload': (file.name, file)
            }
            response = self._multipart_post(data)
        finally:
            file.close()

        return response.text




uploader_classes = {
    "catbox": CatboxUploader,
    "fileio": FileioUploader
}




def upload(host, name):
	uploader_class = uploader_classes[host]
	uploader_instance = uploader_class(name)
	print(name)
	result = uploader_instance.execute()
	print("Your link : {}".format(result))


upload(host = 'catbox',name = '3.mp3')