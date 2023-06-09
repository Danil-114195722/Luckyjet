import sqlite3
from pathlib import Path
from datetime import timedelta


# путь до папки с проектом
PROJECT_PATH = Path(__file__).resolve().parent.parent
# print(PROJECT_PATH)

DATABASE = f'{PROJECT_PATH}/sqlite3.db'
CONNECTION = sqlite3.connect(DATABASE)

# оплаченное время
free_time = timedelta(weeks=1)
month_time = timedelta(days=30)

# пуши без регистрации
push_not_reg_30min = timedelta(minutes=30)
push_not_reg_4hours = timedelta(hours=4)
push_not_reg_12hours = timedelta(hours=12)
push_not_reg_1day = timedelta(days=1)
push_not_reg_3days = timedelta(days=3)

# tests
# push_not_reg_30min = timedelta(minutes=3)
# push_not_reg_4hours = timedelta(minutes=5)
# push_not_reg_12hours = timedelta(minutes=8)

# пуши без оплаты депозита
push_not_pay_1hour = timedelta(hours=1)
push_not_pay_3hours = timedelta(hours=3)
push_not_pay_12hours = timedelta(hours=12)
push_not_pay_1day = timedelta(days=1)

# tests
# push_not_pay_1hour = timedelta(minutes=2)
# push_not_pay_3hours = timedelta(minutes=4)
# push_not_pay_12hours = timedelta(minutes=7)
