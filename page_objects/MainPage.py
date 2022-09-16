import allure
from selenium.webdriver.common.by import By
from .BasePage import BasePage

import logging.config
from logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")

from locators import MAIN_PAGE_LOCATORS


class MainPage(BasePage):
    FEATURE_PRODUCT = (By.CSS_SELECTOR, "#content > div.row .product-layout")
    FEATURE_PRODUCT_NAME = (By.CSS_SELECTOR, ".caption h4 a")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @allure.step("Adding #{index} 'featured product' to cart (by index, in order from left to right)")
    def add_to_cart(self, index=1):
        """Add n-th featured product to cart"""
        add_to_cart_button = self.get_element_if_present(locator=MAIN_PAGE_LOCATORS["featured: add to cart buttons"])
        self.click(add_to_cart_button[index - 1])
        LOGGER.debug(f"Added #{index} 'featured product' to cart (by index, in order from left to right)")

    @allure.step
    def click_featured_product(self, number):
        index = number - 1
        feature_product = self.browser.find_elements(*self.FEATURE_PRODUCT)[index]
        product_name = feature_product.find_element(*self.FEATURE_PRODUCT_NAME).text
        feature_product.click()
        return product_name
