from pytest import mark

create_test_case = {
    'argnames': 'name, description',
    'argvalues': [('test_name', 'test_descr'),
                  ('123', '321'),
                  ('test_name', '')],
    'ids': ['create with letters', 'create with digits', 'create with empty description']
}


@mark.parametrize(**create_test_case)
def test_create_new_test_case(desktop_app_auth, name, description):
    desktop_app_auth.navigate_to('Create new test')
    desktop_app_auth.test_cases_page.create_test(name, description)
    desktop_app_auth.navigate_to('Test Cases')
    assert desktop_app_auth.test_cases_page.check_test_exists(name)
    desktop_app_auth.test_cases_page.delete_test_by_name(name)
    desktop_app_auth.test_cases_page.check_test_not_exists(name)


def test_assert_test_cases_count(desktop_app_auth):
    total_count = desktop_app_auth.test_cases_page.get_test_total()
    desktop_app_auth.navigate_to('Test Cases')
    rows_count = desktop_app_auth.test_cases_page.get_test_case_rows_count()
    total_on_test_case_page = desktop_app_auth.test_cases_page.get_test_total_on_test_case_page()

    assert total_count == rows_count == total_on_test_case_page


# def test_create_via_api(desktop_app_auth):
#     desktop_app_auth.goto('test/new')
#     csrf_token = desktop_app_auth.page.locator('form input[type=hidden]').get_attribute('value')
#     test_name = 'Test via API'
#     response = desktop_app_auth.page.request.post('test/new', form={'csrfmiddlewaretoken': csrf_token,
#                                                                     'name': test_name,
#                                                                     'description': 'nice'})
#     if response.status_code != 200:
#         raise AssertionError(f"An invalid status code was received: {response.status_code}")

# test using web service (in progress)
# def test_delete_test_case(desktop_app_auth, get_web_services):
#     test_name = 'test_for_delete'
#     get_web_services.create_testcase_post(test_name, 'desc')
#     desktop_app_auth.navigate_to('Test Cases')
#     assert desktop_app_auth.test_cases_page.check_test_exists(test_name)
#     desktop_app_auth.test_cases_page.delete_test_by_name(test_name)
#     desktop_app_auth.test_cases_page.check_test_not_exists(test_name)
