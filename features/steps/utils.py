import copy
import json
import logging
import pathlib
import random
import string
from enum import Enum
from time import sleep

import requests
import requests.auth
import selenium.common.exceptions as exceptions
import selenium.webdriver.chrome.options as chrome_options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from steps import constants

logger = logging.getLogger('myLogger')


class ConfigVars(Enum):
    """Configuration ConfigVars from behave.ini are mapped in this class.

        Enum (Enum): Generic enumeration.
    """

    browser = 'browser'
    server = 'server'

    driver_wait_time = 'DRIVER_WAIT_TIME'
    stable_elems_sleep = 'STABLE_ELEMS_SLEEP'
    unstable_elems_sleep = 'UNSTABLE_ELEMS_SLEEP'


def get_value_from_ini(context, key):
    """This function returns the configuration value from behave.ini.

    Args:
        context (Context): The default object is available throughout Behave framework.
        key (Any): Key in the key-value pair from the behave.ini.

    Returns:
        Value (Enum): Value in the key-value pair from the behave.ini
    """

    return context.config.userdata.get(key)


def to_camel_case(regular_str):
    """This function converts the provided string in to camel case formatted string.

    Args:
        regular_str (str): The simple string that should be converted to camel case.

    Returns:
        camel_case_str (str): The string in the camel case format.
    """

    components = regular_str.split(' ')

    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    camel_case_str = components[0].lower() + ''.join(x.title() for x in components[1:])

    return camel_case_str


def get_random_string(length):
    """This function generates the random string of the given length.

    Args:
        length (int): The total number of characters in the randomly generated string.

    Returns:
        result_str (str): The randomly generated string.
    """

    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    logger.debug(f'Random string of length {length} is "{result_str}"')
    return result_str


def get_random_number(length):
    """This function generates the random number of the given length.

    Args:
        length (int): The total number of digits in the randomly generated number.

    Returns:
        result_str (str): The randomly generated number
    """

    digits = string.digits
    result_str = ''.join(random.choice(digits) for i in range(length))
    logger.debug(f'Random number of length {length} is "{result_str}"')
    return result_str


def assert_text(expected_text, actual_text, _text_to_assert="Text"):
    """This function checks whether two strings are equal in every aspect.

    Args:
        expected_text (str): The expected string to compare.
        actual_text (str): The actual string to compare with.
        _text_to_assert (str): What sort of text is about to be asserted.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if the provided strings aren't the same.
    """

    error_msg = f'Expected text for "{_text_to_assert}" was "{expected_text}" but got "{actual_text}" instead.'

    assert str(actual_text) == str(expected_text), error_msg

    logger.debug(f'"{_text_to_assert}" | Expected: "{expected_text}" | Actual: "{actual_text}"')


def assert_text_contains(expected_text, actual_text, _text_to_assert="Text"):
    """This function checks whether the expected string is a subset of the actual string or not.

    Args:
        expected_text (str): The expected string to compare.
        actual_text (str): The actual string to compare with.
        _text_to_assert (str): What sort of text is about to be asserted.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if the provided strings aren't the same.
    """

    error_msg = f'Searching in "{_text_to_assert}" | Unable to find expected text "{expected_text}".'

    assert str(expected_text) in str(actual_text), error_msg

    logger.debug(f'Searching in "{_text_to_assert}" | Contains: "{expected_text}"')


def get_file_path(file_name):
    """This function creates the absolute path of the file from the test-files directory.

    Args:
        file_name (str): The name of the file that is being placed in the test-files folder.

    Returns:
        file_path (str): The absolute path of the filename provided.
    """

    root_path = pathlib.Path(__file__).parents[2]
    file_path = f'{root_path}/features/test-files/{file_name}'
    return file_path


def cleanup_text(text):
    """This function cleans extra spaces and line breaks from the provided text.

    Args:
        text (str): The string that needs to be cleaned.

    Returns:
        new_text (str): The new string without extra spaces and line breaks.
    """

    new_text = text

    while True:

        if '\r' in new_text:
            new_text = new_text.replace('\r', '').strip()

        if '\n' in new_text:
            new_text = new_text.replace('\n', ' ').strip()

        if '  ' in new_text:
            new_text = new_text.replace('  ', ' ').strip()

        if '\n' not in new_text and '  ' not in new_text:
            return new_text


