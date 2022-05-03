import logging
import pytest


@pytest.fixture(autouse=True)
def skip_with_tag(request):
    """Skip test cases based on specific tags"""
    for marker in request.node.iter_markers():
        if marker.name == 'todo':
            pytest.skip("Not completed yet")


@pytest.fixture(autouse=True)
def junit_tag(request, record_property):
    """Apply Jira id to testcase JUnit XML report"""
    for marker in request.node.own_markers:
        if marker.name == 'jira':
            record_property(marker.name, ','.join(marker.args))
        elif 'testrail' in marker.name:
            record_property(marker.name, marker.args[0])


def pytest_bdd_apply_tag(tag, function):
    """Customize how tags are converted to pytest marks"""
    if 'jira' in tag:
        marker = pytest.mark.jira.with_args(*tag[5:-1].split(','))
        marker(function)
        return True
    elif 'testrail' in tag:
        marker = pytest.mark.testrail_suite_id.with_args(tag[18:-1]) \
            if 'suite_id' in tag \
            else pytest.mark.testrail_section_id.with_args(tag[20:-1])
        marker(function)
        return True
    # Fall back to pytest-bdd's default behavior
    return None


def pytest_bdd_before_scenario(feature, scenario):
    """Called before scenario is executed"""
    logging.info(f'\nFeature: {feature.name}\n  Scenario Name: {scenario.name}')


def pytest_bdd_before_step_call(request, step, step_func, step_func_args):
    """Called before step function is executed with evaluated arguments"""
    logging.info(f'\t{step.keyword} {step.name}')
    logging.debug(f'\t\t{str(step_func)[10:-23]}__' +
                  " ".join(f'<{key}={repr(value).split(".")[-1]}>' for key, value in step_func_args.items()))


def pytest_bdd_step_error(request, exception):
    """Called when step function failed to execute"""
    logging.error('Step error: \n\t' + str(exception))


def pytest_bdd_after_scenario(request, feature, scenario):
    """Called after scenario is executed (even if one of steps has failed)"""
    logging.info('Execution complete')


def pytest_bdd_step_func_lookup_error(request, feature, scenario, step, exception):
    """Called when step lookup failed"""
    logging.fatal('Step lookup failed: ' + step.keyword + ' ' + step.name + '\nException: ' + str(exception))
