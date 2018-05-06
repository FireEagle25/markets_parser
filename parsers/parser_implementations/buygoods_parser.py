import functools
import re
import urllib

from urllib import request
from urllib.error import URLError

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
            print('Ссылка успешно найдена')
        except IndexError:
            print('Не удается найти ссылку на странице')
        except URLError:
            print('Не удается получить доступ к сайту')
        return url

    @classmethod
    def get_product_data(cls, product_id):
        print(product_id)

        product_data = {'id': product_id, 'price': cls.NOT_FOUND_STR, 'name': cls.NOT_FOUND_STR, 'size': cls.NOT_FOUND_STR, 'weight': cls.NOT_FOUND_STR, 'url': cls.get_product_url(product_id)}
        page = None

        try:
            req = cls.get_fake_agent_req(product_data['url'])
            page = etree.HTML(urllib.request.urlopen(req).read().decode("utf-8"))
            product_data["name"] = page.xpath(("(//h1[@itemprop='name'])"))[0].xpath('string()')
            print('Название успешно найдено')
            product_data['price'] = page.xpath(("(//span[@class='my_shop_price'])"))[0].xpath('string()').replace('.', ',').replace('$', '').replace('р.', '')
            print('Цена успешно найдена')
        except BaseException:
            pass

        try:
            weights = [float(re.split('[Kk][Gg]', weight_td.xpath('string()'))[0]) for weight_td in page.xpath("//td[re:match(., '[Kk][Gg]') and @align='left']", namespaces={"re": "http://exslt.org/regular-expressions"})]
            product_data["weight"] = str(max(weights)).replace('.', ',')

            print('Вес успешно найдены')
        except BaseException:
            pass

        try:
            sizes = [sizes_td.xpath('string()').split('cm')[0].split(' x ') for sizes_td in page.xpath("//td[re:match(., '[\d\.\d]+ x [\d\.\d]+ x [\d\.\d]+ cm') and @align='left']",
                                  namespaces={"re": "http://exslt.org/regular-expressions"})]
            product_data["size"] = functools.reduce(lambda x,y: x if float(x[0]) > float(y[0]) else y, sizes)
            print('Размер успешно найден')
        except BaseException:
            pass

        try:
            product_data["image"] = cls.download_image(page.cssselect('.jqzoom')[0].getchildren()[0].attrib['src'])
            print('Изображение успешно найдено')
        except BaseException:
            print('Не удалось найти изображение')

        return product_data