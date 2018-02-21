from abc import ABC, abstractmethod
from urllib import request

import configs


class Parser(ABC):

    SITE_URL = ""
    NOT_FOUND_STR = configs.NOT_FOUND_STR

    def __init__(self, identifiers):
        self.identifiers = identifiers

    def parse(self):
        return [self.get_product_data(identifier) for identifier in self.identifiers]

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
    def get_product_data(cls, product_id):
        pass
