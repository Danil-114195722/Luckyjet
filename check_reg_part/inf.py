import requests
import json
import calendar
import time

sess = requests.Session()
sess.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})

class login():
    data_log = {"disableCaptcha": "true",
        "login": "cryptastavka@mail.ru",
        "password": "Passot1kkkbaksov"
    }



class checkreg():
    link_data = {"sources": None,
                "country": None,
                "hash_id": 574581,
                "sub1": 1221
    }



def infcheck(id):
    
    res = sess.post("https://1win-partner.com/api/v2/user/login", json = login.data_log)
    while True:
        checkreg.link_data["sub1"] = id
        res = sess.get(f"https://1win-partner.com/api/v2/stats_v2/all?sources=&country=&hash_id=574581&sub1={id}", json = checkreg.link_data)
        res = json.loads(res.text)
        reg = res["values"]["regs"]   # Регестрация 
        vis = res["values"]["visits"] # Посещение
        time.sleep(2)
        if vis == 1:
            return True
        if vis == 1:
            break
    
