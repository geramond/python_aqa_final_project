import logging.config
import allure
from faker import Faker
from selenium.webdriver.common.by import By

from ..BasePage import BasePage
from logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")

from page_objects.locators import ADD_PRODUCT_PAGE_LOCATORS



class AddProductForm(BasePage):
    INPUT_PRODUCT_NAME = (By.CSS_SELECTOR, "#input-name1")
    INPUT_META_TAG_TITLE = (By.CSS_SELECTOR, "#input-meta-title1")
    INPUT_MODEL = (By.CSS_SELECTOR, "#input-model")
    SAVE_BUTTON = (By.CLASS_NAME, "fa fa-save")

    ADD_NEW_URL_APPENDIX_PART = "admin/index.php?route=catalog/product/add"
    PAGE_TITLE = "Add Product"
    CREATE_NEW_PRODUCT_ERROR_TEXT = " Warning: Please check the form carefully for errors!"

    @allure.step("Switching to section '{name}' in 'Add new product' page configuration")
    def switch_to_tab(self, name):
        self.scroll_to_element(ADD_PRODUCT_PAGE_LOCATORS["tab"][name])
        self.click(ADD_PRODUCT_PAGE_LOCATORS["tab"][name])
        LOGGER.debug(f"Switched to '{name}'")

    @allure.step("Creating product: name='{name}', model='{model}', meta='{meta}'")
    def create_product(self, name=None, model=None, meta=None):
        if name is None:
            f = Faker()
            name = "1" + f.aba()[:3] + f.user_name()
        if model is None:
            model = name + " 6000"
        if meta is None:
            meta = "apple"

        LOGGER.debug(f"Creating product: name='{name}', model='{model}', meta='{meta}'")
        self.fill_field(ADD_PRODUCT_PAGE_LOCATORS["general"]["name"], name)
        self.fill_field(ADD_PRODUCT_PAGE_LOCATORS["general"]["meta"], meta)
        self.switch_to_tab("data")
        self.fill_field(ADD_PRODUCT_PAGE_LOCATORS["data"]["model"], model)

        self.click(ADD_PRODUCT_PAGE_LOCATORS["save"])
        LOGGER.debug(f"Created product")

        created_product = {"name": name, "model": model, "meta": meta}
        return created_product

    def fill_form_general(self, product_name, product_meta_tag_title):
        self._element(self.INPUT_PRODUCT_NAME).send_keys(product_name)
        self._element(self.INPUT_META_TAG_TITLE).send_keys(product_meta_tag_title)

    def fill_form_data(self, product_model):
        self._element(self.INPUT_MODEL).send_keys(product_model)

    def save_data(self):
        self._element(self.SAVE_BUTTON).click()
