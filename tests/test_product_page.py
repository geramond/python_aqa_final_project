import pytest
import logging.config

from page_objects import ProductPage
from logging_settings import logger_config

from page_objects.locators import PRODUCT_PAGE_LOCATORS

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")

PRODUCT_IDS = [
    pytest.param("iphone", marks=pytest.mark.smoke),
    "iMac", "Canon", "Samsung", "test", "Nikon"
]
XFAIL_PRODUCT_IDS = [
    pytest.param("test", marks=pytest.mark.xfail(strict=True)),
    pytest.param("Canon", marks=pytest.mark.xfail(strict=True))
]


@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_product_name_is_not_empty(browser, base_url, product_id):
    """Check product name is not empty"""

    product_page = ProductPage(browser=browser, base_url=base_url, product_id=product_id)
    product_page.open()
    product_name = product_page.get_element_text(PRODUCT_PAGE_LOCATORS["product name"])
    LOGGER.debug(f"ASSERT: Product name '{product_name}' is not empty")
    assert not product_name.isspace(), f"Product name seems to be empty: '{product_name}'"


@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_product_price_is_greater_than_zero(browser, base_url, product_id):
    """Check price is greater than zero"""

    product_page = ProductPage(browser=browser, base_url=base_url, product_id=product_id)
    product_page.open()
    product_price = product_page.get_product_price(currency="$")
    LOGGER.debug(f"ASSERT: product '{product_page.get_tab_name()}' has non-zero price")
    assert product_price > 0, f"Seems product '{product_page.get_tab_name()}' has no price."


@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_product_has_main_image(browser, base_url, product_id):
    """Check product has at least one (main) image"""

    product_page = ProductPage(browser=browser, base_url=base_url, product_id=product_id)
    product_page.open()
    LOGGER.debug(f"ASSERT: Product '{product_page.get_tab_name()}' has main image")
    assert product_page.wait_element(PRODUCT_PAGE_LOCATORS[
                                         "product main image"]), f"Product '{product_page.get_tab_name()}' doesn`t have main image."


@pytest.mark.parametrize("product_id", XFAIL_PRODUCT_IDS)
def test_product_name_same_as_tab_name(browser, base_url, product_id):
    """Check product name is the same as browser tab (window) name"""

    product_page = ProductPage(browser=browser, base_url=base_url, product_id=product_id)
    product_page.open()
    tab_name = product_page.get_tab_name()
    product_name = product_page.get_element_text(PRODUCT_PAGE_LOCATORS["product name"])
    LOGGER.debug(f"ASSERT: tab name '{tab_name}' is the same as product name '{product_name}'")
    assert tab_name == product_name, f"Expected tab name '{tab_name}' the same as product name '{product_name}'"


@pytest.mark.parametrize("product_id", PRODUCT_IDS)
def test_product_name_same_in_title_and_breadcrumb_navigation(browser, base_url, product_id):
    """Check product name is the same as in the breadcrumb navigation"""

    product_page = ProductPage(browser=browser, base_url=base_url, product_id=product_id)
    product_page.open()
    product_name_title = product_page.get_element_text(PRODUCT_PAGE_LOCATORS["product name"])
    product_name_breadcrumb = product_page.get_element_text(
        PRODUCT_PAGE_LOCATORS["product name in breadcrumb navigation"])
    LOGGER.debug(
        f"ASSERT: product name in breadcrumb navigation '{product_name_breadcrumb}' is the same as product name title '{product_name_title}'")
    assert product_name_breadcrumb == product_name_title, \
        f"Expected product name in breadcrumb navigation '{product_name_breadcrumb}' the same as product name title '{product_name_title}'"
