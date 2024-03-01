import allure
from playwright.sync_api import Page, expect

# buttons
edit_test_case_button = '.editBtn '
delete_test_case_button = '.deleteBtn'
download_button = 'div.fileDownload input[type=button]'
upload_button = 'div.fileUploadBox a'

# create test case form
test_name_field = "//input[@id=\"id_name\"]"
test_desc_field = "//textarea[@id=\"id_description\"]"
submit_button = "//input[@type=\"submit\"]"

# edit form
edit_form_name_field = "#id_name"
edit_form_desc_field = "#id_description"
update_button = "//input[@value=\"Update\"]"


class TestCasesPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.expect = expect

    @allure.step
    def check_test_exists(self, test_name: str):
        return self.page.query_selector(f'css=tr >> text=\"{test_name}\"') is not None

    @allure.step
    def check_test_not_exists(self, test_name: str):
        return self.page.query_selector(f'css=tr >> text=\"{test_name}\"') is None

    @allure.step
    def create_test(self, test_name: str, test_description: str):
        self.page.fill(test_name_field, test_name)
        self.page.fill(test_desc_field, test_description)
        self.page.click(submit_button)

    @allure.step
    def check_test_description_in_edit_form(self, test_desc: str):
        field = self.page.locator('#id_description')
        self.expect(field).to_have_value(test_desc)

    @allure.step
    def get_test_description_by_test_name(self, test_name: str):
        desc = self.page.query_selector(f'*css=tr >> text=\"{test_name}\"').query_selector("//td[3]")
        return desc.inner_text()

    @allure.step
    def open_edit_test_case_form_by_name(self, test_name: str):
        row = self.page.query_selector(f'*css=tr >> text=\"{test_name}\"')
        if row is not None:
            row.query_selector(edit_test_case_button).click()
        else:
            raise ValueError('Element not found')

    @allure.step
    def edit_test_name(self, test_name: str):
        self.page.fill(edit_form_name_field, '')
        self.page.fill(edit_form_name_field, test_name)
        self.page.click(update_button)

    @allure.step
    def edit_test_desc(self, test_desc: str):
        self.page.fill(edit_form_desc_field, '')
        self.page.fill(edit_form_desc_field, test_desc)
        self.page.click(update_button)

    @allure.step
    def delete_test_by_name(self, test_name: str):
        row = self.page.query_selector(f'*css=tr >> text=\"{test_name}\"')
        row.query_selector(delete_test_case_button).click()

    @allure.step
    def get_test_case_rows_count(self):
        rows = self.page.query_selector_all('tbody > tr')
        return len(rows)

    @allure.step
    def get_test_total_on_test_case_page(self):
        element = self.page.query_selector('div.tableTitle')
        element_text = element.inner_text()
        split_text = element_text.split()
        total_text = split_text[-1].rstrip(')')
        total_number = int(total_text)
        return total_number

    @allure.step
    def get_test_total(self):
        total_element = self.page.query_selector('p.total > span')
        total_text = total_element.inner_text()
        return int(total_text)

    @allure.step
    def click_on_download_button(self):
        self.page.click(download_button)
