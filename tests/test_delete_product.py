import pytest
import logging.config

from page_objects.AdminPage import AdminProductsPage
from logging_settings import logger_config

from page_objects.locators import ADMIN_PAGE_LOCATORS

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


@pytest.mark.smoke
def test_add_new_product_and_delete(browser, base_url, go_to_add_new_product_page):
    """Create product filling only required fields: name, meta, model"""

    add_new_product_page = go_to_add_new_product_page
    created_product = add_new_product_page.create_product()

    products_page = AdminProductsPage(browser, base_url)
    products_page.filter_and_select_exact_product(created_product["name"])
    products_page.delete_selected_products()
    product_amount_after_deletion = products_page.filter_products_by(
        name=created_product["name"]).get_products_amount_on_page()

    LOGGER.debug("ASSERT: There is no products on page (deleted product and filtered product by its name)")
    assert product_amount_after_deletion == 0, \
        f"Didn`t expect to find the product '{created_product['name']}' on page after deletion, but found it!"


def test_should_be_alert_on_delete_action(browser, base_url, go_to_add_new_product_page):
    """Check there is alert after clicking the 'Delete' button"""

    add_new_product_page = go_to_add_new_product_page
    created_product = add_new_product_page.create_product()

    products_page = AdminProductsPage(browser, base_url)
    products_page.filter_and_select_exact_product(created_product["name"])
    products_page.click(ADMIN_PAGE_LOCATORS["delete"])

    LOGGER.debug("ASSERT: There is alert, after clicking the 'Delete' button")
    assert products_page.wait_alert(), f"Expected to get an alert after clicking 'Delete' button, but didn`t find it."
    products_page.wait_alert().accept()


def test_should_not_delete_product_if_dismiss_alert(browser, base_url, go_to_add_new_product_page):
    """Check didn`t delete product if user dismissed 'Delete product?' alert"""

    add_new_product_page = go_to_add_new_product_page
    created_product = add_new_product_page.create_product()

    products_page = AdminProductsPage(browser, base_url)
    products_page.filter_and_select_exact_product(created_product["name"])
    products_page.click(ADMIN_PAGE_LOCATORS["delete"])

    products_page.wait_alert().dismiss()
    product_amount_after_deletion = products_page.filter_products_by(
        name=created_product["name"]).get_products_amount_on_page()
    LOGGER.debug(f"ASSERT: There is '{created_product['name']}' on page, because we didn`t confirm deleting it")
    assert product_amount_after_deletion == 1, \
        f"Expected to find the product '{created_product['name']}' on page, because it should not been deleted,\
        but didn`t found it!"
