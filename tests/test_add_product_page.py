import pytest
import logging.config

from page_objects.AdminPage import AdminProductsPage
from logging_settings import logger_config

from page_objects.locators import ADD_PRODUCT_PAGE_LOCATORS

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


@pytest.mark.smoke
def test_click_add_new_product_should_open_page(browser, base_url, go_to_add_new_product_page):
    """Should be 'Save' button on the 'Add new product page'"""

    add_page = go_to_add_new_product_page
    LOGGER.debug("ASSERT: There is the 'Save' button on the 'Add New Product' page.")
    assert add_page.wait_element(
        add_page.LOCATORS["save"]), f"Unable to find the 'Save' button on the 'Add New Product' page."


def test_add_new_product_page_contains_all_tabs(browser, base_url, go_to_add_new_product_page):
    """Should be all tabs on the 'Add new product' page: 'General', 'Data', 'Links', 'Attribute', etc."""

    add_page = go_to_add_new_product_page
    LOGGER.debug("ASSERT: All settings tabs are present on the 'Add new product' page.")
    for tab_name, locator in ADD_PRODUCT_PAGE_LOCATORS["tab"].items():
        LOGGER.debug(f"ASSERT: '{tab_name}' tab is present")
        assert add_page.get_element_if_present(
            locator), f"Unable to locate '{tab_name}' tab on the 'Add new product' page."


def test_general_tab_contains_all_fields(browser, base_url, go_to_add_new_product_page):
    """Check all fields are present on the 'General' tab"""

    add_page = go_to_add_new_product_page
    LOGGER.debug("ASSERT: 'General' tab contains all fields (on 'Add new product' page)")
    for field_name, locator in ADD_PRODUCT_PAGE_LOCATORS["general"].items():
        LOGGER.debug(f"ASSERT: field '{field_name}' is present")
        assert add_page.get_element_if_present(locator), f"Unable to locate '{field_name}' field on the 'General' tab."


@pytest.mark.smoke
@pytest.mark.xfail(reason="Fails in headless mode (only)")
def test_add_new_product_filling_only_required_fields(browser, base_url, go_to_add_new_product_page):
    """Create product filling only required fields: Name, Meta, Model"""

    add_page = go_to_add_new_product_page
    new_product = add_page.create_product()
    product_list_filtered = AdminProductsPage(browser, base_url).filter_products_by(name=new_product['name'])
    LOGGER.debug(f"ASSERT: new product '{new_product['name']}' appeared in the Products list")
    assert product_list_filtered.get_product_by_name(
        new_product['name']), f"Unable to find newly created product '{new_product['name']}' in the Products list."


@pytest.mark.paremetrize("fields", [{"name": "", "model": "test1", "meta": "test2"},
                                    {"name": "test1", "model": "", "meta": "test2"},
                                    {"name": "test1", "model": "test2", "meta": ""}])
def test_cant_add_new_product_with_empty_required_field(fields, browser, base_url, go_to_add_new_product_page):
    """Should be not able to create product if any of required fields is empty: Name, Model or Meta"""

    add_page = go_to_add_new_product_page
    add_page.create_product(**fields)
    LOGGER.debug(
        f"ASSERT: there is an error message when trying to save a product with empty one of required field: {fields}")
    assert add_page.wait_element(ADD_PRODUCT_PAGE_LOCATORS["error banner"],
                                 f"Expected to get error message trying to save a product with empty one of the required fields: '{fields}'")


def test_page_title(browser, base_url, go_to_add_new_product_page):
    """Page title should be 'Add Product'"""

    add_page = go_to_add_new_product_page
    page_title = add_page.get_element_text(ADD_PRODUCT_PAGE_LOCATORS["page title"])
    LOGGER.debug(f"ASSERT: Page title to be '{add_page.PAGE_TITLE}'")
    assert add_page.PAGE_TITLE in page_title, f"Expected page title to be '{add_page.PAGE_TITLE}', but got '{page_title}'"
