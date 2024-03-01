import allure


@allure.title('User can log out')
def test_log_out(desktop_app_auth):
    desktop_app_auth.log_out()
    assert desktop_app_auth.login_form_is_visible()
