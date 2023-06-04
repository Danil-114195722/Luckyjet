from sqlite3 import Connection, Error
from datetime import datetime

from data.constants import CONNECTION


# выполнить SQL-команду без возврата значений
def exec_without_resp(con: Connection, query):
    cur = con.cursor()
    result = None
    all_right = False

    try:
        result = cur.execute(query)
        con.commit()
        all_right = True

    except Error as error:
        print(f'Ha-ha-ha, you caught the error in project "Luckyjet", in file "db_connection", in func "execute_query": {str(error)}')

    return result, all_right


# выполнить SQL-команду с возвратом значений
def exec_with_resp(con: Connection, query):
    cur = con.cursor()
    result = None
    all_right = False

    try:
        cur.execute(query)
        result = cur.fetchall()
        all_right = True

    except Error as error:
        print(f'Ha-ha-ha, you caught the error in project "Luckyjet", in file "db_connection", in func "execute_query": {str(error)}')

    return result, all_right


# создать таблицу "user"
def create_table_user():
    # id - уникальный id в таблице
    # tg_id - уникальный id юзера в тг
    # reg - True/False (зареган или нет)
    # rate - выбранный тариф (0 - бесплатно, 1 - на месяц, 3 - бессрочно)
    # rate_date - дата оплаты тарифа (выбора тарифа)
    # start_date - дата добавления юзера в БД (первое сообщение /start в бота от юзера)

    create_query = '''CREATE TABLE IF NOT EXISTS user (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    tg_id INT NOT NULL UNIQUE,
    reg bool NOT NULL,
    rate INT NULL,
    rate_date DATETIME NULL DEFAULT NULL,
    start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );'''
    # выполняем создание таблицы
    exec_without_resp(CONNECTION, create_query)


# выбрать все данные о пользователе по его id в телеграме
def select_user(tg_id: int):
    select_query = f'SELECT * FROM user WHERE tg_id={tg_id};'
    try:
        return exec_with_resp(CONNECTION, select_query)[0][0]
    # если юзер не был найден
    except IndexError:
        return tuple()


# добавить нового пользователя в БД
def add_user(tg_id: int, reg: int):
    insert_query = f'INSERT INTO user (tg_id, reg) VALUES ({tg_id}, {reg});'
    exec_without_resp(CONNECTION, insert_query)


# зарегистрировать пользователя
def make_reg(tg_id: int):
    update_query = f'UPDATE user SET reg = 1 WHERE tg_id = {tg_id};'
    exec_without_resp(CONNECTION, update_query)


# добавить тариф пользователю
def make_rate(tg_id: int, rate: int = 0):
    update_query = f'UPDATE user SET rate = {rate} WHERE tg_id = {tg_id};'
    update_query = f'UPDATE user SET rate_date = CURRENT_TIMESTAMP WHERE tg_id = {tg_id};'
    exec_without_resp(CONNECTION, update_query)


# удалить тариф у пользователя
def del_rate(tg_id: int):
    update_query = f'UPDATE user SET rate = NULL WHERE tg_id = {tg_id};'
    exec_without_resp(CONNECTION, update_query)


if __name__ == '__main__':
    # add_user(tg_id=1234567, reg=False)
    # print(select_user(tg_id=1234567))
    # make_reg(tg_id=1601245210)
    # del_rate(tg_id=1234567)
    pass
