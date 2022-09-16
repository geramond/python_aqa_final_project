import allure
from selenium.webdriver.common.by import By

from .BasePage import BasePage

import logging.config
from logging_settings import logger_config

from locators import ADMIN_PAGE_LOCATORS

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


class AdminLoginPage(BasePage):
    LOGGED_IN_URL_APPENDIX_PART = "admin/index.php?route=common/dashboard"
    FORGOTTEN_PASSWORD_URL_APPENDIX = "admin/index.php?route=common/forgotten"
    PAGE_TITLE = "Please enter your login details."
    NO_SUCH_USER_ERROR = "No match for Username and/or Password."

    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)
        self.url += "admin"

    def fill_field_login_page(self, username=None, password=None):
        if username:
            super().fill_field(ADMIN_PAGE_LOCATORS["username"], username)
        if password:
            super().fill_field(ADMIN_PAGE_LOCATORS["password"], password)


class AdminDashboardPage(BasePage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @allure.step("Go from 'Dashboard' to 'Products'")
    def go_to_products(self):
        LOGGER.debug("Going from 'Dashboard' to 'Products'")
        open_catalog_button = self.wait_element(ADMIN_PAGE_LOCATORS["open catalog"])
        open_catalog_button.click()
        open_product_button = self.wait_element(ADMIN_PAGE_LOCATORS["catalog: products"])
        open_product_button.click()


class AdminProductsPage(BasePage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url += "/admin/index.php?route=catalog/product"

    @allure.step("Clicking on 'Add new product'")
    def click_add_new_product(self):
        self.click(ADMIN_PAGE_LOCATORS["add new"])
        LOGGER.debug("Clicked on 'Add new product'")

    @allure.step("Finding product with name: '{name}'")
    def get_product_by_name(self, name):
        self.scroll_to_element((By.XPATH, "//*[contains(text(), '{0}')]".format(name)))
        product = self.get_element_if_present((By.XPATH, "//*[contains(text(), '{0}')]".format(name)))
        LOGGER.debug("Product with name: '{name}' has been found")
        return product

    @allure.step("Filtering products list by: product name='{name}' and/or model='{model}'")
    def filter_products_by(self, name=None, model=None):
        if name:
            self.clear_field(ADMIN_PAGE_LOCATORS["filter: name"])
            self.fill_field(ADMIN_PAGE_LOCATORS["filter: name"], name)
            LOGGER.debug(f"Filtered products list by product name='{name}'")
        if model:
            self.clear_field(ADMIN_PAGE_LOCATORS["filter: model"])
            self.fill_field(ADMIN_PAGE_LOCATORS["filter: model"], model)
            LOGGER.debug(f"Filtered products list by product model='{model}'")
        self.click(ADMIN_PAGE_LOCATORS["filter"])
        return self

    @allure.step("Counting products in list on 'Products page'")
    def get_products_amount_on_page(self):
        products = self.get_element_if_present(ADMIN_PAGE_LOCATORS["products on page"])
        products_count = len(products) - 1
        LOGGER.debug(f"Found {products_count} products in list")
        return products_count

    @allure.step("Filtering products by '{name}' and '{model}' and select it")
    def filter_and_select_exact_product(self, name=None, model=None):
        self.filter_products_by(name=name, model=model)
        assert self.get_products_amount_on_page() == 1
        select_all_checkbox = self.get_element_if_present(ADMIN_PAGE_LOCATORS["products on page"], only_first=True)
        self.click(select_all_checkbox)
        LOGGER.debug(f"Checked that only ONE product left after filtering and then selected it")

    @allure.step("Deleting selected product")
    def delete_selected_products(self):
        self.click(ADMIN_PAGE_LOCATORS["delete"])
        delete_alert = self.browser.switch_to.alert
        delete_alert.accept()
        LOGGER.debug("Deleted selected product")
