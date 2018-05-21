import urllib
from abc import ABC, abstractmethod
from urllib import request

import os
from progress.bar import ChargingBar

import configs


class Parser(ABC):

    SITE_URL = ""
    NOT_FOUND_STR = configs.NOT_FOUND_STR

    def __init__(self, identifiers, image_download):
        self.identifiers = identifiers
        self.image_download = image_download

    def parse(self):
        bar = ChargingBar('Завершено', max=len(self.identifiers))

        products_data = []
        for identifier in self.identifiers:
            products_data.append(self.get_product_data(identifier, self.image_download))
            bar.next()
        bar.finish()

        return products_data

    @staticmethod
    def get_fake_agent_req(url):
        return request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )

    @classmethod
    @abstractmethod
    def get_product_url(cls, product_id):
        pass

    @classmethod
    @abstractmethod
    def get_product_data(cls, product_id, image_download):
        pass

    @staticmethod
    def download_image(url, name):
        splitted_url = url.split('.')
        file_path = os.getcwd() + '/images/' + str(name) + '.' + splitted_url[len(splitted_url) - 1]
        urllib.request.urlretrieve(url, file_path)
        return file_path
