import allure


@allure.title('User can not log in with invalid username')
def test_invalid_login(desktop_app):
    desktop_app.login('invalid', 'Qamania123')
    assert desktop_app.error_message_is_visible()


@allure.title('User can not log in with invalid password')
def test_invalid_password(desktop_app):
    desktop_app.login('alice', 'Qamania12345')
    assert desktop_app.error_message_is_visible()
