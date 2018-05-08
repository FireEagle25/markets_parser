import re
import urllib

from urllib import request
from urllib.error import URLError

from lxml import etree
from configs import GEARBEST_URL, RU_GEARBEST_URL
from parsers.parser import Parser


class GearbestParser(Parser):
    SITE_URL = GEARBEST_URL
    RU_SITE_URL = RU_GEARBEST_URL

    @classmethod
    def get_product_url(cls, product_id, image_download=False):

        url = cls.NOT_FOUND_STR

        try:
            req = cls.get_fake_agent_req(GearbestParser.SITE_URL + '/' + str(product_id) + '-_gear/')
            page = etree.HTML(urllib.request.urlopen(req).read().decode("utf-8"))
            url = page.cssselect('.gbGoodsItem_thumb')[0].attrib['href']
            print('Ссылка успешно найдена')
        except IndexError:
            print("Не удается найти ссылку на англиской версии сайта")
            try:
                req = cls.get_fake_agent_req(GearbestParser.RU_SITE_URL + '/' + str(product_id) + '-_gear/')
                page = etree.HTML(urllib.request.urlopen(req).read().decode("utf-8"))
                url = page.cssselect('.gbGoodsItem_thumb')[0].attrib['href']
                print('Ссылка успешно найдена')
            except IndexError:
                print("Не удается найти ссылку на русской версии сайта")
        except URLError:
            print('Не удается получить доступ к сайту')


        return url

    @classmethod
    def get_product_data(cls, product_id, image_download):
        print(product_id)

        product_data = {'id': product_id, 'price': cls.NOT_FOUND_STR, 'name': cls.NOT_FOUND_STR, 'size': cls.NOT_FOUND_STR, 'weight': cls.NOT_FOUND_STR, 'url': cls.get_product_url(product_id), 'image': cls.NOT_FOUND_STR}
        sizes_and_weight_str = ""
        page = None

        try:
            req = cls.get_fake_agent_req(product_data['url'])
            page = etree.HTML(urllib.request.urlopen(req).read().decode("utf-8"))
            product_data["name"] = page.cssselect('.goodsIntro_title')[0].xpath("string()").lstrip().replace('\n', '')
            print('Название успешно найдено')
            product_data['price'] = re.findall(r"[-+]?\d*\.\d+|\d+", page.cssselect('.goodsIntro_price')[0].xpath("string()"))[0].replace('.', ',')
            print('Цена успешно найдена')
            sizes_and_weight_str = page.xpath("//td[re:match(., '[Ww]eight.* kg')]", namespaces={"re": "http://exslt.org/regular-expressions"})
            if not sizes_and_weight_str:
                sizes_and_weight_str = page.xpath("//td[re:match(., '[Ww]eight')]", namespaces={"re": "http://exslt.org/regular-expressions"})
                if not sizes_and_weight_str:
                    sizes_and_weight_str = page.xpath("//*[re:match(., '[Ww]eight')]", namespaces={"re": "http://exslt.org/regular-expressions"})

            sizes_and_weight_str = sizes_and_weight_str[0].xpath('string()')
        except BaseException:
            try:
                sizes_and_weight_str = page.xpath("//td[re:match(., '[Вв]ес.* кг')]", namespaces={"re": "http://exslt.org/regular-expressions"})[0].xpath('string()')
            except BaseException:
                pass

        try:
            product_data["size"] = sizes_and_weight_str.split(re.findall(r'(Package [Ss]ize.*:|Package [Dd]imensi.*:)', sizes_and_weight_str)[0])[1].split(' cm')[0].split(' x ')
            print('Размеры успешно найдены')
        except BaseException:
            try:
                product_data["size"] = sizes_and_weight_str.split(re.findall(r'Размер упаковки.*: ', sizes_and_weight_str)[0])[1].split(' см')[0].split(' x ')
                print('Размеры успешно найдены')
            except BaseException:
                pass
        finally:
            for size in product_data['size']:
                if re.match(r'^.*$', size) is None:
                    product_data["size"] = cls.NOT_FOUND_STR

        try:
            product_data["weight"] = sizes_and_weight_str.split('Package weight: ')[1].split('kg')[0].replace('.', ',')
            print('Вес успешно найден')
        except BaseException:
            try:
                product_data["weight"] = sizes_and_weight_str.split('Weight: ')[1].split('kg')[0].replace('.', ',')
            except BaseException:
                try:
                    product_data["weight"] = sizes_and_weight_str.split('Вес упаковки: ')[1].split(' кг')[0].replace('.', ',')
                    print('Вес успешно найден')
                except BaseException:
                    pass
        finally:
            if re.match(r'^.*$', product_data["weight"]) is None:
                product_data["weight"] = cls.NOT_FOUND_STR

        if image_download:
            try:
                product_data["image"] = cls.download_image(page.cssselect('.goodsIntro_largeImgWrap')[0].getchildren()[0].attrib['src'])
                print('Изображение успешно найдено')
            except BaseException:
                print('Не удалось найти изображение')

        return product_data