def has_context_attr(context, required_attr):
    """This function makes sure that the provided attribute is present in the context.

    Args:
        context (Context): The default object is available throughout Behave framework.
        required_attr (str): The attribute to look for in the context.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if required attribute is not found in the context.
    """

    if not hasattr(context, required_attr):
        raise AssertionError(f'Context is missing required attribute "{required_attr}".')
    else:
        logger.debug(f'Context has required attribute "{required_attr}".')


def get_json_response(context):
    """This function returns the response of recently generated request in the json format.

    Args:
        context (Context): The default object is available throughout Behave framework.

    Returns:
        json_response (dict): The response of the request in the json format.
    """

    text_to_assert = 'Content-Type'
    expected_text = 'application/json'
    actual_text = context.response.headers[text_to_assert]

    assert_text(expected_text, actual_text, text_to_assert)

    return context.response.json()


def generate_hash(username, _secret_key='any_secret_key.com'):
    """This function generates the hash value against the provided username.

    Args:
        username (str): The username of the account holder.
        _secret_key (str): Any Secret key to use while creating hash.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if the "Status Code" of the request being made is not 200.

    Returns:
        hash_string (str): The hash being generated.
    """

    website_url = 'https://www.devglan.com/online-tools/hmac-sha256-online'

    payload = copy.deepcopy(constants.ApiConstant.hash_generating_payload.value)

    payload["inputString"] = username
    payload["secretKey"] = _secret_key

    logger.debug(f'Payload for generating hash: {payload}')

    response = requests.post(website_url, json=payload)

    if response.status_code == 200:
        return response.json()["outputString"]
    else:
        raise AssertionError(f'Unable to generate Hash for user: {username} with status code: {response.status_code}')


# Backend Testing utils


def validate_endpoint(context, _request_type):
    """This function validates that the context has required endpoint attribute to make the request.

    Args:
        context (Context): The default object is available throughout Behave framework.
        _request_type (str): CRUD operation being used while making the request.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if 'endpoint' attribute is not found in the context.
                        2) Something goes fishy on the server side.
    """

    server = get_value_from_ini(context, ConfigVars.server.value)

    if not hasattr(context, 'endpoint'):
        raise AssertionError(f'Context should have a valid "endpoint" attribute to make "{_request_type}" request.')

    if server not in context.endpoint:
        context.endpoint = server + context.endpoint


def generate_request_logs(context, _request_type):
    """This function generates specific logs for testing purposes based on the attributes being passed in the context.

    Args:
        context (Context): The default object is available throughout Behave framework.
        _request_type (str): CRUD operation being used while making the request.
    """

    if not hasattr(context, 'payload'):
        context.payload = {}
    elif context.payload:
        logger.debug(f'Payload: {context.payload}')

    if not hasattr(context, 'files'):
        context.files = []
    elif context.files:
        logger.debug(f'Files: {context.files}')

    if hasattr(context, 'allow_redirects'):
        logger.debug(f'Allow redirects is set to "{context.allow_redirects}".')
    else:
        context.allow_redirects = True

    if hasattr(context, 'headers') and context.headers:
        logger.debug(f'Headers: {context.headers}')

    logger.debug(f'Endpoint: {context.endpoint}')


def dump_payload(context):
    """This function properly dumps the payload if it is not in url-encoded format.

    Args:
        context (Context): The default object is available throughout Behave framework.
    """

    if str(context.payload).startswith('{') and str(context.payload).endswith('}'):
        context.payload = json.dumps(context.payload)
    else:
        # No need to dump the payload if it is in url-encoded format. i.e. 'username=abc&password=xyz'
        pass


def prepare_request(context, _request_type='GET'):
    """This function validates that the required attributes are present in the context before making a request.

    Args:
        context (Context): The default object is available throughout Behave framework.
        _request_type (str): CRUD operation being used while making the request.
    """

    validate_endpoint(context, _request_type)
    generate_request_logs(context, _request_type)
    dump_payload(context)


def send_request_with_headers(context, _request_type):

    if hasattr(context, 'files') and context.files:
        context.response = requests.request(_request_type, context.endpoint, headers=context.headers,
                                            json=context.payload, files=context.files,
                                            allow_redirects=context.allow_redirects)
    else:
        context.response = requests.request(_request_type, context.endpoint, headers=context.headers,
                                            data=context.payload, allow_redirects=context.allow_redirects)


