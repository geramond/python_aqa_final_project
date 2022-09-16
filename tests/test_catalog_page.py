import pytest
import time
import logging.config

from page_objects import CatalogPage
from logging_settings import logger_config

from page_objects.locators import CATALOG_PAGE_LOCATORS

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")

CATALOG_IDS = [
    pytest.param("laptop-notebook", marks=pytest.mark.smoke),
    "windows", "tablet", "smartphone", "software", "mp3-players"
]


@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_catalog_name_same_as_tab_name(browser, base_url, catalog_id):
    """Check Catalog name is the same as browser tab name (window)"""

    catalog_page = CatalogPage(browser=browser, base_url=base_url, catalog_id=catalog_id)
    catalog_page.open()
    tab_name = catalog_page.get_tab_name()
    page_title = catalog_page.get_element_text(CATALOG_PAGE_LOCATORS["catalog page title"])
    LOGGER.debug(f"ASSERT: tab name '{tab_name}' is the same as catalog page title '{page_title}'")
    assert tab_name == page_title, f"Expected tab name '{tab_name}' to be the same as catalog page title '{page_title}'"


@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_if_no_products_in_category_should_be_appropriate_message(browser, base_url, catalog_id):
    f"""Check if no products in Catalog show message '{CatalogPage.NO_PRODUCTS_MESSAGE}'"""

    catalog_page = CatalogPage(browser=browser, base_url=base_url, catalog_id=catalog_id)
    catalog_page.open()
    if not catalog_page.wait_element(CATALOG_PAGE_LOCATORS["products on page"]):
        LOGGER.debug(f"There is no products on {catalog_id}")
        page_description = catalog_page.get_element_text(CATALOG_PAGE_LOCATORS["no products in category"])
        LOGGER.debug(f"ASSERT: page description text is '{catalog_page.NO_PRODUCTS_MESSAGE}'")
        assert page_description == catalog_page.NO_PRODUCTS_MESSAGE, \
            f"Expected to see text '{catalog_page.NO_PRODUCTS_MESSAGE}'\
             because catalog '{catalog_id}' does not have any products. But got '{page_description}'"
        LOGGER.debug(f"ASSERT: 'Continue' button is on the page")
        assert catalog_page.wait_element(CATALOG_PAGE_LOCATORS["no products in category > continue button"]), \
            f"Expected to see 'Continue' button on the page, but didn`t find it"


@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_switch_products_view(browser, base_url, catalog_id):
    """Check:
        - All products are shown in grid by default
        - After switching to 'list' view -- show in list
    """

    catalog_page = CatalogPage(browser=browser, base_url=base_url, catalog_id=catalog_id)
    catalog_page.open()
    if catalog_page.wait_element(CATALOG_PAGE_LOCATORS["products on page"]):
        # grid view is default
        LOGGER.debug(f"ASSERT: all products are shown in grid by default")
        assert (
                catalog_page.get_element_if_present(CATALOG_PAGE_LOCATORS["products on page grid"])
                and
                not catalog_page.get_element_if_present(CATALOG_PAGE_LOCATORS["products on page list"])
        ), f"All products are NOT shown in grid (which should be the default view mode)"

        # switch to list view
        catalog_page.click(CATALOG_PAGE_LOCATORS["list view button"])
        LOGGER.debug(f"ASSERT: all products are shown in list, after switching to the 'list' view")
        assert (
                catalog_page.click(CATALOG_PAGE_LOCATORS["list view button"])
                and
                not catalog_page.get_element_if_present(CATALOG_PAGE_LOCATORS["products on page grid"])
        ), f"All products are NOT shown in list (after switching to the 'list' view)"


@pytest.mark.parametrize("product_index", [
    pytest.param(1, marks=pytest.mark.smoke),
    2, 3])
@pytest.mark.parametrize("catalog_id", CATALOG_IDS)
def test_add_product_to_cart_should_be_success_message_and_increase_cart_total(browser, base_url, catalog_id,
                                                                               product_index):
    """Check:
        - After adding product to cart: 'total items' = 1, 'cart price' > 0
        - If product has NO required fields, it can be added to cart from 'Catalog page' immediately
        - If product has required fields, user gets redirected to product page
    """

    catalog_page = CatalogPage(browser=browser, base_url=base_url, catalog_id=catalog_id)
    catalog_page.open()
    if catalog_page.wait_element(CATALOG_PAGE_LOCATORS["products on page"]):

        # check only catalogs contains at least 1 product
        LOGGER.debug(f"Catalog '{catalog_id}' contains at least 1 product")
        catalog_page.scroll_to_element(CATALOG_PAGE_LOCATORS["add to cart buttons"])
        try:
            catalog_page.add_to_cart(product_index)
            time.sleep(1)  # url can be changed. this is reason for waiting
            if browser.current_url != catalog_page.url:

                # if product has required fields it can`t be added from Catalog - redirect to product page happen
                # check the product has at least 1 required field
                LOGGER.debug("User is redirected to the product page. Seems this product has required fields...")
                catalog_page.scroll_to_element(CATALOG_PAGE_LOCATORS["add to cart required fields"])
                LOGGER.debug(f"ASSERT: product '{browser.current_url}' has at least 1 required field")
                assert catalog_page.get_element_if_present(CATALOG_PAGE_LOCATORS["add to cart required fields"],
                                                           only_first=True), \
                    f"Product '{browser.current_url}' doesn`t have any required field.\
                So it should have been added to cart from main page (but wasn`t)"
            else:

                # other products can be added from Catalog page, should be success message
                catalog_page.wait_element(
                    CATALOG_PAGE_LOCATORS["alert"])  # page automatically scrolls to top, but it takes same time
                success_message = catalog_page.get_element_if_present(CATALOG_PAGE_LOCATORS["alert"], only_first=True)
                success_message_text = catalog_page.get_element_text(success_message)
                LOGGER.debug(f"ASSERT: there is success message")
                assert "Success: You have added" and " to your shopping cart!" in success_message_text, \
                    f"Expected success message to be ' Success: You have added ... to your shopping cart!',\
                     but got {success_message_text}"
                items_in_cart, total_price = catalog_page.get_cart_item_count_and_total_price()
                LOGGER.debug(f"ASSERT: should be 1 item in cart")
                assert items_in_cart == 1 and total_price != 0, \
                    f"Should be 1 item in cart, but got {items_in_cart} items, total price is ${total_price}"

        except IndexError:
            # check adding to cart first N products in category
            # and ignore if category contains less than N products
            pass
