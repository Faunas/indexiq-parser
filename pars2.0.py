import requests
from bs4 import BeautifulSoup
import fake_useragent
import datetime
from time import sleep
import random
from notifiers import get_notifier
import time
import asyncio


def send_message_to_tg(brand_name, constant_white_iphone_price, new_product_price, const_price, product_price,
                       link_to_product, emoji, start_time):
    global uptime, time_prefix
    last_activity = ""
    curency_change = "***"
    curency_emoji = ""
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

    messages = f"{emoji} Цена на {brand_name} изменилась. \n Прошлая цена: {constant_white_iphone_price} \n Новая цена: {new_product_price} \n {curency_emoji} Последняя активность: {curency_change} \n ⏳Аптайм: {uptime} {time_prefix}\n 📎Ссылка на товар: \n{link_to_product}"
    telegram.notify(message=messages, token=TOKEN', chat_id=chat_ID1)
    # Запись в файл
    text = messages
    fp = open('products_price_logs.txt', 'a', encoding='utf-8')
    fp.write(f"\n{datetime.datetime.now().replace(microsecond=0)} \n-----------------" + text + "\n----------------")
    fp.close()
    print("Изменение цены записаны в файл.")


def surf_the_product(product_url):
    global constant_iphone14pro_white_128_price, constant_airpods3_iphone_price, \
        constant_iphone14promax_deeppurple_128_price, emoji_stick, start_time
    if product_url == "https://indexiq.ru/product/apple-iphone-14-pro-128gb-silver-esim-sim/":
        const_price = constant_iphone14pro_white_128_price
        emoji_stick = "⚪️📱"
    elif product_url == "https://indexiq.ru/product/apple-airpods-3-mpny3/":
        const_price = constant_airpods3_iphone_price
        emoji_stick = "🎧"
    elif product_url == "https://indexiq.ru/product/apple-iphone-14-pro-max-128gb-deep-purple-esim-sim//":
        const_price = constant_iphone14promax_deeppurple_128_price
        emoji_stick = "🔮📱"
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    url = product_url
    responce = requests.get(url, headers=header).text
    soup = BeautifulSoup(responce, "lxml")
    brand_name = soup.find("h1", itemprop="name").text.replace("Смартфон", "")
    soup.find("link", itemprop="url").get("href")
    old_product_price = soup.find("span", itemprop="price").text.replace(".", "")
    soup.find("span", itemprop="price").text.replace(".", "")
    product_price = int(old_product_price[0:len(old_product_price) - 2])
    print(f"Цена на товар: {const_price}")
    if int(product_price) == const_price:
        print(f"Последняя дата проверки: {datetime.datetime.now().replace(microsecond=0)}")
        print(f"Товар: {brand_name})\n"
              f"Цена: {product_price}")
    if int(product_price) != int(const_price):
        # print(f"product_price = {product_price} \n constant_white_iphone_price = {constant_iphone13promax_price}")
        print(
            f"---------------------------------------\n"
            f"Цена на {brand_name} изменилась. \n Прошлая цена: {const_price}"
            f" \n Новая цена: {product_price}\n"
            f"---------------------------------------")
        # Отправляем уведомление в телеграм
        send_message_to_tg(brand_name, const_price, product_price, const_price, product_price, link_to_product=url,
                           emoji=emoji_stick, start_time=start_time)
        if product_url == "https://indexiq.ru/product/apple-iphone-14-pro-128gb-silver-esim-sim/":
            constant_iphone14pro_white_128_price = product_price
        elif product_url == "https://indexiq.ru/product/apple-airpods-3-mpny3/":
            constant_airpods3_iphone_price = product_price
        elif product_url == "https://indexiq.ru/product/apple-iphone-14-pro-max-128gb-deep-purple-esim-sim//":
            constant_iphone14promax_deeppurple_128_price = product_price


def main():
    surf_the_product(url_14promax_128_purple_iphone)
    surf_the_product(url_airpods13)
    surf_the_product(url_14pro_128_white_iphone)


if __name__ == "__main__":

    counter = 1
    #   Обработчик
    telegram = get_notifier('telegram')
    #   Ссылки на товары
    url_14pro_128_white_iphone = "https://indexiq.ru/product/apple-iphone-14-pro-128gb-silver-esim-sim/"
    url_airpods13 = "https://indexiq.ru/product/apple-airpods-3-mpny3/"
    url_14promax_128_purple_iphone = "https://indexiq.ru/product/apple-iphone-14-pro-max-128gb-deep-purple-esim-sim//"

    #   Константы на цены
    constant_airpods3_iphone_price = int(12500)
    constant_iphone14pro_white_128_price = int(89990)
    constant_iphone14promax_deeppurple_128_price = int(100990)  # deep purple
    chat_ID1 = 1227493429
    print(f"✅ Начал выполнять работу в {datetime.datetime.now().replace(microsecond=0)}")
    start_time = time.time()
    telegram.notify(message=f"✅ Начал выполнение работы в {datetime.datetime.now().replace(microsecond=0)}",
                    token='5103076975:AAHkT_5T2CnyK0vWREMgFAqnXP22Vdm-w0U', chat_id=chat_ID1)
    while True:
        counter = counter + 1
        main()
        my_random_sleep = (random.randrange(600, 3600))
        print(f"Следующая проверка товаров через {my_random_sleep} секунд")
        sleep(my_random_sleep)  # Повторная отправка запросов с рандомной задержкой
