import allure
from selenium.webdriver.common.by import By

from .BasePage import BasePage

import logging.config
from logging_settings import logger_config

from locators import CATALOG_PAGE_LOCATORS

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


class CatalogPage(BasePage):
    CONTENT = (By.CSS_SELECTOR, "#content")
    ADD_TO_CART = (By.CSS_SELECTOR, "input[value='Add to Cart']")
    NO_PRODUCTS_MESSAGE = "There are no products to list in this category."

    def __init__(self, catalog_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url += catalog_id

    @allure.step("")
    def add_to_cart(self, index=1):
        LOGGER.debug(f"Adding #{index} product to cart (by index in order from left to right)")
        add_to_cart_button = self.get_element_if_present(locator=CATALOG_PAGE_LOCATORS["add to cart buttons"])
        self.click(add_to_cart_button[index - 1])
        LOGGER.debug(f"Added #{index} product to cart")

    @allure.step
    def verify_product_link(self, product_name):
        self._verify_link_presence(product_name)
        return self