def send_request_without_headers(context, _request_type):

    if hasattr(context, 'files') and context.files:
        context.response = requests.request(_request_type, context.endpoint,
                                            json=context.payload, files=context.files,
                                            allow_redirects=context.allow_redirects)
    else:
        context.response = requests.request(_request_type, context.endpoint, data=context.payload,
                                            allow_redirects=context.allow_redirects)


def send_request(context, _request_type='GET'):
    """This function uses the local server base urls to make the request without the need to include certificates.

    Args:
        context (Context): The default object is available throughout Behave framework.
        _request_type (str): CRUD operation being used while making the request.
    """

    if hasattr(context, 'headers') and context.headers:
        send_request_with_headers(context, _request_type)
    else:
        send_request_without_headers(context, _request_type)

    # Resetting the context attributes to default values after making the request.
    context.payload = {}
    context.files = []


def validate_request(context, expected_code):
    """This function validates that the curtain conditions meet after making a request.

    Args:
        context (Context): The default object is available throughout Behave framework.
        expected_code (int): Expected status code after making a request.
    """

    if 'Content-Type' in context.response.headers:

        if context.response.headers["Content-Type"] == 'application/json':
            logger.debug(f'Response: {context.response.text}')
        else:
            # logger.debug(f'Response: {context.response.text}')
            logger.debug(f'Response type is: {context.response.headers["Content-Type"]}')

    elif not context.response.text:
        logger.debug('Response text is empty.')
    else:
        logger.debug(f'Unknown Response: {context.response.text}')

    if expected_code:
        actual_code = context.response.status_code
        assert_text(str(expected_code), actual_code, _text_to_assert="Status Code")


def make_request(context, _request_type='GET', _status_code=0):
    """This function makes a request to the live server with the provided CRUD operation.

    Args:
        context (Context): The default object is available throughout Behave framework.
        _request_type (str): CRUD operation being used while making the request.
        _status_code (int): Expected status code after making a request.
    """

    prepare_request(context, _request_type)

    send_request(context, _request_type)

    validate_request(context, _status_code)


# Frontend Testing utils

def get_browser(context):
    """This function returns an instance of the Web Driver after initial configuration.

    Args:
        context (Context): The default object is available throughout Behave framework.

    Raises:
        AssertionError: If desired browser is not configured then raises this specific exception.

    Returns:
        browser (WebDriver): It returns Chrome browser instance to control automatically.
    """

    desired_browser = get_value_from_ini(context, ConfigVars.browser.value)

    if desired_browser == 'chrome':
        custom_options = chrome_options.Options()

        prefs = {'download.default_directory': '/downloads'}
        custom_options.add_experimental_option("prefs", prefs)

        if context.test_headless:
            custom_options.headless = True
            custom_options.add_argument('--no-sandbox')
            custom_options.add_argument('--disable-dev-shm-usage')

        browser = webdriver.Chrome(chrome_options=custom_options)
        browser.set_window_size(1920, 1080)

        browser_name = browser.capabilities["browserName"]
        browser_version = browser.capabilities["browserVersion"]

        logger.debug('--------\nINFO:')
        logger.debug(f'Testing on {browser_name} version {browser_version}\n--------')
        logger.debug(f'Headless mode is turned {"ON" if context.test_headless else "OFF"}.')

        return browser
    else:
        raise AssertionError(f'The settings for browser {desired_browser} are not configured.')


def open_page(context, url, _elem_xpath='', _elem_index=0, _error_msg='', _driver_wait_time=-1):
    """This function waits until the specified element become clickable on the Web Page using Text.

    Args:
        context (Context): The default object is available throughout Behave framework.
        url (str): The visible text of the elements that we are looking for.
        _elem_xpath (str): The XPath of the element that we are looking for.
        _elem_index (int): In the case of multiple elements, one can specify one of the indexes from the list.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if unable to find the presence of any elements.
                        2) if the provided index is not in the list.
    """

    base_url = get_value_from_ini(context, ConfigVars.server.value)
    full_url = base_url + url

    logger.debug(f'Loading Page: "{full_url}"')
    context.browser.get(full_url)

    if _elem_xpath:

        if not _error_msg:
            _error_msg = f'Timed out waiting for page to load element with xpath: "{_elem_xpath}".'

        wait_for_elem(context, _elem_xpath, _elem_index, _error_msg, _driver_wait_time)


# Following are the Functions to interact with selenium elements.


