import os

from MySQLdb import connect, cursors, Error


MYSQLCONF = {
    'host': 'localhost',  # хост базы данных
    'user': '123',  # имя пользователя базы данных
    'password': '123',  # пароль пользователя базы данных
    'db': '123',  # имя базы данных
    'charset': 'utf8',  # используемая кодировка базы данных
    'autocommit': True,  # автоматический cursor.commit()
    # извлекаемые строки из БД принимают вид словаря
    'cursorclass': cursors.DictCursor
}


def write_change_price(product_id, old_price, new_price):
    db = connect(**MYSQLCONF)
    cursor = db.cursor()
    cursor.execute(
        f"INSERT INTO `all_changes_price` (`id`, `product_id`, `old_price`, `new_price`, `date`) VALUES (NULL, '{product_id}', '{old_price}', '{new_price}', CURRENT_TIMESTAMP)")
    db.close()


def output_product_change(product_id):
    db = connect(**MYSQLCONF)
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM `all_changes_price` WHERE `product_id` = {product_id}')
    result = cursor.fetchall()
    return result

def output_all_product_in_db():
    db = connect(**MYSQLCONF)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM `all_changes_price`')
    result = cursor.fetchall()
    return result

def max_price_from_db(product_id):
    db = connect(**MYSQLCONF)
    cursor = db.cursor()
    cursor.execute(f'SELECT MAX(old_price) FROM all_changes_price WHERE product_id = {product_id}')
    result = cursor.fetchall()
    return result[0]['MAX(old_price)']
#   print(max_price_from_db(7))
def min_price_from_db(product_id):
    db = connect(**MYSQLCONF)
    cursor = db.cursor()
    cursor.execute(f'SELECT MIN(old_price) FROM all_changes_price WHERE product_id = {product_id} AND old_price > 1000')
    result = cursor.fetchall()
    return result[0]['MIN(old_price)']
#   print(min_price_from_db(2))


def last_product_price(product_id):
    db = connect(**MYSQLCONF)
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM `all_changes_price` WHERE `product_id` = {product_id} ORDER BY id DESC LIMIT 1')
    result = cursor.fetchall()
    return result[0]['new_price']
#   print(last_product_price(2))


def add_empty_object_with_unical_product_id(product_id):
    db = connect(**MYSQLCONF)
    cursor = db.cursor()
    cursor.execute(f'INSERT INTO `all_changes_price` (`id`, `product_id`, `old_price`, `new_price`, `date`, `max_price`, `min_price`) VALUES (NULL, {product_id}, 0, 0, NOW(), NULL, NULL)')
