import logging

from behave import fixture

from steps import utils

logger = logging.getLogger('myLogger')


@fixture
def test_in_browser(context):
    """This function provides a Chrome browser instance to perform automated actions.

    Args:
        context (Context): The default object is available throughout behave framework.

    Yields:
        browser (ChromeDriver): The Chrome driver instance.
    """

    logger.debug('--- Initiating Fixture to create a browser instance for Web Testing. ---')

    # Quit previous browser instance before we launch a new one to avoid low memory crashes.
    if hasattr(context, 'browser'):
        context.browser.quit()

    browser = utils.get_browser(context)
    context.browser = browser

    logger.debug('--- A browser instance for Web Testing has been created. ---')

    yield browser

    browser.quit()

    logger.debug('--- Quiting the browser instance after Web Testing. ---')


@fixture
def create_account(context):
    """This function creates a customer account for API testing.

    Args:
        context (Context): The default object is available throughout behave framework.
    """

    logger.debug('--- Initiating Fixture to create a Customer Account. ---')

    context.execute_steps('''
        Given the user has already visited the registration page of parabank with "a valid" JSESSIONID.
        And the user has a public endpoint to register a customer account.
        And the user has a payload for account registration.
        When the user makes the "POST" request to the endpoint.
        Then the request passes with the status code "200".
        And the customer account is registered successfully.
    ''')

    logger.debug(f'--- A Customer Account is created. ---')