def wait_for_elems(context, elems_xpath, _error_msg='', _driver_wait_time=-1):
    """This function waits until the presence of the specified element is located on the Web Page using XPath.

    Args:
        context (Context): The default object is available throughout Behave framework.
        elems_xpath (str): The XPath of the elements that we are looking for.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.

    Raises:
        AssertionError: If unable to find the presence of any elements using text then raises this specific exception.

    Returns:
        WebDriverElement (list): It returns a list of WebDriverElements after searching the Web Page.
    """

    if not _error_msg:
        _error_msg = f'Elements with xpath "{elems_xpath}" did not appear on the web page.'

    if _driver_wait_time <= 0:
        _driver_wait_time = int(get_value_from_ini(context, ConfigVars.driver_wait_time.value))

    try:
        elems = WebDriverWait(context.browser, _driver_wait_time).until(
                    EC.presence_of_all_elements_located((By.XPATH, elems_xpath)))
    except exceptions.TimeoutException:
        raise AssertionError(_error_msg)

    logger.debug(f'The number of Elements found on the web page: {len(elems)}')

    return elems


def wait_for_elem(context, elem_xpath, _elem_index=0, _error_msg='', _driver_wait_time=-1):
    """This function waits until the presence of the specified element is located on the Web Page using XPath.

    Args:
        context (Context): The default object is available throughout Behave framework.
        elem_xpath (str): The XPath of the element that we are looking for.
        _elem_index (int): In the case of multiple elements, one can specify one of the indexes from the list.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if unable to find the presence of any elements.
                        2) if the provided index is not in the list.

    Returns:
        elem (WebDriverElement): It returns the WebDriverElement from either the default index or the specified index.
    """

    elems = wait_for_elems(context, elem_xpath, _error_msg, _driver_wait_time)

    if _elem_index >= len(elems):
        _error_msg = f'Requested Index: "{_elem_index}" | Actual Count: "{len(elems)}" | ' \
                     f'Element Index should be less than actual elements count.'

        raise AssertionError(_error_msg)

    elem = elems[_elem_index]

    if elem.is_displayed():
        text = elem.text.replace('\n', '<br>').replace('\r', '').strip()
    else:
        text = ''

    logger.debug(f'Element found | Text: "{text}" | XPath: "{elem_xpath}"')

    return elem


def wait_for_elems_by_text(context, elems_text, _exact_text=False, _error_msg='', _driver_wait_time=-1):
    """This function waits until the presence of the specified element is located on the Web Page using Text.

    Args:
        context (Context): The default object is available throughout Behave framework.
        elems_text (str): The visible text of the elements that we are looking for.
        _exact_text (bool): This flag helps to decide whether an element has the exact text or contains the text.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.

    Raises:
        AssertionError: If unable to find the presence of any elements using text then raises this specific exception.

    Returns:
        WebDriverElement (list): It returns a list of WebDriverElements after searching the Web Page.
    """

    if not _error_msg:
        _error_msg = f'Elements with text "{elems_text}" did not appear on the web page.'

    if _driver_wait_time <= 0:
        _driver_wait_time = int(get_value_from_ini(context, ConfigVars.driver_wait_time.value))

    if _exact_text:
        locate_elem_by_xpath = constants.FrontEndXpath.locate_elem_by_exact_text_xpath.value.replace(
            '"', "'").format(elems_text)
    else:
        locate_elem_by_xpath = constants.FrontEndXpath.locate_elem_by_having_text_xpath.value.replace(
            '"', "'").format(elems_text)

    elems = wait_for_elems(context, locate_elem_by_xpath, _error_msg, _driver_wait_time)

    logger.debug(f'The number of Elements found on the web page: {len(elems)}')

    return elems


def wait_for_elem_by_text(context, elem_text, _elem_index=0, _exact_text=False, _error_msg='', _driver_wait_time=-1):
    """This function waits until the presence of the specified element is located on the Web Page using Text.

    Args:
        context (Context): The default object is available throughout Behave framework.
        elem_text (str): The visible text of the elements that we are looking for.
        _elem_index (int): In the case of multiple elements, one can specify one of the indexes from the list.
        _exact_text (bool): This flag helps to decide whether an element has the exact text or contains the text.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if unable to find the presence of any elements.
                        2) if the provided index is not in the list.

    Returns:
        elem (WebDriverElement): It returns the WebDriverElement from either the default index or the specified index.
    """

    elems = wait_for_elems_by_text(context, elem_text, _exact_text, _error_msg, _driver_wait_time)

    if _elem_index >= len(elems):
        _error_msg = f'Requested Index: "{_elem_index}" | Actual Count: "{len(elems)}" | ' \
                     f'Element Index should be less than actual elements count.'

        raise AssertionError(_error_msg)

    exact_text_index = -1

    for index in range(len(elems)):
        elem = elems[index]

        if elem_text.lower().strip() == elem.text.lower().strip():
            exact_text_index = index

    # In case of multiple elements having same text, AI based approach to choose element with exact text.
    if exact_text_index != -1 and _elem_index == 0:
        elem = elems[exact_text_index]
    else:
        elem = elems[_elem_index]

    if elem.is_displayed():
        text = elem.text.replace('\n', '<br>').replace('\r', '').strip()
    else:
        text = ''

    logger.debug(f'Located Element with Text: "{text}".')

    return elem


