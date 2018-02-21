import re
import urllib

from urllib import request
from lxml import etree

from configs import BUYINGGOODS_URL
from parsers.parser import Parser


class BuygoodsParser(Parser):

    SITE_URL = BUYINGGOODS_URL

    @classmethod
    def get_product_url(cls, product_id):

        url = cls.NOT_FOUND_STR

        try:
            req = cls.get_fake_agent_req(BuygoodsParser.SITE_URL + '/' + str(product_id) + '-_bulk/')
            page = etree.HTML(urllib.request.urlopen(req).read().decode("utf-8"))
            url = page.cssselect('.all_proNam')[0].getchildren()[0].attrib['href']
        finally:
            return url

    @classmethod
    def get_product_data(cls, product_id):

        product_data = {'id': product_id, 'name': cls.NOT_FOUND_STR, 'size': cls.NOT_FOUND_STR, 'weight': cls.NOT_FOUND_STR, 'url': cls.get_product_url(product_id)}
        page = None

        try:
            req = cls.get_fake_agent_req(product_data['url'])
            page = etree.HTML(urllib.request.urlopen(req).read().decode("utf-8"))
            product_data["name"] = page.cssselect('.goods_info_inner')[0].getchildren()[0].xpath("string()")
        except BaseException:
            pass

        try:
            product_data["weight"] = page.xpath("//td[re:match(text(), 'Package weight')]", namespaces={"re": "http://exslt.org/regular-expressions"})[0].getparent().getchildren()[1].xpath("string()").split(' ')[0]
        except BaseException:
            pass

        try:
            product_data["size"] = page.xpath("//td[re:match(text(), 'Package size')]", namespaces={"re": "http://exslt.org/regular-expressions"})[0].getparent().getchildren()[1].xpath("string()").split('cm /')[0].split(' x ')
        except BaseException:
            pass

        return product_data