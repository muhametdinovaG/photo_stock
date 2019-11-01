from contracts.ftp.ftp_stock import FtpStock


class PixtaStock(FtpStock):
    service_name = 'Pixta Stock'

    def retrieve_photo(self, model):
        if model['px'] >= 1301:
            return True
        return False
