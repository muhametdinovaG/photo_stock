from abc import ABCMeta, abstractmethod
import ftplib
import re
from urllib import request
from io import BytesIO
from contracts.stock import Stock


class FtpStock(Stock):
    server = None
    username = None
    password = None

    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password

    # Проверка модели на условия
    # Returns bool
    @abstractmethod
    def retrieve_photo(self, model):
        pass

    def upload(self, model):
        ftp = ftplib.FTP(self.server, self.username, self.password)
        ftp.getwelcome()

        photo_url = model['url']
        try:
            response = request.urlopen(photo_url)
        except:
            return "404: Файл не существует"

        photo_bytes = BytesIO(response.read())
        photo_name = re.search('[^/]*$', photo_url).group(0)

        answer = None
        try:
            answer = ftp.storbinary("STOR " + photo_name, photo_bytes, 1024)
        except:
            answer = "Не отправилось в " + self.server

        return answer
