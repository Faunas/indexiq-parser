import datetime
import time

import fake_useragent
import requests
import telebot
from bs4 import BeautifulSoup
from telebot import types

from db import *

url_14pro_128_white_iphone = "https://indexiq.ru/product/apple-iphone-14pro-max-128gb-silver/"
url_airpods13 = "https://indexiq.ru/product/apple-airpods-3-mpny3/"
url_14promax_128_purple_iphone = "https://indexiq.ru/product/apple-iphone-14-pro-128gb-deep-purple/"
url_airpods2color_violet = "https://indexiq.ru/product/apple-airpods-2-color-matte-violet/"
url_MacBook_Pro_13_512Gb_Silver = "https://indexiq.ru/product/apple-macbook-pro-13-512gb-silver-mneq3/"
url_airpods_2019 = "https://indexiq.ru/product/apple-airpods-2019-mv7n2/"
url_airpods_pro_with_magsafe_case = "https://indexiq.ru/product/apple-airpods-pro-with-magsafe-case-mlwk3/"

BOT_TOKEN = TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

all_chat_ids = [&&&]

PRODUCTS = {
    1: {'name': 'iphone14pro_white_128', 'price': 'constant_iphone14pro_white_128_price',
        'url': f'{url_14pro_128_white_iphone}'},
    2: {'name': 'iphone14promax_deeppurple_128', 'price': 'constant_iphone14promax_deeppurple_128_price',
        'url': f'{url_14promax_128_purple_iphone}'},
    3: {'name': 'airpods3_iphone', 'price': 'constant_airpods3_iphone_price', 'url': f'{url_airpods13}'},
    4: {'name': 'MacBook_Pro_13_512Gb_Silver', 'price': 'constant_MacBook_Pro_13_512Gb_Silver',
        'url': f'{url_MacBook_Pro_13_512Gb_Silver}'},
    5: {'name': 'airpods2color_violet', 'price': 'constant_airpods2color_violet', 'url': f'{url_airpods2color_violet}'},
    6: {'name': 'airpods_2019', 'price': 'constant_airpods_2019', 'url': f'{url_airpods_2019}'},
    7: {'name': 'airpods_pro_with_magsafe_case', 'price': 'constant_airpods_pro_with_magsafe_case',
        'url': f'{url_airpods_pro_with_magsafe_case}'}
}


def send_message_to_tg(brand_name, constant_white_iphone_price, new_product_price, const_price, product_price,
                       link_to_product, emoji, start_time, product_id):
    global uptime, time_prefix
    last_activity = ""
    curency_change = "***"
    curency_emoji = ""
    time_prefix = ""
    uptime = 1
    razniza = abs(product_price - const_price)
    if product_price - const_price > 0:
        curency_change = f"Повышение цены на {razniza}".replace("(", "").replace("'", "").replace(",", "")
        curency_emoji = "📈"
    elif product_price - const_price < 0:
        curency_change = f"Понижение цены на {razniza}".replace("(", "").replace("'", "").replace(",", "")
        curency_emoji = "📉"

    if (round(time.time() - start_time)) // 60 // 60 > 1:
        uptime = (round(time.time() - start_time)) // 60 // 60
        time_prefix = "час(ов)"
    elif (round(time.time() - start_time)) // 60 > 1:
        uptime = round(time.time() - start_time) // 60
        time_prefix = "минут"
    elif (round(time.time() - start_time)) < 60:
        uptime = round(time.time() - start_time)
        time_prefix = "секунд"

    button_text = "Открыть ссылку на товар"
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text=button_text, callback_data="open_product_url", url=link_to_product)
    keyboard.add(button)
    max_price = max_price_from_db(product_id)
    min_price = min_price_from_db(product_id)
    messages = f"{emoji} Цена на {brand_name} изменилась. \n Прошлая цена: {constant_white_iphone_price} \n Новая " \
               f"цена: {new_product_price}\n {curency_emoji} Последняя активность: {curency_change} \n ⏳Аптайм {uptime} {time_prefix}\n" \
               f"😱Максимальная цена: {max_price} руб.\n" \
               f"🤑Минимальная цена: {min_price}"
    for bot_clients in all_chat_ids:
        bot.send_message(chat_id=bot_clients, text=messages, disable_web_page_preview=True, reply_markup=keyboard)
    # bot.send_message(chat_id=chat_ID1, text=messages, disable_web_page_preview=True, reply_markup=keyboard)
    # Запись в файл
    text = messages
    fp = open('products_price_logs.txt', 'a', encoding='utf-8')
    fp.write(f"\n{datetime.datetime.now().replace(microsecond=0)} \n-----------------" + text + "\n----------------")
    fp.close()
    print("Изменение цены записаны в файл.")


