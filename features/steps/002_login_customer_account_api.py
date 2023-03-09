import logging
from urllib.parse import quote

from behave import given, then

from steps import utils, constants

logger = logging.getLogger('myLogger')


# Scenario 1
@given(u'the user has a public endpoint to login into the customer account.')
def step_impl(context):
    context.endpoint = constants.ApiEndpoint.login_endpoint.value


@given(u'the user has "{status}" credentials to login into the customer account.')
def step_impl(context, status):
    context.allow_redirects = False
    context.headers = {"Content-Type": "application/x-www-form-urlencoded",
                       "Cookie": f"JSESSIONID={context.session_id}"}

    if status == 'valid':
        utils.has_context_attr(context, 'registration_payload')

        username = context.registration_payload['customer.username']
        password = context.registration_payload['customer.password']
    else:
        username = password = 'invalid'

    context.payload = f'username={quote(username)}&password={quote(password)}'


@then(u'the user can see the message "{expected_text}".')
def step_impl(context, expected_text):
    actual_text = context.response.text
    utils.assert_text_contains(expected_text, actual_text, 'Response Text')


# Scenario 3
@given(u'the user has already logged into the customer account using "valid" credentials.')
def step_impl(context):
    context.execute_steps('''
        Given the user has a public endpoint to login into the customer account.
        And the user has "valid" credentials to login into the customer account.
        When the user makes the "POST" request to the endpoint.
        Then the request passes with the status code "302".
    ''')


@given(u'the user has a private endpoint to visit the dashboard overview of parabank.')
def step_step(context):
    context.endpoint = constants.ApiEndpoint.overview_endpoint.value


# Scenario 4
@given(u'the user has a private endpoint to logout of the customer account of parabank.')
def step_impl(context):
    context.endpoint = constants.ApiEndpoint.login_endpoint.value
