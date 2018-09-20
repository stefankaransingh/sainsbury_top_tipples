import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import jsonify

def get_target_page_html(url=None):
    response = requests.get(url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def parse_offer_item(item=None):
    item_name = item.findAll('p',{'class':'productName'})[0].string
    item_strap_line = item.findAll('div',{'class':'promoStrapline'})[0].findAll('a')[0].text

    start = item_strap_line.find('£')
    stop = item_strap_line.find(':')
    item_price = float(item_strap_line[start+1:stop])

    save_index = item_strap_line.find('Save ')
    item_save_value = item_strap_line[save_index+5: ].rstrip()

    if 'p' in item_save_value:
        item_save_amount = float('0.'+ item_save_value.replace('p',''))
    elif '£'in item_save_value:
        item_save_amount = float(item_save_value.replace('£',''))
    else:
        item_save_amount = 0

    return item_name,item_price,item_save_value,item_save_amount

def get_offers(threshold_price = None):
    soup = get_target_page_html('https://www.sainsburys.co.uk/shop/gb/groceries/find-great-offers/top-tipple')
    great_offers= soup.findAll('div', {'class': 'greatOffersItem'})
    items_name = []
    items_prices = []
    items_save_value = []
    items_save_amount = []
    for item in great_offers:
        item_name,item_price,item_save_value,item_save_amount = parse_offer_item(item)
        if threshold_price == None or item_price < threshold_price:
            items_name.append(item_name)
            items_prices.append(item_price)
            items_save_value.append(item_save_value)
            items_save_amount.append(item_save_amount)

    return items_name,items_prices,items_save_value,items_save_amount


def get_huge_savings():
    items_name,items_prices,items_save_value,items_save_amount = get_offers()
    max_save_amount = max(items_save_amount)

    max_save_items_name = []
    max_save_items_price = []
    max_save_items_save_value = []

    for item_name,item_price,item_save_value,item_save_amount in zip(items_name,items_prices,items_save_value,items_save_amount):
        if item_save_amount == max_save_amount:
            max_save_items_name.append(item_name)
            max_save_items_price.append(item_price)
            max_save_items_save_value.append(item_save_value)
    return max_save_items_name,max_save_items_price,max_save_items_save_value


def jsonify_offer_list(items_name,items_price,items_save_value):
    data = {}
    for index,item in enumerate(zip(items_name,items_price,items_save_value)):
        data.update({index:{
                            'item_name':item[0],
                            'item_price':item[1],
                            'item_save_value':item[2]
        }})

    return jsonify(data)
