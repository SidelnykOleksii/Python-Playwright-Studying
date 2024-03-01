import allure
from pytest import mark

missed_mandatory_field = {
    "argnames": 'username, email, password, confirmpass',
    "argvalues": [('', '', 'Qamania123', 'Qamania123'),
                  ('test_user', '', '', 'Qamania123'),
                  ('test_user', '', 'Qamania123', '')],
    "ids": ['missed username', 'missed password', 'missed confirm password']
}


@mark.parametrize(**missed_mandatory_field)
def test_required_fields(desktop_app, username, email, password, confirmpass):
    desktop_app.goto('register/')
    desktop_app.registration_page.create_account(username, email, password, confirmpass)
    desktop_app.registration_page.check_register_form_is_displayed()


@allure.title('User can register new account with valid data')
def test_register_valid_data(desktop_app, get_db):
    new_user = 'TestUser_90@'
    email = 'test_email_6@mail.com'
    desktop_app.goto('register/')
    desktop_app.registration_page.create_account(new_user, email, 'Qamania123', 'Qamania123')
    assert desktop_app.logo_is_visible()
    desktop_app.new_user_name_is_visible(new_user)
    result = get_db.check_user_exist(new_user, email)
    assert result is not None
    get_db.delete_user(new_user)
