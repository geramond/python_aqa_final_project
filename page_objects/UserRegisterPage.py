import allure

from .BasePage import BasePage

import logging.config
from logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")

from locators import ADD_PRODUCT_PAGE_LOCATORS
from config import random_int

EXAMPLE_USER = {
    "first_name": "Alex" + str(random_int()), "last_name": "Bell" + str(random_int()),
    "email": "alex.bell" + str(random_int()) + "@example.com",
    "telephone": "+123456789", "password": "password", "password_confirm": "password"
}


class UserRegisterPage(BasePage):
    SUCCESS_REGISTRATION_URL_APPENDIX = "index.php?route=account/success"
    LOGIN_URL_APPENDIX = "index.php?route=account/login"
    ERROR_TEXT_POLICY = "Warning: You must agree to the Privacy Policy!"

    def __init__(self, browser, url):
        super().__init__(browser, url)
        self.url += "index.php?route=account/register"

    @allure.step(
        "Filling register page fields with credentials: first_name: '{first_name}', last_name: '{last_name}', email: '{email}', password: '{password}'")
    def fill_field_register_page(self, first_name=None, last_name=None, email=None, phone=None, password=None,
                                 password_confirm=None):
        if first_name:
            super().fill_field(ADD_PRODUCT_PAGE_LOCATORS["first name"], first_name)
        if last_name:
            super().fill_field(ADD_PRODUCT_PAGE_LOCATORS["last name"], last_name)
        if email:
            super().fill_field(ADD_PRODUCT_PAGE_LOCATORS["email"], email)
        if phone:
            super().fill_field(ADD_PRODUCT_PAGE_LOCATORS["phone"], phone)
        if password:
            super().fill_field(ADD_PRODUCT_PAGE_LOCATORS["password"], password)
        if password_confirm:
            super().fill_field(ADD_PRODUCT_PAGE_LOCATORS["password_confirm"], password_confirm)

    def generate_user(self):
        f = Faker()
        password = f.password()
        generated_user = {
            "first_name": f.first_name(), "last_name": f.last_name(), "email": f.email(),
            "telephone": f.phone_number(), "password": password, "password_confirm": password
        }
        LOGGER.debug(f"Generated user with data: {generated_user}")
        return generated_user