def update_product_prices():
    for product_id, product in PRODUCTS.items():
        try:
            if product.get('url'):
                price = last_product_price(product_id)
            else:
                price = globals()[product['price']]
            print(f"Цена на отслеживаемый товар {product['name']}: {price}")
        except Exception:
            print(f"Отсутствует PRODUCT ID {product_id} в базе данных. Выполняю добавление.")
            add_empty_object_with_unical_product_id(product_id=product_id)


def surf_the_product(product_url):
    products = {
        "https://indexiq.ru/product/apple-iphone-14-pro-128gb-deep-purple/": {
            "const_price": last_product_price(2),
            "emoji": "🔮📱",
            "product_id": 2
        },
        "https://indexiq.ru/product/apple-airpods-3-mpny3/": {
            "const_price": last_product_price(3),
            "emoji": "🎧3",
            "product_id": 3
        },
        "https://indexiq.ru/product/apple-iphone-14pro-max-128gb-silver/": {
            "const_price": last_product_price(1),
            "emoji": "⚪️📱",
            "product_id": 1
        },
        "https://indexiq.ru/product/apple-macbook-pro-13-512gb-silver-mneq3/": {
            "const_price": last_product_price(4),
            "emoji": "🖥⚪️",
            "product_id": 4
        },
        "https://indexiq.ru/product/apple-airpods-2-color-matte-violet/": {
            "const_price": last_product_price(5),
            "emoji": "🎧️💜",
            "product_id": 5
        },
        "https://indexiq.ru/product/apple-airpods-2019-mv7n2/": {
            "const_price": last_product_price(6),
            "emoji": "🎧2019",
            "product_id": 6
        },
        "https://indexiq.ru/product/apple-airpods-pro-with-magsafe-case-mlwk3/": {
            "const_price": last_product_price(7),
            "emoji": "🎧magsafe",
            "product_id": 7
        }
    }

    if product_url in products:
        product = products[product_url]
        const_price = product["const_price"]
        print(f"Константая цена (берется из бд) = {const_price}")
        emoji_stick = product["emoji"]
        product_id = product["product_id"]
    else:
        print("Продукт не найден в списке.")

    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    responce = requests.get(product_url, headers=header).text
    soup = BeautifulSoup(responce, "lxml")
    brand_name = soup.find("h1", itemprop="name").text.replace("Смартфон", "").replace('Беспроводные наушники', "")
    product_link = soup.find("link", itemprop="url").get("href")
    old_product_price = soup.find("span", itemprop="price").text.replace(".", "")
    product_price = int(old_product_price[0:len(old_product_price) - 2])
    max_price = max_price_from_db(product_id)
    min_price = min_price_from_db(product_id)
    print(f"Цена на товар: {const_price}")
    if product_price == const_price:
        print(f"Последняя дата проверки: {datetime.datetime.now().replace(microsecond=0)}")
        print(f"Товар: {brand_name})\n"
              f"Цена: {product_price}\n"
              f"Максимальная цена: {max_price}\n")

    if product_price != const_price:
        if time.time() - start_time > 10:
            print(f"---------------------------------------\n"
                  f"Цена на {brand_name} изменилась. \n Прошлая цена: {const_price}"
                  f" \n Новая цена: {product_price}\n"
                  f"---------------------------------------")
            write_change_price(product_id, old_price=const_price, new_price=product_price)
            send_message_to_tg(brand_name, const_price, product_price, const_price, product_price,
                               link_to_product=product_link, emoji=emoji_stick, start_time=start_time,
                               product_id=product_id)



def main():
    # surf_the_product(url_14promax_128_purple_iphone)
    surf_the_product(url_airpods13)
    # surf_the_product(url_14pro_128_white_iphone)
    # surf_the_product(url_MacBook_Pro_13_512Gb_Silver)
    surf_the_product(url_airpods2color_violet)
    surf_the_product(url_airpods_2019)
    surf_the_product(url_airpods_pro_with_magsafe_case)


if __name__ == "__main__":
    print(f"✅ Начал выполнять работу в {datetime.datetime.now().replace(microsecond=0)}")
    start_time = time.time()
    update_product_prices()
    while True:
        main()
