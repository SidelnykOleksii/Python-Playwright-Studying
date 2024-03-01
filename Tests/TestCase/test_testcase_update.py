import pytest
import allure

test_name = 'test for edit'
desc_name = 'test desc'
edited_name = 'edited test name'
edited_desc = 'edited desc'


@pytest.fixture()
def create_case_for_testing_via_ui(desktop_app_auth):
    desktop_app_auth.navigate_to('Create new test')
    desktop_app_auth.test_cases_page.create_test(test_name, desc_name)
    desktop_app_auth.navigate_to('Test Cases')

@pytest.fixture()
def create_case_for_testing_via_api(get_web_services):
    get_web_services.create_testcase_post('API test', desc_name)
    yield


@allure.step('User can edit test name')
def test_test_case_edit_name(desktop_app_auth, get_web_services):
    desktop_app_auth.navigate_to('Create new test')
    get_web_services.create_testcase_post('API test name', 'API desc')
    desktop_app_auth.test_cases_page.open_edit_test_case_form_by_name('API test')
    desktop_app_auth.test_cases_page.edit_test_name('Edited API test')
    desktop_app_auth.navigate_to('Test Cases')
    assert desktop_app_auth.test_cases_page.check_test_exists('Edited API test')
    desktop_app_auth.test_cases_page.delete_test_by_name('Edited API test')


@allure.step('User can edit description')
def test_test_case_edit_desc(desktop_app_auth, create_case_for_testing_via_ui):
    desktop_app_auth.test_cases_page.open_edit_test_case_form_by_name(test_name)
    desktop_app_auth.test_cases_page.edit_test_desc(edited_desc)
    desktop_app_auth.navigate_to('Test Cases')
    desktop_app_auth.test_cases_page.open_edit_test_case_form_by_name(test_name)
    desktop_app_auth.test_cases_page.check_test_description_in_edit_form(edited_desc)
    desktop_app_auth.navigate_to('Test Cases')
    desc = desktop_app_auth.test_cases_page.get_test_description_by_test_name(test_name)
    assert desc == edited_desc
    desktop_app_auth.test_cases_page.delete_test_by_name(test_name)
