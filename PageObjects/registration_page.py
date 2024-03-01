import allure
from playwright.sync_api import Page, expect

# fields
username_filed = "#id_username"
email_field = "#id_email"
password_field = "#id_password1"
confirm_password_field = "#id_password2"

# buttons
submit_register_button = "input[value='Register']"


class RegistrationPage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step
    def create_account(self, username, email, password, confirmpass):
        self.page.fill(username_filed, username)
        self.page.fill(email_field, email)
        self.page.fill(password_field, password)
        self.page.fill(confirm_password_field, confirmpass)
        self.page.click(submit_register_button)

    @allure.step
    def check_register_form_is_displayed(self):
        reg_form = self.page.locator('.loginForm.regForm')
        expect(reg_form).to_be_visible()
