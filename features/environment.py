import os
import logging
import logging.config

from behave import use_fixture
from selenium.webdriver.common.by import By
from xvfbwrapper import Xvfb

from steps import fixtures, constants

logger = logging.getLogger('myLogger')


def before_all(context):

    if not context.config.log_capture:
        logging.config.fileConfig('behave_logging.ini')

    if context.config.userdata.get('headless').lower() == 'true':
        context.virtual_display = Xvfb()
        context.virtual_display.start()
        logger.debug('--- Initiated Virtual Display ---')
        context.test_headless = True
    else:
        # Headless testing enabled by passing option -D headless
        context.test_headless = False


def before_scenario(context, scenario):
    logger.debug('--------\n')
    logger.debug(f'Scenario: {scenario.name}')

    if 'web' in (scenario.feature.tags + scenario.tags):
        # Web based scenarios will be tested in the browser.
        use_fixture(fixtures.test_in_browser, context)


def after_step(context, step):
    # Save Screenshots if scenario fails until or unless not running in the pipelines.
    pipeline_stage = os.getenv('CI_JOB_STAGE', None)

    if pipeline_stage is None:

        if step.status == 'failed' and hasattr(context, 'browser'):
            screenshots_dir_path = str(constants.BackOfficeConstant.screenshots_dir_path.value)

            if not os.path.isdir(screenshots_dir_path):
                os.mkdir(screenshots_dir_path)

            screenshot_file_path = f'{screenshots_dir_path + context.scenario.name}.png'
            context.browser.find_element(By.CSS_SELECTOR, 'body').screenshot(screenshot_file_path)


def before_tag(context, tag):

    if tag == 'create_account':
        use_fixture(fixtures.create_account, context)


def after_tag(context, tag):
    # tags mentioned here will run after the scenario is executed.
    pass


def after_all(context):

    if context.config.userdata.get('headless').lower() == 'true':
        logger.debug('< Closed the virtual display.')
        context.virtual_display.stop()