def locate_elems(context, elems_xpath, _error_msg='', _driver_wait_time=-1):
    """This function waits until the specified elements becomes visible on the Web Page using XPath.

    Args:
        context (Context): The default object is available throughout Behave framework.
        elems_xpath (str): The XPath of the elements that we are looking for.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.

    Raises:
        AssertionError: If no elements are visible using XPath then raises this specific exception.

    Returns:
        WebDriverElement (list): It returns a list of WebDriverElements after searching the Web Page.
    """

    if not _error_msg:
        _error_msg = f'Could not locate elements with xpath "{elems_xpath}".'

    if _driver_wait_time <= 0:
        _driver_wait_time = int(get_value_from_ini(context, ConfigVars.driver_wait_time.value))

    try:
        elems = WebDriverWait(context.browser, _driver_wait_time).until(
                    EC.visibility_of_all_elements_located((By.XPATH, elems_xpath)))
    except exceptions.TimeoutException:
        raise AssertionError(_error_msg)

    logger.debug(f'The number of Elements located: {len(elems)}')

    return elems


def locate_elem(context, elem_xpath, _elem_index=0, _error_msg='', _driver_wait_time=-1):
    """This function waits until the specified element become visible on the Web Page using XPath.

    Args:
        context (Context): The default object is available throughout Behave framework.
        elem_xpath (str): The XPath of the element that we are looking for.
        _elem_index (int): In the case of multiple elements, one can specify one of the indexes from the list.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if no elements are visible using XPath.
                        2) if the provided index is not in the list.

    Returns:
        elem (WebDriverElement): It returns the WebDriverElement from either the default index or the specified index.
    """

    elems = locate_elems(context, elem_xpath, _error_msg, _driver_wait_time)

    if _elem_index >= len(elems):
        _error_msg = f'Requested Index: "{_elem_index}" | Actual Count: "{len(elems)}" | ' \
                     f'Element Index should be less than actual elements count.'

        raise AssertionError(_error_msg)

    elem = elems[_elem_index]

    if elem.is_displayed():
        text = elem.text.replace('\n', '<br>').replace('\r', '').strip()
    else:
        text = ''

    logger.debug(f'Element Found | Text: "{text}" | xpath: "{elem_xpath}"')

    return elem


def locate_elems_by_text(context, elems_text, _exact_text=False, _error_msg='', _driver_wait_time=-1):
    """This function waits until the specified elements becomes visible on the Web Page using Text.

    Args:
        context (Context): The default object is available throughout Behave framework.
        elems_text (str): The visible text of the elements that we are looking for.
        _exact_text (bool): This flag helps to decide whether an element has the exact text or contains the text.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.

    Raises:
        AssertionError: If no elements are visible using Text then raises this specific exception.

    Returns:
        WebDriverElement (list): It returns a list of WebDriverElements after searching the Web Page.
    """

    if not _error_msg:
        _error_msg = f'Could not locate elements with text "{elems_text}".'

    if _driver_wait_time <= 0:
        _driver_wait_time = int(get_value_from_ini(context, ConfigVars.driver_wait_time.value))

    if _exact_text:
        locate_elem_by_xpath = constants.FrontEndXpath.locate_elem_by_exact_text_xpath.value.replace(
            '"', "'").format(elems_text)
    else:
        locate_elem_by_xpath = constants.FrontEndXpath.locate_elem_by_having_text_xpath.value.replace(
            '"', "'").format(elems_text)

    elems = locate_elems(context, locate_elem_by_xpath, _error_msg, _driver_wait_time)

    logger.debug(f'The number of Elements located: {len(elems)}')

    return elems


