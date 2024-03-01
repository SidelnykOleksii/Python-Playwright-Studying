import os
import allure


@allure.step('User can download file')
def test_download_testcase(desktop_app_auth):
    desktop_app_auth.download_file('/tests/', 'div.fileDownload input[type=button]', 'downloads/test.csv')
    # compare function
    # delete downloaded file

# example if use Python
# desktop_app_auth.goto('/tests/')
# with desktop_app_auth.page.expect_download() as d_file:
#     desktop_app_auth.test_cases_page.click_on_download_button()
# f_url = d_file.value.url
# print(d_file.value.path())
# desktop_app_auth.page.wait_for_timeout(4000)
# current_working_dir = os.getcwd()
# file_path = os.path.join(current_working_dir, "./downloads/file.csv")
# d_file.value.save_as(file_path)


@allure.step('User can upload file')
def test_upload_testcase(desktop_app_auth):
    test_name = 'test_upload_summary'
    test_desc = 'test_upload_desc'
    desktop_app_auth.upload_file('/tests/', 'div.fileUploadBox a', 'Shared/TestData/csv/test_upload.csv')
    assert desktop_app_auth.test_cases_page.check_test_exists(test_name)
    desc = desktop_app_auth.test_cases_page.get_test_description_by_test_name(test_name)
    assert desc == test_desc
    desktop_app_auth.test_cases_page.delete_test_by_name(test_name)
