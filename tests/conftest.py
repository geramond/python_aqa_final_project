import pytest
from faker import Faker

from page_objects import AdminPage
from page_objects.locators import ADMIN_PAGE_LOCATORS
from page_objects.elements import AddProductForm


@pytest.fixture(scope="function")
def login_as_admin(browser, base_url, user):
    admin_login_page = AdminPage.AdminLoginPage(browser, base_url)
    admin_login_page.open()
    admin_login_page.fill_field_login_page(user["username"], user["password"])
    login_button = admin_login_page.wait_element(ADMIN_PAGE_LOCATORS["login button"])
    login_button.click()
    return AdminPage.AdminDashboardPage(browser, base_url)


@pytest.fixture(scope="function")
def go_to_products(browser, base_url, login_as_admin, logged_in=False):
    if logged_in:
        page = AdminPage.AdminDashboardPage(browser, base_url)
        page.wait_element(ADMIN_PAGE_LOCATORS["open catalog"]).click()
        page.wait_element(ADMIN_PAGE_LOCATORS["catalog: products"]).click()
        return AdminPage.AdminProductsPage(browser, base_url)
    login_as_admin.go_to_products()
    return AdminPage.AdminProductsPage(browser, base_url)


@pytest.fixture(scope="function")
def go_to_add_new_product_page(browser, base_url, go_to_products):
    go_to_products.click_add_new_product()
    return AddProductForm(browser, base_url)


@pytest.fixture(scope="function")
def fake_user():
    f = Faker()
    fake_user = {
        "username": f.first_name(),
        "password": f.password()
    }
    return fake_user