def locate_elem_by_text(context, elem_text, _elem_index=0, _exact_text=False, _error_msg='', _driver_wait_time=-1):
    """This function waits until the specified element become visible on the Web Page using Text.

    Args:
        context (Context): The default object is available throughout Behave framework.
        elem_text (str): The visible text of the elements that we are looking for.
        _elem_index (int): In the case of multiple elements, one can specify one of the indexes from the list.
        _exact_text (bool): This flag helps to decide whether an element has the exact text or contains the text.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if no elements are visible using Text.
                        2) if the provided index is not in the list.

    Returns:
        elem (WebDriverElement): It returns the WebDriverElement from either the default index or the specified index.
    """

    elems = locate_elems_by_text(context, elem_text, _exact_text, _error_msg, _driver_wait_time)

    if _elem_index >= len(elems):
        err_msg = f'Requested Index: "{_elem_index}" | Actual Count: "{len(elems)}" | ' \
                  f'Element Index should be less than actual elements count.'

        raise AssertionError(err_msg)

    exact_text_index = -1

    for index in range(len(elems)):
        elem = elems[index]

        if elem_text.lower().strip() == elem.text.lower().strip():
            exact_text_index = index

    # In case of multiple elements having same text, AI based approach to choose element with exact text.
    if exact_text_index != -1 and _elem_index == 0:
        elem = elems[exact_text_index]
    else:
        elem = elems[_elem_index]

    if elem.is_displayed():
        text = elem.text.replace('\n', '<br>').replace('\r', '').strip()
    else:
        text = ''

    logger.debug(f'The element located using Text: "{text}"')

    return elem


def clickable_elem(context, elem_xpath, _error_msg='', _driver_wait_time=-1):
    """This function waits until the specified element become clickable on the Web Page using XPath.

    Args:
        context (Context): The default object is available throughout Behave framework.
        elem_xpath (str): The XPath of the element that we are looking for.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.

    Raises:
        AssertionError: If unable to find the specified clickable element then raises this specific exception.

    Returns:
        elem (WebDriverElement): It returns the WebDriverElement from either the default index or the specified index.
    """

    if not _error_msg:
        _error_msg = f'Element with xpath "{elem_xpath}" is not clickable.'

    if _driver_wait_time <= 0:
        _driver_wait_time = int(get_value_from_ini(context, ConfigVars.driver_wait_time.value))

    try:
        elem = WebDriverWait(context.browser, _driver_wait_time).until(
                    EC.element_to_be_clickable((By.XPATH, elem_xpath)))
    except exceptions.TimeoutException:
        raise AssertionError(_error_msg)

    return elem


def clickable_elem_by_text(context, elem_text, _elem_index=0, _exact_text=False, _error_msg='', _driver_wait_time=-1):
    """This function waits until the specified element become clickable on the Web Page using Text.

    Args:
        context (Context): The default object is available throughout Behave framework.
        elem_text (str): The visible text of the elements that we are looking for.
        _elem_index (int): In the case of multiple elements, one can specify one of the indexes from the list.
        _exact_text (bool): This flag helps to decide whether an element has the exact text or contains the text.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if unable to find the specified clickable element.
                        2) if the provided index is not in the list.

    Returns:
        elem (WebDriverElement): It returns the WebDriverElement from either the default index or the specified index.
    """

    if not _error_msg:
        _error_msg = f'Element with text "{elem_text}" is not clickable.'

    if _driver_wait_time <= 0:
        _driver_wait_time = int(get_value_from_ini(context, ConfigVars.driver_wait_time.value))

    if _exact_text:
        locate_elem_by_xpath = constants.FrontEndXpath.locate_elem_by_exact_text_xpath.value.replace(
            '"', "'").format(elem_text)
    else:
        locate_elem_by_xpath = constants.FrontEndXpath.locate_elem_by_having_text_xpath.value.replace(
            '"', "'").format(elem_text)

    try:
        elem = WebDriverWait(context.browser, _driver_wait_time).until(
                    EC.element_to_be_clickable((By.XPATH, locate_elem_by_xpath)))
    except exceptions.TimeoutException:
        raise AssertionError(_error_msg)

    return elem


