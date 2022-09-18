import logging.config

import allure
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from config import CONFIG

from logging_settings import logger_config

from locators import BASE_PAGE_LOCATORS

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


class BasePage:
    TIMEOUT = 3
    CURRENCY_DROPDOWN_STATE = "area-expanded"
    CURRENCY_SIGNS = {"USD": "$", "EUR": "€", "GBP": "£"}

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def open(self):
        with allure.step(f"Opening page: {self.url}"):
            self.browser.get(self.url)
            LOGGER.debug(f"Opened page: {self.url}")

    @allure.step("Searching: {locator}")
    def get_element_if_present(self, locator, only_first=False):
        """Returns element or elements list if found"""

        element_list = self.browser.find_elements(*locator)
        if only_first:
            LOGGER.debug(f"FOUND! Return only first element: '{locator}' ")
            return element_list[0]
        else:
            LOGGER.debug(f"FOUND! Return elements list: '{locator}' ")
            return element_list

    @allure.step("Clicking on: {element_or_locator}")
    def click(self, element_or_locator: tuple):
        if isinstance(element_or_locator, WebElement):
            element_or_locator.click()
        else:
            self.get_element_if_present(element_or_locator, only_first=True).click()
        LOGGER.debug(f"Clicked on: '{element_or_locator}' ")

    @allure.step("Writing text '{text}' into field '{locator}'")
    def fill_field(self, locator, text):
        self.wait_element(locator).send_keys(text)
        LOGGER.debug(f"Written text '{text}' into field '{locator}'")

    @allure.step("Clearing the field: {locator}")
    def clear_field(self, locator):
        self.wait_element(locator).clear()
        LOGGER.debug(f"Cleared the field: {locator}")

    @allure.step("Waiting element present: '{locator}' to be present for {timeout} seconds")
    def wait_element(self, locator, timeout=TIMEOUT):
        try:
            LOGGER.debug(f"Waiting element present: '{locator}' for {timeout} seconds")
            return WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            LOGGER.warning(f"Unable to find element: '{locator}'; waited for {timeout} seconds")
            return False

    @allure.step("Scrolling to: {element_or_locator}")
    def scroll_to_element(self, element_or_locator):
        try:
            if isinstance(element_or_locator, WebElement):
                self.browser.execute_script("arguments[0].scrollIntoView();", element_or_locator)
            else:
                self.browser.execute_script("arguments[0].scrollIntoView();",
                                            self.browser.find_element(*element_or_locator))
            LOGGER.debug(f"Scrolled, now element is visible: '{element_or_locator}'")
        except NoSuchElementException:
            LOGGER.warning(f"Tried to scroll to element, but didn`t find it: '{element_or_locator}' ")
            return False

    @allure.step("Waiting element NOT present: '{locator}' for {timeout} seconds")
    def wait_element_not_present(self, locator, timeout=TIMEOUT):
        try:
            LOGGER.debug(f"Waiting element NOT present: '{locator}' for {timeout} seconds")
            return WebDriverWait(self.browser, timeout).until_not(EC.visibility_of_element_located(locator))
        except TimeoutException:
            LOGGER.warning(f"Didn`t expect to find element: '{locator}'; waited for {timeout} seconds ")
            return False

    @allure.step("Waiting alert present for {timeout} seconds")
    def wait_element_clickable(self, locator, timeout=TIMEOUT):
        try:
            LOGGER.debug(f"Waiting element clickable: '{locator}' for {timeout} seconds")
            return WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            LOGGER.warning(f"Failed to find CLICKABLE element: '{locator}'; waited for {timeout} seconds")
            return False

    @allure.step("Waiting alert present for {timeout} seconds")
    def wait_alert(self, timeout=TIMEOUT):
        try:
            LOGGER.debug(f"Waiting alert present for {timeout} seconds")
            return WebDriverWait(self.browser, timeout).until(EC.alert_is_present())
        except:
            LOGGER.warning(f"Didn`t find any alert; waited for {timeout} seconds")
            return False

    @allure.step("Extracting text from element: '{element_or_locator}'")
    def get_element_text(self, element_or_locator):
        if isinstance(element_or_locator, WebElement):
            element_text = element_or_locator.text
        else:
            element_text = self.get_element_if_present(element_or_locator, only_first=True).text
        LOGGER.debug(f"Extracted text '{element_text}' from element: {element_or_locator}")
        return element_text

    @allure.step("Getting current tab`s name")
    def get_tab_name(self):
        LOGGER.debug(f"Current tab name is '{self.browser.title}'")
        return self.browser.title

    @allure.step("Getting current currency")
    def get_current_currency(self):
        current_currency = self.get_element_text(BASE_PAGE_LOCATORS["currency"]["current"])
        LOGGER.debug(f"Current currency is '{current_currency}'")
        return current_currency

    def is_currency_dropdown_opened(self):
        currency_dropdown = self.get_element_if_present(BASE_PAGE_LOCATORS["currency"]["dropdown"],
                                                        only_first=True)
        currency_dropdown_state = currency_dropdown.get_attribute(self.CURRENCY_DROPDOWN_STATE)
        LOGGER.debug(f"Currency dropdown is {'' if currency_dropdown_state else 'NOT'} opened")
        return currency_dropdown_state

    @allure.step("Changing currency to '{currency}'")
    def change_currency_to(self, currency):
        if not self.is_currency_dropdown_opened():
            self.click(BASE_PAGE_LOCATORS["currency"]["dropdown"])
        self.click(BASE_PAGE_LOCATORS["currency"][currency.upper()])
        LOGGER.debug(f"Changed currency to '{currency}'")

    @allure.step("Getting cart total items and total price")
    def get_cart_item_count_and_total_price(self):
        cart_text = self.get_element_text(BASE_PAGE_LOCATORS["cart button"]).replace(",", "").strip()
        LOGGER.debug(f"Cart has {cart_text} in total ")
        cart_text_split = cart_text.split(" item(s) - $")
        items_in_cart, total_price = int(cart_text_split[0]), float(cart_text_split[1])
        return items_in_cart, total_price

    @allure.step("Verify link presence")
    def _verify_link_presence(self, link_text):
        try:
            return WebDriverWait(self.browser, self.browser.t) \
                .until(EC.visibility_of_element_located((By.LINK_TEXT, link_text)))
        except TimeoutException:
            raise AssertionError("Cant find element by link text: {}".format(link_text))
        LOGGER.debug(f"Verify presence link: '{link_text}' ")

    @allure.step("Verify element presence")
    def _verify_element_presence(self, locator: tuple):
        try:
            return WebDriverWait(self.browser, self.browser.t).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise AssertionError("Cant find element by locator: {}".format(locator))

    @allure.step
    def _element(self, locator: tuple):
        return self._verify_element_presence(locator)

    @allure.step
    def _click_element(self, element):
        ActionChains(self.browser).pause(0.3).move_to_element(element).click().perform()

    @allure.step
    def _simple_click_element(self, element):
        element.click()

        # element = self._element(locator)
        # ActionChains(self.browser).pause(0.3).move_to_element(element).click().perform()

    @allure.step("Clicking in element")
    def _click_in_element(self, element, locator: tuple, index: int = 0):
        element = element.find_elements(*locator)[index]
        self._click_element(element)
        LOGGER.debug(f"Clicked in element: '{element}'")

    @allure.step("Clicking on link")
    def click_link(self, link_text):
        self.click((By.LINK_TEXT, link_text))
        LOGGER.debug(f"Clicked on link: '{link_text}'")
        return self

    @allure.step("Check base elements: top, logo, search, cart, menu, category")
    def check_base_elements(self):
        wait = WebDriverWait(self.browser, 10, poll_frequency=1)
        wait.until(EC.visibility_of_element_located((By.ID, "top")))
        wait.until(EC.presence_of_element_located((By.ID, "logo")))
        wait.until(EC.presence_of_element_located((By.ID, "search")))
        wait.until(EC.presence_of_element_located((By.ID, "cart")))
        wait.until(EC.presence_of_element_located((By.ID, "menu")))
        el = wait.until(EC.visibility_of_element_located((By.ID, "category")))
        wait.until(EC.text_to_be_present_in_element((By.ID, "category"), "Categories"))
        assert el.text == CONFIG["category"]

    @allure.step
    def check_page_title(self, page):
        self.browser.get(CONFIG[page]["url"])
        wait = WebDriverWait(self.browser, 10, poll_frequency=1)
        wait.until(EC.title_is(CONFIG[page]["title"]))
