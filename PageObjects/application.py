import allure
from playwright.sync_api import Browser
from settings import DEFAULT_TIMEOUT
from .test_cases_page import TestCasesPage
from .registration_page import RegistrationPage


class App:
    def __init__(self, browser: Browser, base_url: str, **kwargs):
        self.browser = browser
        self.context = self.browser.new_context(**kwargs)
        self.context.set_default_timeout(DEFAULT_TIMEOUT)
        self.page = self.context.new_page()
        self.base_url = base_url
        self.test_cases_page = TestCasesPage(self.page)
        self.registration_page = RegistrationPage(self.page)

    @allure.step
    def goto(self, endpoint: str, use_base_url=True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)

    @allure.step
    def open_registration_page_from_login_form(self):
        self.page.click("//a[@href='/register/']")

    @allure.step
    def navigate_to(self, menu: str):
        self.page.click(f"css=header >> text=\"{menu}\"")

    @allure.step
    def login(self, login: str, password: str):
        self.page.fill("//input[@id=\"id_username\"]", login)
        self.page.fill("//input[@id=\"id_password\"]", password)
        self.page.click("//input[@value=\"Login\"]")

    @allure.step
    def logo_is_visible(self):
        return self.page.locator('.logo > a') is not None

    @allure.step
    def new_user_name_is_visible(self, user_name: str):
        element = self.page.query_selector('div.account')
        element_text = element.inner_text()
        split_text = element_text.split(', ')
        new_user_name = split_text[1]
        assert new_user_name == user_name

    @allure.step
    def login_form_is_visible(self):
        return self.page.locator('.loginForm') is not None

    @allure.step
    def error_message_is_visible(self):
        return self.page.locator('.loginError') is not None

    @allure.step
    def log_out(self):
        self.page.click('.logOut')

    @allure.step
    def download_file(self, url, locator, file_path):
        with self.page.expect_download() as download_info:
            self.goto(url)
            self.page.click(locator)
        download = download_info.value
        path = download.path()
        download.save_as(file_path)

    @allure.step
    def upload_file(self, url, locator, upload_file_path):
        """
        Uploads the file according to the specified path to the specified location on the page.

        :param url: The URL of the page to upload the file to.
        :param locator: The locator of the element to click on to open the file upload dialog.
        :param upload_file_path: The path to the file to upload.
        """
        with self.page.expect_file_chooser() as fc_info:
            self.goto(url)
            self.page.click(locator)
            file_chooser = fc_info.value
            file_chooser.set_files(upload_file_path)
        try:
            file_chooser = fc_info.value
            if file_chooser:
                file_chooser.set_files(upload_file_path)
                self.page.wait_for_timeout(5000)
            else:
                raise ValueError("File chooser element not found.")
        except Exception as e:
            print(f"An error occurred while uploading the file: {e}")

    @allure.step
    def close(self):
        self.page.close()
        self.context.close()
        self.browser.close()
