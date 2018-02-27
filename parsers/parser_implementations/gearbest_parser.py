import re
import urllib

from urllib import request
from lxml import etree
from configs import GEARBEST_URL, RU_GEARBEST_URL
from parsers.parser import Parser


class GearbestParser(Parser):
    SITE_URL = GEARBEST_URL
    RU_SITE_URL = RU_GEARBEST_URL

    @classmethod
    def get_product_url(cls, product_id):

        url = cls.NOT_FOUND_STR

        try:
            req = cls.get_fake_agent_req(GearbestParser.SITE_URL + '/' + str(product_id) + '-_gear/')
            page = etree.HTML(urllib.request.urlopen(req).read().decode("utf-8"))
            url = page.cssselect('.all_proNamContent')[0].getchildren()[0].attrib['href']
        except BaseException:
            try:
                req = cls.get_fake_agent_req(GearbestParser.RU_SITE_URL + '/' + str(product_id) + '-_gear/')
                page = etree.HTML(urllib.request.urlopen(req).read().decode("utf-8"))
                url = page.cssselect('.all_proNamContent')[0].getchildren()[0].attrib['href']
            except BaseException:
                pass

        return url

    @classmethod
    def get_product_data(cls, product_id):

        product_data = {'id': product_id, 'price': cls.NOT_FOUND_STR, 'name': cls.NOT_FOUND_STR, 'size': cls.NOT_FOUND_STR, 'weight': cls.NOT_FOUND_STR, 'url': cls.get_product_url(product_id)}
        sizes_and_weight_str = ""
        page = None

        try:
            req = cls.get_fake_agent_req(product_data['url'])
            page = etree.HTML(urllib.request.urlopen(req).read().decode("utf-8"))
            product_data["name"] = page.cssselect('.goods-info-top')[0].getchildren()[0].xpath("string()")
            product_data['price'] = page.cssselect('.my_shop_price')[0].xpath("string()")
            sizes_and_weight_str = page.xpath("//td[re:match(text(), 'weight')]", namespaces={"re": "http://exslt.org/regular-expressions"})[0].xpath('string()')
        except BaseException:
            try:
                sizes_and_weight_str = page.xpath("//td[re:match(text(), 'Вес')]", namespaces={"re": "http://exslt.org/regular-expressions"})[0].xpath('string()')
            except BaseException:
                pass

        try:
            product_data["size"] = sizes_and_weight_str.split(re.findall(r'Package size*: ', sizes_and_weight_str)[0])[1].split(' cm /')[0].split(' x ')
        except BaseException:
            try:
                product_data["size"] = sizes_and_weight_str.split(re.findall(r'Размер упаковки*: ', sizes_and_weight_str)[0])[1].split(' см /')[0].split(' x ')
            except BaseException:
                pass

        try:
            product_data["weight"] = sizes_and_weight_str.split('Package weight: ')[1].split(' kg')[0].replace('.', ',')
        except BaseException:
            try:
                product_data["weight"] = sizes_and_weight_str.split('Вес упаковки: ')[1].split(' кг')[0].replace('.', ',')
            except BaseException:
                pass

        return product_data
