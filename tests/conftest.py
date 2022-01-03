import logging
import pytest


@pytest.fixture(scope='function', autouse=True)
def junit_tag(request, record_xml_attribute):
    """Apply Jira id to testcase JUnit XML report"""
    for marker in request.node.own_markers:
        if marker.name == 'jira':
            jira_ids = marker.args
    record_xml_attribute('jira', ','.join(jira_ids))


def pytest_bdd_apply_tag(tag, function):
    """Customize how tags are converted to pytest marks"""
    if tag == 'todo':
        marker = pytest.mark.skip(reason="Not implemented yet")
        marker(function)
        return True
    elif 'jira' in tag:
        marker = pytest.mark.jira.with_args(*tag[5:-1].split(','))
        marker(function)
        return True
    # Fall back to pytest-bdd's default behavior
    return None


def pytest_bdd_before_step_call(request, step, step_func, step_func_args):
    """Called before step function is executed with evaluated arguments"""
    logging.info(f'\t{step.keyword} {step.name}')
    logging.debug(f'\t\t{step_func}_({", ".join(str(value) for value in step_func_args.values())})')


def pytest_bdd_step_error(request, exception):
    """Called when step function failed to execute"""
    logging.error('Step error: \n\t' + str(exception))


def pytest_bdd_after_scenario(request, feature, scenario):
    """Called after scenario is executed (even if one of steps has failed)"""
    logging.info(f'Execution complete {scenario.name}\n')


def pytest_bdd_step_func_lookup_error(request, feature, scenario, step, exception):
    """Called when step lookup failed"""
    logging.fatal('Step lookup failed: ' + step.keyword + ' ' + step.name +
                  '\nException: ' + str(exception))
