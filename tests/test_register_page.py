import pytest

import logging.config
from page_objects import UserRegisterPage
from logging_settings import logger_config

from page_objects.locators import REGISTER_PAGE_LOCATORS

logging.config.dictConfig(logger_config)
LOGGER = logging.getLogger("file_logger")


@pytest.mark.smoke
def test_registration(browser, base_url):
    """Test simple valid registration flow"""
    register_page = UserRegisterPage(browser, base_url)
    register_page.open()
    register_page.wait_element(REGISTER_PAGE_LOCATORS["first name"])
    fake_user = register_page.generate_user()
    register_page.fill_field_register_page(**fake_user)
    register_page.click(REGISTER_PAGE_LOCATORS["agree to privacy policy checkbox"])
    register_page.click(REGISTER_PAGE_LOCATORS["continue"])
    LOGGER.debug(
        f"ASSERT: successfully registered and redirected to '{register_page.SUCCESS_REGISTRATION_URL_APPENDIX}'")
    assert register_page.SUCCESS_REGISTRATION_URL_APPENDIX in browser.current_url, \
        f"Expected to reach {register_page.SUCCESS_REGISTRATION_URL_APPENDIX} after registration, but got {browser.current_url}"


def test_should_be_link_to_login_page(browser, base_url):
    """Check user can go to 'login' page from 'register'"""
    register_page = UserRegisterPage(browser, base_url)
    register_page.open()
    login_link = register_page.wait_element(REGISTER_PAGE_LOCATORS["login link"])
    register_page.click(login_link)
    LOGGER.debug(f"ASSERT: reached '{base_url + register_page.LOGIN_URL_APPENDIX}' after clicking 'login page' link")
    assert register_page.LOGIN_URL_APPENDIX in browser.current_url, \
        f"Expected to reach '{base_url + register_page.LOGIN_URL_APPENDIX}' after clicking 'login page' link"


def test_cant_register_if_dont_agree_policy(browser, base_url):
    """Check user can`t register if doesn`t enable 'Agree policy' checkbox"""
    register_page = UserRegisterPage(browser, base_url)
    register_page.open()
    register_page.wait_element(REGISTER_PAGE_LOCATORS["first_name"])
    fake_user = register_page.generate_user()
    register_page.fill_field_register_page(**fake_user)

    # Skip 'Agree policy' checkbox
    LOGGER.debug(f"Skipping 'Agree policy' checkbox")
    register_page.click(REGISTER_PAGE_LOCATORS["continue"])
    error_banner = register_page.wait_element(REGISTER_PAGE_LOCATORS["error banner"])
    error_banner_text = register_page.get_element_text(error_banner)
    LOGGER.debug(f"ASSERT: There is error message: '{register_page.ERROR_TEXT_POLICY}'")
    assert register_page.ERROR_TEXT_POLICY in error_banner_text, \
        f"Expected to get error message: '{register_page.ERROR_TEXT_POLICY}', but got '{error_banner_text}'"


@pytest.mark.smoke
@pytest.mark.parametrize("user_data_item", UserRegisterPage.EXAMPLE_USER.keys())
def test_cant_register_if_any_of_mandatory_fields_is_empty(browser, base_url, user_data_item):
    """Check user can`t register if he doesn`t fill all required fields. User stays 'register page'"""
    register_page = UserRegisterPage(browser, base_url)
    register_page.open()
    register_page.wait_element(REGISTER_PAGE_LOCATORS["first name"])
    fake_user = register_page.generate_user()
    del (fake_user[user_data_item])
    register_page.fill_field_register_page(**fake_user)
    register_page.click(REGISTER_PAGE_LOCATORS["agree to privacy policy checkbox"])
    register_page.click(REGISTER_PAGE_LOCATORS["continue"])
    LOGGER.debug(f"ASSERT: can`t register if one of mandatory field is empty, user stays on 'register page'")
    assert browser.current_url == register_page.url, \
        f"Expected user stays on register page if there is an error in registration, but URL changed to {browser.current_url}"


def test_cant_register_if_password_and_pass_confirm_dont_match(browser, base_url):
    """Check user cant register if password confirmation incorrect"""
    register_page = UserRegisterPage(browser, base_url)
    register_page.open()
    register_page.wait_element(REGISTER_PAGE_LOCATORS["first name"])
    fake_user = register_page.generate_user()
    fake_user["password_confirm"] += "#"
    register_page.fill_field_register_page(**fake_user)
    register_page.click(REGISTER_PAGE_LOCATORS["agree to privacy policy checkbox"])
    register_page.click(REGISTER_PAGE_LOCATORS["continue"])
    LOGGER.debug(f"ASSERT: cant register if password confirmation incorrect, user stays on 'register page'")
    assert browser.current_url == register_page.url, \
        f"Expected user stays on register page if password confirmation incorrect, but URL changed to '{browser.current_url}'"
