from enum import Enum


class AccountCredentials(Enum):
    customer_username = 'admin'
    customer_password = 'Test@123'


class ApiEndpoint(Enum):
    homepage_endpoint = '/parabank/index.htm'
    register_customer_with_session_id_endpoint = '/parabank/register.htm;jsessionid={0}'
    register_customer_endpoint = '/parabank/register.htm'

    login_endpoint = '/parabank/login.htm'
    overview_endpoint = '/parabank/overview.htm'
    logout_endpoint = '/parabank/logout.htm'


class ApiConstant(Enum):
    register_customer_payload = {
        "customer.firstName": "fname",
        "customer.lastName": "lname",
        "customer.address.street": "address",
        "customer.address.city": "city",
        "customer.address.state": "state",
        "customer.address.zipCode": "zipCode",
        "customer.phoneNumber": "",
        "customer.ssn": "1122",
        "customer.username": "admin007",
        "customer.password": "Test@123",
        "repeatedPassword": "Test@123"
    }
    hash_generating_payload = {"inputString": "", "secretKey": "", "algo": "SHA-256", "outputFormat": "text"}


class BackOfficeXpath(Enum):
    locate_elem_by_exact_text_xpath = './/*[text()="{0}"]'
    locate_elem_by_having_text_xpath = './/*[contains(text(), "{0}")]'


class BackOfficeConstant(Enum):
    screenshots_dir_path = '../screenshots/'


class FrontEndURL(Enum):
    homepage_url = '/parabank/index.htm'


class FrontEndXpath(Enum):
    locate_elem_by_exact_text_xpath = './/*[text()="{0}"]'
    locate_elem_by_having_text_xpath = './/*[contains(text(), "{0}")]'

    field_xpath = './/tr[.//*[contains(text(), "{0}")]]//input'
    registration_btn_xpath = './/input[@value="Register"]'

    username_field_xpath = './/input[@name="username"]'
    password_field_xpath = './/input[@name="password"]'

    login_btn_xpath = './/input[@value="Log In"]'


class FrontEndConstant(Enum):
    pass
