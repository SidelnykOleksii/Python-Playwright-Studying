import allure


@allure.title('User can log in with valid data')
def test_valid_login(desktop_app):
    desktop_app.login('alice', 'Qamania123')
    assert desktop_app.logo_is_visible()
