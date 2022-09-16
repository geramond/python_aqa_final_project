import time
import pytest
import logging.config

from page_objects import MainPage

from logging_settings import logger_config

from page_objects.locators import BASE_PAGE_LOCATORS
from page_objects.locators import MAIN_PAGE_LOCATORS
from page_objects.locators import PRODUCT_PAGE_LOCATORS

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


def test_logo_on_main_page_exists(browser, base_url):
    """Check OpenCart logo on 'Main page'"""

    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    LOGGER.debug(f"ASSERT: opencart logo on main page")
    assert main_page.wait_element(BASE_PAGE_LOCATORS["logo"]), f"Unable to find opencart logo on main page"


def test_usd_is_default_currency(browser, base_url):
    """Check USD($) is default currency"""

    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    current_currency = main_page.get_currenct_currency()
    LOGGER.debug(f"ASSERT: USD($) is default currency")
    assert current_currency == main_page.CURRENCY_SIGNS[
        "USD"], f"Expected 'USD'($) is default currency, but got {current_currency}"


@pytest.mark.parametrize("currency", ["USD", "EUR", "GBP"])
def test_change_currency(browser, base_url, currency):
    """Check currency can be changed"""

    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.change_currency_to(currency=currency)
    current_currency = main_page.get_currenct_currency()
    LOGGER.debug(f"ASSERT: currency changed to '{main_page.CURRENCY_SIGNS[currency.upper()]}'")
    assert current_currency == main_page.CURRENCY_SIGNS[
        currency.upper()], f"Expected currency '{main_page.CURRENCY_SIGNS[currency.upper()]}' but got '{current_currency'"


@pytest.mark.smoke
def test_nav_bar_on_main_page_exists(browser, base_url):
    """Check navigation bar on Main page"""

    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    LOGGER.debug(f"ASSERT: there is navigation bar on Main page")
    assert main_page.wait_element(BASE_PAGE_LOCATORS["navbar"]), f"Unable to find navigation bar on the Main page"


def test_nav_bar_items_clickable(browser, base_url):
    """Check navigation bar items are clickable"""

    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    nav_bar_items = main_page.get_element_if_present(BASE_PAGE_LOCATORS["navbar items"])
    LOGGER.debug(f"ASSERT: navigation bar items are clickable")
    for item in nav_bar_items:
        assert main_page.wait_element_clickable(item)


def test_cart_is_empty_on_first_launch(browser, base_url):
    """Check cart is empty when user opens Opencart for the first time"""

    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    items_in_cart, total_price = main_page.get_cart_item_count_and_total_price()
    LOGGER.debug(f"ASSERT: cart is empty when user opens Opencart for the first time")
    assert items_in_cart == 0 and total_price == 0, \
        f"Should not be items in cart, but got {items_in_cart} items, total price is {total_price}"


@pytest.mark.parametrize("product_index",
                         [pytest.param(1, marks=pytest.mark.smoke),
                          2, 3])
def test_success_message_after_add_featured_product_to_cart_and_increase_cart_total(browser, base_url,
                                                                                    product_index):
    """Check:
        - after adding product to cart, 'total items' == 1, 'cart price' > 0.
        - if product has NO required fields, it can be added to cart from 'Main page' immediately
        - if product has required fields, user redirected to product page
        """

    main_page = MainPage(browser=browser, base_url=base_url)
    main_page.open()
    main_page.scroll_to_element(BASE_PAGE_LOCATORS["featured: add to cart buttons"])
    main_page.add_to_cart(product_index)
    time.sleep(1)  # url can be changed, we`re waiting for it
    if browser.current_url != main_page.url:

        # if product has required fields it can`t be added from Main - redirect to product page.
        # Check product has at least 1 required field
        LOGGER.debug("User is redirected to product page. Seems this product has required fields...")
        main_page.scroll_to_element(PRODUCT_PAGE_LOCATORS["add to cart required fields"])
        LOGGER.debug(f"ASSERT: product '{browser.current_url}' has at least 1 required field")
        assert main_page.get_element_if_present(PRODUCT_PAGE_LOCATORS["add to cart required fields"],
                                                only_first=True), \
            f"Product '{browser.current_url}' doesn`t have any required field.\
            It should have been added to cart from main page (but wasn`t)"
    else:

        # other products can be added from Main page, should be success message
        main_page.wait_element(MAIN_PAGE_LOCATORS["alert"])
        success_message = main_page.get_element_if_present(MAIN_PAGE_LOCATORS["alert"], only_first=True)
        success_message_text = main_page.get_element_text(success_message)
        LOGGER.debug(f"ASSERT: there is success message")
        assert "Success: You have added" and " to your shopping cart!" in success_message_text, \
            f"Expected success message to be 'Success: You have added ... to your shopping cart!', but got {success_message_text}"
        items_in_cart, total_price = main_page.get_cart_item_count_and_total_price()
        LOGGER.debug(f"ASSERT: should be 1 item in cart")
        assert items_in_cart == 1 and total_price != 0, f"Should be 1 item in cart, but got {items_in_cart} items, total price is ${total_price}"
