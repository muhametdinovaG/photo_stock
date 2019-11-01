import datetime
from iconsapi import IconsApi
from database import StockDatabase
from stocks.adobe_stock import AdobeStock
from stocks.pixta_stock import PixtaStock

DATABASE_NAME = 'stock.db'


class Worker:
    api = None
    db = None
    services = [
        AdobeStock('ftp.contributor.adobestock.com', '208906643', '6876b505'),
        PixtaStock('eu-ftp.pixta.jp', '1501797', 'FlkumyJn'),
    ]

    def __init__(self):
        self.api = IconsApi(10)
        self.db = StockDatabase()
        self.db.open(DATABASE_NAME)

    def start(self, upload_limit=10):
        current_page = 1
        uploaded = 0

        models = self.api.get_models(current_page)
        working = True
        print("Upload to {0} service's starting. Limited to {1} items".format(len(self.services), upload_limit))
        while working:
            print("Retrieve {0} models from {1} page...".format(len(models), current_page))
            for model in models:
                for service in self.services:
                    db_data = self.db.find_file(model['id'], service.get_name())
                    if not db_data:
                        if service.retrieve_photo(model):
                            print("Upload {0} model...".format(model['id']))
                            result = service.upload(model)
                            self.db.write_report(
                                model['id'],
                                service.get_name(),
                                datetime.datetime.now(),
                                result
                            )
                            uploaded += 1
                # т.к. у нас может быть несколько сервисов, правильнее будет
                # считать общее кол-во загрузок по всем сервисам (т.е. 1 фото в 2 сервиса = 2 загрузкам)
                # а чтобы посчитать кол-во загрузок конкретно по фото,
                # без привязки к сервису, то общее делим на кол-во сервисов
                print("Currently uploaded: {0}/{1}".format(round(uploaded / len(self.services)), upload_limit))
                if uploaded == upload_limit:
                    working = False
                    break
            if working:
                current_page += 1
                models = self.api.get_models(current_page)
                if not models:
                    working = False
