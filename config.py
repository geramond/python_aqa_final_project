import random
from selenium.webdriver.common.by import By

CONFIG = {
    "main":
        {"url": "http://localhost:8081/",
         "title": "Your Store"},
    "desktops":
        {"url": "http://localhost:8081/desktops",
         "title": "Desktops"},
    "mac":
        {"url": "http://localhost:8081/desktops/mac/imac",
         "title": "iMac"},
    "admin":
        {"url": "http://localhost:8081/admin/",
         "title": "Administration"
         },
    "register":
        {"url": "http://localhost:8081/index.php?route=account/register",
         "title": "Register Account"
         },
    "category": "Categories"
}

TIMEOUT = 3
CURRENCY_DROPDOWN_STATE = "area-expanded"
CURRENCY_SIGNS = {"USD": "$", "EUR": "€", "GBP": "£"}


def random_int(): return random.randint(1, 30000)
