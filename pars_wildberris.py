# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent


url_get = 'https://card.wb.ru/cards/detail?spp=0&regions=80,4,38,70,69,86,30,40,48,1,' \
          '112&pricemarginCoeff=1&reg=0&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=' \
          '2,12,7,6,9,21,11&dest=-1221185,-147166,-1749247,123585533&nm='
urls_user = ['https://www.wildberries.ru/catalog/26480523/detail.aspx?targetUrl=EX',
             'https://www.wildberries.ru/catalog/91245274/detail.aspx?targetUrl=MI',
             'https://www.wildberries.ru/catalog/2025364/detail.aspx?targetUrl=MI',
             'https://www.wildberries.ru/catalog/112729350/detail.aspx',
             'https://www.wildberries.ru/catalog/65126334/detail.aspx?size=113816546']


def defines_product_id(urls_user: str):
    """Из url id товара"""
    try:
        url_list = urls_user.split('/')
        id_prod = filter(lambda x: x.isnumeric(), url_list)
        return list(id_prod)[0]
    except IndexError:
        return False


def img_by_id(id_ph):
    headers = {'User-Agent': UserAgent().chrome}
    basket = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
    for i in basket:
        s = f'https://basket-{i}.wb.ru/vol{id_ph[:-5]}/part{id_ph[:-3]}/{id_ph}/images/big/1.jpg'
        img_link = requests.get(s)
        if img_link.status_code != 404:
            # with open(f"{id_ph+i}.jpg", 'wb') as file:
            #     file.write(img_link.content)
            return s


def generates_link_request(id_prod):
    """ get запрос по id, возращает словарь с полным описанием товара"""
    headers = {'User-Agent': UserAgent().chrome}
    url_get_user = url_get + id_prod
    req = requests.get(url_get_user, headers)
    return req.json()


def selects_values(js_dict):
    """Выбирает нужные характеристики"""
    a = ['id', 'name', 'salePriceU']
    dict_bd = {}
    for i in js_dict['data']['products'][0].items():
        if i[0] in a:
            dict_bd.setdefault(i[0], i[1])
    return dict_bd


def all_pars(url):
    # for i in url:
    id_all = defines_product_id(url)
    lin = img_by_id(str(id_all))
    a = generates_link_request(id_all)
    all_bd = (selects_values(a))
    all_bd.setdefault('link_photo', lin)
    all_bd.setdefault('link', url)
    return all_bd


def parsing_evry_day(url):
    id_all = defines_product_id(url)
    a = generates_link_request(id_all)
    all_bd = (selects_values(a))
    return all_bd



