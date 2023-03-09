import copy
import logging

from behave import given, when, then

from steps import utils, constants

logger = logging.getLogger('myLogger')


# Scenario 1
@given(u'the user has a public endpoint to visit homepage of parabank.')
def step_impl(context):
    context.endpoint = constants.ApiEndpoint.homepage_endpoint.value


@when(u'the user makes the "{request_type}" request to the endpoint.')
def step_impl(context, request_type):
    utils.make_request(context, _request_type=request_type)


@then(u'the request passes with the status code "{expected_code}".')
def step_impl(context, expected_code):
    actual_code = context.response.status_code
    utils.assert_text(expected_code, actual_code, _text_to_assert='Status Code')


@then(u'the user receives a "{session_key}" as a token.')
def step_impl(context, session_key):
    context.session_id = context.response.cookies.get(session_key)
    logger.debug(f'Received "{session_key}" is "{context.session_id}".')


# Scenario 2
@given(u'the user has already visited the homepage of parabank.')
def step_impl(context):
    context.execute_steps('''
        Given the user has a public endpoint to visit homepage of parabank.
        When the user makes the "GET" request to the endpoint.
        Then the request passes with the status code "200".
        And the user receives a "JSESSIONID" as a token.
    ''')


@given(u'the user has "{status}" JSESSIONID as a token.')
def step_impl(context, status):

    if status == 'a valid':
        utils.has_context_attr(context, 'session_id')   # Ensuring that Context variable contains JSESSIONID value.
    else:
        context.session_id = 'invalid_id'


@given(u'the user has a public endpoint to visit the registration page of Parabank.')
def step_impl(context):
    context.endpoint = constants.ApiEndpoint.register_customer_with_session_id_endpoint.value.format(context.session_id)


# Scenario 4
@given(u'the user has already visited the registration page of parabank with "{status}" JSESSIONID.')
def step_impl(context, status):
    context.execute_steps(f'''
        Given the user has already visited the homepage of parabank.
        And the user has "{status}" JSESSIONID as a token.
        And the user has a public endpoint to visit the registration page of Parabank.
        When the user makes the "GET" request to the endpoint.
        Then the request passes with the status code "200".
    ''')


@given(u'the user has a public endpoint to register a customer account.')
def step_impl(context):
    context.endpoint = constants.ApiEndpoint.register_customer_endpoint.value


@given(u'the user has a payload for account registration.')
def step_impl(context):
    context.headers = {"Content-Type": "application/x-www-form-urlencoded",
                       "Cookie": f"JSESSIONID={context.session_id}"}

    if not hasattr(context, 'payload'):
        context.payload = copy.deepcopy(constants.ApiConstant.register_customer_payload.value)

    context.registration_payload = copy.deepcopy(context.payload)    # Storing as a reference for later steps.


@then(u'the customer account is registered successfully.')
def step_impl(context):
    # This step is just for better readability.
    pass


# Scenario 5
@then(u'the request fails with the status code "{expected_code}".')
def step_impl(context, expected_code):
    actual_code = context.response.status_code
    utils.assert_text(expected_code, actual_code, _text_to_assert='Status Code')


@then(u'the customer account is not registered.')
def step_impl(context):
    # This step is just for better readability.
    pass
