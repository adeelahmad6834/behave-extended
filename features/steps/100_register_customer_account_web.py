import logging

from behave import given, when, then

from steps import utils, constants

logger = logging.getLogger('myLogger')


# Scenario 1
@given(u'the user is on the home page of Parabank.')
def step_impl(context):
    homepage_url = constants.FrontEndURL.homepage_url.value
    utils.open_page(context, homepage_url)


@when(u'the user clicks on the "{btn_name}" button.')
def step_impl(context, btn_name):
    utils.click_elem_by_text(context, btn_name)


@then(u'the user is redirected to "{page_name}" page.')
def step_impl(context, page_name):
    # This step is just for better readability. Next step will verify that user is on desired screen.
    pass


@then(u'the user can see a message "{msg}".')
def step_impl(context, msg):
    utils.locate_elem_by_text(context, msg)


# Scenario 2
@given(u'the user is already on the registration page of Parabank.')
def step_impl(context):
    context.execute_steps('''
        Given the user is on the home page of Parabank.
        When the user clicks on the "Register" button.
        Then the user is redirected to "Registration" page.
        And the user can see a message "Signing up is easy!".
    ''')


@when(u'the user enters "{field_value}" in the "{field_name}" field.')
def step_impl(context, field_value, field_name):
    specific_field_xpath = constants.FrontEndXpath.field_xpath.value.format(field_name)
    utils.send_keys_to_elem(context, field_value, specific_field_xpath)


@when(u'the user submits the form by clicking on the Register button.')
def step_impl(context):
    registration_btn_xpath = constants.FrontEndXpath.registration_btn_xpath.value
    utils.click_elem(context, registration_btn_xpath)
