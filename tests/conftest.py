# These lines will add the parent directory of this file working directory to the
# python path, This helps with Import issues and relative paths.  We could do this
# better though!
import sys
import os
sys.path.append(os.path.split(os.path.dirname(__file__))[0])

import pytest
import arrow
import time
from py.xml import html
from src.RequestSession.SimpleRequests import BasicRequestSession


##################################################################################
# FIXTURES
##################################################################################
@pytest.fixture(scope="session")
def basic_api():
    return BasicRequestSession()
##################################################################################
# End FIXTURES
##################################################################################


##################################################################################
# HOOKS
##################################################################################
def pytest_configure(config):
    '''
    Configuring py.test, add items here for ini, help and things like that

    called after command line options have been parsed
    and all plugins and initial conftest files been loaded.
    This hook is called for every plugin.
    '''

    # Change the Name of the HTML Report
    if hasattr(config.option, 'htmlpath') and config.option.htmlpath is not None:
        if "{date}" in config.option.htmlpath:
            config.option.htmlpath = config.option.htmlpath.format(
                date=time.strftime("%Y-%m-%dT%H-%M"))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    ''' This Hook Controls what goes into the report
    '''

    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # Add __doc__ string to report
    rep.description = str(item.function.__doc__)


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    '''Adding columns to HTML Report, Description and Time Executed
    '''
    cells.insert(2, html.th('Description'))
    cells.insert(1, html.th('Local Time Executed', class_='sortable time', col='time'))


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    '''Adding values to columns of HTML Report, Description and Time Executed
    '''
    if hasattr(report, "description"):
        cells.insert(2, html.td(report.description))
    else:
        cells.insert(2, html.td("None"))
    cells.insert(1, html.td(arrow.now(), class_='col-time'))
##################################################################################
# END HOOKS
##################################################################################
