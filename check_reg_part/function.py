import requests
import json
import calendar
import time



# Json для авторизации на сайте пп

class login():
    data_log = {"disableCaptcha": "true",
        "login": "cryptastavka@mail.ru",
        "password": "Passot1kkkbaksov"
    }




# Заготовка json для запроса данных о регистрации

class checkreg():
    link_data = {"sources": None,
                "country": None,
                "hash_id": 574581,
                "sub1": 1221
    }



sess = requests.Session()
sess.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})


# Пример ответа от сервера

"""data = {'error': False, 'values': {'date': None, 'payment_sum': 0, 'deposits_amount': 0, 'deposits_sum': 0, 'payments_amount': 0, 'regs': 0, 'visits': 1, 'new_deposit': 0, 'poker_rake': 0, 'poker_rake_profit': 0, 'bets_amount': 0, 'profit_bets_sum': 0, 'loss_bets_sum': 0, 'profit_casino_sum': 0, 'loss_casino_sum': 0, 'profit_case_sum': 0, 'loss_case_sum': 0, 'difference': 0, 'epc': 0, 'withdrawal_sum': 0, 'profit_total_sum': 
0, 'loss_total_sum': 0}}"""



# Авторизация на сайте ПП

def logfun():
    res = sess.post("https://1win-partner.com/api/v2/user/login", json = login.data_log)


# Главная функция. Проверка регистрации

def check(id):
    # Коректировка json для получение данных о регистрации
    checkreg.link_data["sub1"] = id
    res = sess.get(f"https://1win-partner.com/api/v2/stats_v2/all?sources=&country=&hash_id=574581&sub1={id}", json = checkreg.link_data)
    res = json.loads(res.text)
    reg = res["values"]["regs"]   # Регестрация 
    vis = res["values"]["visits"] # Посещение
    return int(reg)


