import requests
from bs4 import BeautifulSoup
import lxml
import fake_useragent
import datetime
from time import sleep
import random
from notifiers import get_notifier
import asyncio
import time

constant_purple_iphone_price = int(90490)  # 90990
constant_white_iphone_price = int(89990)
constant_iphone14promax_price = int(98990)
chat_ID1 = 1227493429


async def send_message_to_tg(brand_name, constant_white_iphone_price, new_product_price):
    telegram = get_notifier('telegram')
    messages = f"Цена на{brand_name} изменилась. \n Прошлая цена: {constant_white_iphone_price} \n Новая цена: {new_product_price}"
    telegram.notify(message=messages, token='5103076975:AAHkT_5T2CnyK0vWREMgFAqnXP22Vdm-w0U', chat_id=chat_ID1)


async def surf_the_14promax_iphone():
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    url_white_iphone = "https://indexiq.ru/product/apple-iphone-14pro-max-128gb-silver/"
    responce = requests.get(url_white_iphone, headers=header).text
    soup = BeautifulSoup(responce, "lxml")
    brand_name = soup.find("h1", itemprop="name").text.replace("Смартфон", "")
    link_to_product = soup.find("link", itemprop="url").get("href")
    old_product_price = soup.find("span", itemprop="price").text.replace(".", "")
    new_product_price = soup.find("span", itemprop="price").text.replace(".", "")
    product_price = int(old_product_price[0:len(old_product_price) - 2])
    # print(product_price)
    if int(product_price) == constant_iphone14promax_price:
        # my_random_sleep = (random.randrange(800, 3600))
        # print(f"Следующая проверка магазина через {my_random_sleep} секунд")
        # sleep(my_random_sleep)  # Повторная отправка запросов с рандомной задержкой от 60 до 120 секунд.
        print(f"Последняя дата проверки: {datetime.datetime.now().replace(microsecond=0)}")
        print(f"Товар: {brand_name})\n"
              f"Цена: {product_price}")
    if int(product_price) != int(constant_iphone14promax_price):
        # print(f"product_price = {product_price} \n constant_white_iphone_price = {constant_iphone13promax_price}")
        print(
            f"---------------------------------------\n"
            f"Цена на{brand_name} изменилась. \n Прошлая цена: {constant_iphone14promax_price} \n Новая цена: {product_price}\n"
            f"---------------------------------------")
        # Отправляем уведомление в телеграм
        await send_message_to_tg(brand_name, constant_iphone14promax_price, product_price)


async def surf_the_purple_iphone():
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    url_white_iphone = "https://indexiq.ru/product/apple-iphone-14-pro-128gb-deep-purple-esim-sim/"
    responce = requests.get(url_white_iphone, headers=header).text
    soup = BeautifulSoup(responce, "lxml")
    brand_name = soup.find("h1", itemprop="name").text.replace("Смартфон", "")
    link_to_product = soup.find("link", itemprop="url").get("href")
    old_product_price = soup.find("span", itemprop="price").text.replace(".", "")
    new_product_price = soup.find("span", itemprop="price").text.replace(".", "")
    product_price = int(old_product_price[0:len(old_product_price) - 2])
    # print(product_price)
    if int(product_price) == constant_purple_iphone_price:
        # my_random_sleep = (random.randrange(800, 3600))
        # print(f"Следующая проверка магазина через {my_random_sleep} секунд")
        # sleep(my_random_sleep)  # Повторная отправка запросов с рандомной задержкой от 60 до 120 секунд.
        print(f"Последняя дата проверки: {datetime.datetime.now().replace(microsecond=0)}")
        print(f"Товар: {brand_name})\n"
              f"Цена: {product_price}")
    if int(product_price) != int(constant_purple_iphone_price):
        # print(f"product_price = {product_price} \n constant_white_iphone_price = {constant_purple_iphone_price}")
        print(
            f"---------------------------------------\n"
            f"Цена на{brand_name} изменилась. \n Прошлая цена: {constant_iphone14promax_price} \n Новая цена: {product_price}\n"
            f"---------------------------------------")
        # Отправляем уведомление в телеграм
        await send_message_to_tg(brand_name, constant_purple_iphone_price, product_price)


async def surf_the_white_iphone():
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    url_white_iphone = "https://indexiq.ru/product/apple-iphone-14-pro-128gb-silver-esim-sim/"
    responce = requests.get(url_white_iphone, headers=header).text
    soup = BeautifulSoup(responce, "lxml")
    brand_name = soup.find("h1", itemprop="name").text.replace("Смартфон", "")
    link_to_product = soup.find("link", itemprop="url").get("href")
    old_product_price = soup.find("span", itemprop="price").text.replace(".", "")
    new_product_price = soup.find("span", itemprop="price").text.replace(".", "")
    product_price = int(old_product_price[0:len(old_product_price) - 2])
    # print(product_price)
    if int(product_price) == constant_white_iphone_price:
        print(f"Последняя дата проверки: {datetime.datetime.now().replace(microsecond=0)}")
        print(f"Товар: {brand_name})\n"
              f"Цена: {product_price}")
    if int(product_price) != int(constant_white_iphone_price):
        print(
            f"---------------------------------------\n"
            f"Цена на{brand_name} изменилась. \n Прошлая цена: {constant_iphone14promax_price} \n Новая цена: {product_price}\n"
            f"---------------------------------------")
        # Отправляем уведомление в телеграм
        await send_message_to_tg(brand_name, constant_white_iphone_price, product_price)


async def main():
    task1 = asyncio.create_task(surf_the_purple_iphone())
    task2 = asyncio.create_task(surf_the_white_iphone())
    task3 = asyncio.create_task(surf_the_14promax_iphone())

    await task1
    await task2
    await task3


if __name__ == "__main__":
    print(f"Начал выполнение работы в {datetime.datetime.now().replace(microsecond=0)}")
    while True:
        asyncio.run(main())
        my_random_sleep = (random.randrange(800, 3600))
        print(f"Следующая проверка товаров через {my_random_sleep} секунд")
        sleep(my_random_sleep)  # Повторная отправка запросов с рандомной задержкой