def click_elem(context, elem_xpath, _elem_index=0, _error_msg='', _driver_wait_time=-1, _click_sleep=-1,
               _locate_by='presence', _click_by='driver'):
    """This function clicks the specified element on the Web Page using XPath.

    Args:
        context (Context): The default object is available throughout Behave framework.
        elem_xpath (str): The XPath of the element that we are looking for.
        _elem_index (int): In the case of multiple elements, one can specify one of the indexes from the list.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.
        _click_sleep (int): After the element got clicked, The time in seconds to delay for the UI to update.

        _locate_by (str): The option being used to locate the element to click. Available options are:
            1. presence (default) -> The script will use wait_for_elem function to locate element.
            2. clickable -> The script will use clickable_elem function to locate element.
            3. visible -> The script will use locate_elem function to locate element.

        _click_by (str): The approach used to click an element.
            1. driver (default) -> The script will use the WebDriverElement click method to operate.
            2. script -> The script will use the javascript click method to operate.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if unable to find the specified clickable element.
                        2) if the provided index is not in the list.
    """

    if _click_sleep <= 0:
        _click_sleep = int(get_value_from_ini(context, ConfigVars.stable_elems_sleep.value))

    if _locate_by == 'clickable':
        elem = clickable_elem(context, elem_xpath, _error_msg, _driver_wait_time)
    elif _locate_by == 'visible':
        elem = locate_elem(context, elem_xpath, _elem_index, _error_msg, _driver_wait_time)
    else:
        elem = wait_for_elem(context, elem_xpath, _elem_index, _error_msg, _driver_wait_time)

    logger.debug(f'Clicked element having Text: "{elem.text}".')

    if _click_by.lower() == 'script':
        context.browser.execute_script('arguments[0].click();', elem)
    else:
        elem.click()

    sleep(_click_sleep)


def click_elem_by_text(context, elem_text, _elem_index=0, _exact_text=False, _error_msg='', _driver_wait_time=-1,
                       _click_sleep=-1, _locate_by='presence', _click_by='driver'):
    """This function clicks the specified element on the Web Page using Text.

    Args:
        context (Context): The default object is available throughout Behave framework.
        elem_text (str): The visible text of the elements that we are looking for.
        _elem_index (int): In the case of multiple elements, one can specify one of the indexes from the list.
        _exact_text (bool): This flag helps to decide whether an element has the exact text or contains the text.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.
        _click_sleep (int): After the element got clicked, The time in seconds to delay for the UI to update.

        _locate_by (str): The option being used to locate the element to click. Available options are:
            1. presence (default) -> The script will use wait_for_elem function to locate element.
            2. clickable -> The script will use clickable_elem function to locate element.
            3. visible -> The script will use locate_elem function to locate element.

        _click_by (str): The approach used to click an element.
            1. driver (default) -> The script will use the WebDriverElement click method to operate.
            2. script -> The script will use the javascript click method to operate.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if unable to find the specified clickable element.
                        2) if the provided index is not in the list.
    """

    if _click_sleep <= 0:
        _click_sleep = int(get_value_from_ini(context, ConfigVars.stable_elems_sleep.value))

    if _locate_by == 'clickable':
        elem = clickable_elem_by_text(context, elem_text, _elem_index, _exact_text, _error_msg, _driver_wait_time)
    elif _locate_by == 'visible':
        elem = locate_elem_by_text(context, elem_text, _elem_index, _exact_text, _error_msg, _driver_wait_time)
    else:
        elem = wait_for_elem_by_text(context, elem_text, _elem_index, _exact_text, _error_msg, _driver_wait_time)

    logger.debug(f'Clicked element having Text: "{elem.text}".')

    if _click_by.lower() == 'script':
        context.browser.execute_script('arguments[0].click();', elem)
    else:
        elem.click()

    sleep(_click_sleep)


def send_keys_to_elem(context, keys, elem_xpath, _elem_index=0, _error_msg='', _driver_wait_time=-1, _click_sleep=-1,
                      _clear_keys=False, _locate_by='presence'):
    """This function writes specified text in the editable field present on the Web Page using XPath.

    Args:
        context (Context): The default object is available throughout Behave framework.
        keys (str): The text to enter into the editable field.
        elem_xpath (str): The XPath of the element that we are looking for.
        _elem_index (int): In the case of multiple elements, one can specify one of the indexes from the list.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.
        _click_sleep (int): After the element got clicked, The time in seconds to delay for the UI to update.
        _clear_keys (bool): It helps to decide whether to remove the existing text from the field.

        _locate_by (str): The option being used to locate the element to click. Available options are:
            1. presence (default) -> The script will use wait_for_elem function to locate element.
            2. visible -> The script will use locate_elem function to locate element.
            3. clickable -> The script will use clickable_elem function to locate element.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if unable to find an editable field
                        2) if the provided index is not in the list.
    """

    if _click_sleep <= 0:
        _click_sleep = int(get_value_from_ini(context, ConfigVars.stable_elems_sleep.value))

    if _locate_by == 'clickable':
        elem = clickable_elem(context, elem_xpath, _error_msg, _driver_wait_time)
    elif _locate_by == 'visible':
        elem = locate_elem(context, elem_xpath, _elem_index, _error_msg, _driver_wait_time)
    else:
        elem = wait_for_elem(context, elem_xpath, _elem_index, _error_msg, _driver_wait_time)

    logger.debug(f'Send Keys to element | Keys: "{keys}" | Xpath: "{elem_xpath}"')

    if _clear_keys:
        elem.clear()

    elem.send_keys(keys)

    sleep(_click_sleep)


