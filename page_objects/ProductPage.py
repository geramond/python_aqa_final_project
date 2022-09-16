import allure
import time

from selenium.webdriver.common.by import By
from .BasePage import BasePage

import logging.config
from logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")

from locators import PRODUCT_PAGE_LOCATORS


class ProductPage(BasePage):
    WISH_LIST_BUTTON = (By.CSS_SELECTOR, "[data-original-title='Add to Wish List']")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "#button-cart")
    ADD_TO_COMPARISON = (By.CSS_SELECTOR, "[data-original-title='Compare this Product']")

    def __init__(self, product_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url += product_id

    @allure.step
    def get_product_price(self, currency="$"):
        if currency == "$":
            product_price = float(self.get_element_text(PRODUCT_PAGE_LOCATORS["product price"])[1:])
            LOGGER.debug(f"Found that the price of the product is ${product_price}")
            return product_price

    @allure.step
    def add_to_wish_list(self):
        self.click(self.WISH_LIST_BUTTON)

    @allure.step
    def add_to_cart(self):
        time.sleep(1)  # Page loading problem
        self.click(self.ADD_TO_CART_BUTTON)

    @allure.step
    def add_to_comparison(self):
        self.click(self.ADD_TO_COMPARISON)
