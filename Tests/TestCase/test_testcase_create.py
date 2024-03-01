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