def send_keys_to_elem_by_text(context, keys, elem_text, _elem_index=0, _exact_text=False, _error_msg='',
                              _driver_wait_time=-1, _click_sleep=-1, _clear_keys=False, _locate_by='presence'):
    """This function writes specified text in the editable field present on the Web Page using Text.

    Args:
        context (Context): The default object is available throughout Behave framework.
        keys (str): The text to enter into the editable field.
        elem_text (str): The visible text of the elements that we are looking for.
        _elem_index (int): In the case of multiple elements, one can specify one of the indexes from the list.
        _exact_text (bool): This flag helps to decide whether an element has the exact text or contains the text.
        _error_msg (str): The error message to raise if the web elements are missing.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.
        _click_sleep (int): After the element got clicked, The time in seconds to delay for the UI to update.
        _clear_keys (bool): It helps to decide whether to remove the existing text from the field.

        _locate_by (str): The option being used to locate the element to click. Available options are:
            1. presence (default) -> The script will use wait_for_elem function to locate element.
            2. visible -> The script will use locate_elem function to locate element.
            3. clickable -> The script will use clickable_elem function to locate element.

    Raises:
        AssertionError: An exception arises if any of the following situations occur:
                        1) if unable to find an editable field.
                        2) if the provided index is not in the list.
    """

    if _click_sleep <= 0:
        _click_sleep = int(get_value_from_ini(context, ConfigVars.stable_elems_sleep.value))

    if _locate_by == 'clickable':
        elem = clickable_elem_by_text(context, elem_text, _elem_index, _exact_text, _error_msg, _driver_wait_time)
    elif _locate_by == 'visible':
        elem = locate_elem_by_text(context, elem_text, _elem_index, _exact_text, _error_msg, _driver_wait_time)
    else:
        elem = wait_for_elem_by_text(context, elem_text, _elem_index, _exact_text, _error_msg, _driver_wait_time)

    logger.debug(f'Send Keys to element | Keys: "{keys}" | Text: "{elem_text}"')

    if _clear_keys:
        elem.clear()

    elem.send_keys(keys)

    sleep(_click_sleep)


def scroll_down_to_bottom_of_page(context, _click_sleep=-1):
    """This function scrolls down to the bottem of the page.

    Args:
        context (Context): The default object is available throughout Behave framework.
        _click_sleep (int): After the element got clicked, The time in seconds to delay for the UI to update.
    """

    if _click_sleep <= 0:
        _click_sleep = int(get_value_from_ini(context, ConfigVars.stable_elems_sleep.value))

    last_height = context.browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        context.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        sleep(_click_sleep)

        # Calculate new scroll height and compare with last scroll height
        new_height = context.browser.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height


def scroll_to_elem(context, elem_xpath, _driver_wait_time=-1, _click_sleep=-1):
    """This function scrolls down to the specific element present on the page.

    Args:
        context (Context): The default object is available throughout Behave framework.
        elem_xpath (str): The XPath of the element that we are looking for.
        _driver_wait_time (int): WebDriver waits for a specified number of seconds at max while looking for the element.
        _click_sleep (int): After the element got clicked, The time in seconds to delay for the UI to update.
    """

    if _click_sleep <= 0:
        _click_sleep = int(get_value_from_ini(context, ConfigVars.stable_elems_sleep.value))

    elem = wait_for_elem(context, elem_xpath, _driver_wait_time=_driver_wait_time)

    if elem:
        context.browser.execute_script('arguments[0].scrollIntoView();', elem)

        sleep(_click_sleep)

        return elem
    else:
        return False
