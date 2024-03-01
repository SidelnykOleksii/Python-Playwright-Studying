import pytest
import os
import json
from settings import *
from pytest import fixture, hookimpl
from playwright.sync_api import sync_playwright
from PageObjects.application import App
from helpers.web_service import WebService
from helpers.db import DataBase


@pytest.fixture(scope="session")
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def get_web_services(request):
    # base_url = request.config.getini('base_url')
    # secure = request.config.getoption('--secure')
    # config = load_config(request.session.fspath.strpath, secure)
    # web = WebService(base_url)
    # web.login_post(**config['users']['userRole1'])
    # yield web
    # web.close()
    web = WebService(base_url='http://127.0.0.1:8000/')
    web.login_post('alice', 'Qamania123')
    yield web
    web.close()


@pytest.fixture(scope="session", params=['chromium'])
def get_browser(get_playwright, request):
    browser = request.param
    os.environ['PWBROWSER'] = browser
    headless = request.config.getini('headless')
    if headless == 'True':
        headless = True
    else:
        headless = False

    if browser == 'chromium':
        bro = get_playwright.chromium.launch(headless=headless)
    elif browser == 'firefox':
        bro = get_playwright.firefox.launch(headless=headless)
    elif browser == 'webkit':
        bro = get_playwright.webkit.launch(headless=headless)
    else:
        assert False, 'unsupported browser type'
    yield bro
    bro.close()
    del os.environ['PWBROWSER']


@pytest.fixture(scope="session")
def desktop_app(get_browser, request):
    base_url = request.config.getini('base_url')
    app = App(get_browser, base_url=base_url, **BROWSER_OPTION)
    app.goto('/')
    yield app
    app.close()


@pytest.fixture(scope="session")
def desktop_app_auth(desktop_app):
    app = desktop_app
    app.goto('/login')
    app.login('alice', 'Qamania123')
    yield app


@pytest.fixture(scope="session")
def get_db(request):
    path = request.config.getini('db_path')
    db = DataBase(path)
    yield db
    db.close()


def pytest_addoption(parser):
    parser.addoption('--secure', action='store', default='secure.json')
    parser.addini('base_url', help='base url of site under test', default='http://127.0.0.1:8000')
    parser.addini('db_path', help='path to sqlite db file', default='D:\\IT\\Python_Playwright_Course\\TestMe\\TestMe-TCM\\db.sqlite3')
    parser.addini('headless', help='run browser in headless mode', default='True')
    parser.addini('tcm_report', help='report test results to tcm', default='False')


def load_config(project_path, file: str) -> dict:
    config_file = os.path.join(project_path, file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())
