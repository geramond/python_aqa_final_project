import pytest
import datetime
import os
import mysql.connector
import logging
import json
import allure

from selenium import webdriver
from selenium.webdriver.opera.options import Options

import logging.config
from logging_settings import logger_config

logging.config.dictConfig(logger_config)
LOGGER_START = logging.getLogger("file_logger_start")
LOGGER_ENV = logging.getLogger("file_logger_env")

DRIVERS = os.path.expanduser("~/Downloads/drivers")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to run tests. Default is 'chrome'. Also available: 'safari', 'firefox', 'opera', 'yandex', 'edge'")
    parser.addoption("--executor", action="store", default="127.0.0.1",
                     help="Specify IP of Selenoid. Or 'local' to run without Selenoid. Default is '127.0.0.1'")
    parser.addoption("--mobile", action="store_true")
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--logs", action="store_true")
    parser.addoption("--videos", action="store_true")
    parser.addoption("--bv", default=None)
    parser.addoption("--url", "-U", action='store', default="http://demo.opencart.com", help="Opencart base url")
    parser.addoption("--tolerance", type=int, default=3)
    parser.addoption("--log_level", action="store", default="DEBUG")
    parser.addoption('--username', action='store')
    parser.addoption('--password', action='store')


@pytest.fixture
def base_url(request):
    base_url = request.config.getoption('--url')
    if base_url[-1] != "/":
        base_url += "/"
    return base_url


@pytest.fixture
def browser(request):
    """ Фикстура инициализации браузера """

    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    version = request.config.getoption("--bv")
    vnc = request.config.getoption("--vnc")
    logs = request.config.getoption("--logs")
    videos = request.config.getoption("--videos")
    mobile = request.config.getoption("--mobile")
    url = request.config.getoption("--url")
    tolerance = request.config.getoption("--tolerance")
    log_level = request.config.getoption("--log_level")

    logger = logging.getLogger(request.node.name)
    file_handler = logging.FileHandler(f"logs/{request.node.name}.log")
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    logger.info("===> Test {} started at {}".format(request.node.name, datetime.datetime.now()))

    # https://www.selenium.dev/documentation/en/webdriver/page_loading_strategy/
    common_caps = {"pageLoadStrategy": "eager",
                   "browserVersion": version,
                   "name": "Maksim",
                   "selenoid:options": {
                       "enableVNC": vnc,
                       "enableVideo": videos,
                       "enableLog": logs
                   },
                   'acceptSslCerts': True,
                   'acceptInsecureCerts': True,
                   'timeZone': 'Europe/Moscow',
                   'goog:chromeOptions': {}
                   }

    if executor == "local":
        caps = {'goog:chromeOptions': {}}

        if mobile:
            caps["goog:chromeOptions"]["mobileEmulation"] = {"deviceName": "iPhone 5/SE"}

        driver = webdriver.Chrome(
            executable_path=f"{DRIVERS}/chromedriver",
            desired_capabilities=common_caps
        )
    else:

        desired_capabilities = {
            "browser": browser,
            **common_caps
        }

        options = Options()
        if browser == "opera":
            options.add_experimental_option('w3c', True)

        driver = webdriver.Remote(
            desired_capabilities=desired_capabilities,
            command_executor=f"http://{executor}:4444/wd/hub",
            options=options
        )

        if not mobile:
            driver.maximize_window()

    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.capabilities),
        attachment_type=allure.attachment_type.JSON)

    def fin():
        driver.quit()
        logger.info("===> Test {} finished at {}".format(request.node.name, datetime.datetime.now()))

    # request.addfinalizer(driver.quit)
    request.addfinalizer(fin)

    def open(path=""):
        return driver.get(url + path)

    driver.maximize_window()

    driver.open = open
    driver.open()
    driver.t = tolerance

    return driver


@pytest.fixture
def db_connection(request):
    connection = mysql.connector.connect(
        user='bn_opencart',
        password='',
        host='127.0.0.1',
        database='bitnami_opencart',
        port='3306'
    )
    request.addfinalizer(connection.close)
    return connection


@pytest.fixture(scope="function")
def user(request):
    username = request.config.getoption('--username')
    password = request.config.getoption('--password')
    yield {"username": username, "password": password}


@pytest.fixture(scope="function", autouse=True)
def log():
    current_test_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    LOGGER_START.debug(f"{current_test_name}")


@pytest.fixture(scope="session", autouse=True)
def log_env(request):
    browser = request.config.getoption('--browser')
    executor = request.config.getoption('--executor')
    version = request.config.getoption('--bv')
    vnc = request.config.getoption('--vnc')

    if executor == 'local':
        LOGGER_ENV.info(f"Running tests locally in {browser}")
    else:
        LOGGER_ENV.info(f"Running tests on http://{executor}/wd/hub via Selenoid in {browser}"
                        f"(parameters: vnc= {vnc}, browser_version={version})")
