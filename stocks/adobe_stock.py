from contracts.ftp.ftp_stock import FtpStock


class AdobeStock(FtpStock):
    service_name = 'Adobe Stock'

    def retrieve_photo(self, model):
        if 4 <= model['mp'] <= 100 and model['weight'] <= 45:
            return True
        return False
