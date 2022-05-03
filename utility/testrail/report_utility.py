from os import path
from requests import get, post
from requests.auth import HTTPBasicAuth
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from utility.testrail.testrail_status import TestRailStatus
from utility.testrail.testrail_case_types import TestRailCaseTypes


class ReportUtility:
    PROJECT_ID = 2
    TESTRAIL_AUTH: HTTPBasicAuth
    BASE_URL = 'https://kr87nikhil.testrail.io/index.php?api/v2'
    TODO_MESSAGE = 'Not completed yet'
    XML_REPORT_PATH: str = None
    _suite_id_case_ids_map = dict()

    @classmethod
    def get_suite_case_map(cls):
        return cls._suite_id_case_ids_map

    @classmethod
    def set_suite_case_map(cls, suite_ids):
        for suite_id in suite_ids:
            cases_response = get(cls._get_url(f'get_cases/{cls.PROJECT_ID}&suite_id={suite_id}'), auth=cls.TESTRAIL_AUTH,
                                 headers={'Content-Type': 'application/json'})
            cases_response.raise_for_status()
            cls._suite_id_case_ids_map.update(
                {suite_id: {test_case.get('title'): test_case.get('id') for test_case in cases_response.json().get('cases')}})

    # region Create Testrail cases
    @classmethod
    def identify_potential_cases(cls):
        """Identify test cases not already available in TestRail"""
        test_cases_dict = dict()
        with open(cls.XML_REPORT_PATH) as file_object:
            root_element = ElementTree.parse(file_object).getroot()
            for test_case in root_element.iter('testcase'):
                if cls._has_todo_tag(cls._get_testrail_status(test_case), test_case):
                    continue
                case_name = test_case.get('name')
                jira_ids = cls._get_property(test_case, 'jira')
                suite_id = cls._get_property(test_case, 'testrail_suite_id')
                section_id = cls._get_property(test_case, 'testrail_section_id')
                if suite_id not in test_cases_dict.keys():
                    test_cases_dict[suite_id] = dict()
                if section_id not in test_cases_dict.get(suite_id).keys():
                    test_cases_dict[suite_id][section_id] = list()
                test_cases_dict[suite_id][section_id].append((jira_ids, case_name))
        test_cases_identified = list()
        for suite_id, section_dict in test_cases_dict.items():
            response = get(cls._get_url(f'get_cases/{cls.PROJECT_ID}&suite_id={suite_id}'),
                           auth=cls.TESTRAIL_AUTH, headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            existing_test_cases = response.json()
            for section_id, case_details in section_dict.items():
                cases_in_section = list(filter(lambda x: x.get('section_id') == int(section_id), existing_test_cases.get('cases')))
                test_case_names = set(map(lambda x: x[1], case_details)) - {test_case.get('title') for test_case in cases_in_section}
                if len(test_case_names) > 0:
                    test_cases_identified.append((
                        section_id, list(case_detail for case_detail in case_details if case_detail[1] in test_case_names)
                    ))
        return test_cases_identified

    @classmethod
    def create_testrail_cases(cls, test_cases_identified, test_case_type: TestRailCaseTypes):
        for section_id, case_detail in test_cases_identified:
            for jira_ids, case_title in case_detail:
                response = post(cls._get_url(f'add_case/{section_id}'), auth=cls.TESTRAIL_AUTH,
                                headers={'Content-Type': 'application/json'},
                                json={'section_id': int(section_id), 'title': case_title,
                                      'type_id': test_case_type.value, 'refs': jira_ids})
                response.raise_for_status()
    # endregion

    @classmethod
    def get_test_result(cls):
        result_array = list()
        with open(cls.XML_REPORT_PATH) as file_object:
            root_element = ElementTree.parse(file_object).getroot()
            cls.set_suite_case_map(
                {int(cls._get_property(test_case, 'testrail_suite_id')) for test_case in root_element.iter('testcase')})
            for test_case in root_element.iter('testcase'):
                test_result = dict()
                status_id = cls._get_testrail_status(test_case)
                if cls._has_todo_tag(status_id, test_case):
                    continue
                case_name = test_case.get('name')
                suite_id = int(cls._get_property(test_case, 'testrail_suite_id'))
                test_result['case_id'] = cls.get_suite_case_map().get(suite_id).get(case_name)
                test_result['status_id'] = status_id
                if status_id == TestRailStatus.Passed.value or status_id == TestRailStatus.Failed.value:
                    test_result['elapsed'] = test_case.get('time') + 's'
                if status_id == TestRailStatus.Failed.value:
                    error = test_case.find('error')
                    failure = test_case.find('failure')
                    fail_element = error if error is not None else failure
                    test_result['comment'] = f'Message: {fail_element.get("message")}\nStack Trace: {fail_element.text}'
                if status_id == TestRailStatus.Blocked.value:
                    test_result['comment'] = 'Reason: ' + test_case.find('skipped').get('message')
                result_array.append(test_result)
        return result_array

    @classmethod
    def submit_execution_report(cls, run_id, test_results):
        """Submit test execution report to TestRail"""
        response = post(cls._get_url(f'add_results_for_cases/{run_id}'), auth=cls.TESTRAIL_AUTH,
                        headers={'Content-Type': 'application/json'}, json={'results': test_results})
        response.raise_for_status()

    # region Publish Test Plan/Run report
    @classmethod
    def get_milestone_id(cls, milestone_name) -> int:
        """Get milestone id for the corresponding milestone name within testRail project"""
        response = get(cls._get_url(f'get_milestones/{cls.PROJECT_ID}&is_started=1'),
                       auth=cls.TESTRAIL_AUTH, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return [milestone.get('id') for milestone in response.json().get('milestones') if milestone.get('name') == milestone_name][0]

    @classmethod
    def create_test_run(cls, milestone_id, test_run_name, test_suite_name):
        test_suites_response = get(cls._get_url(f'get_suites/{cls.PROJECT_ID}'), auth=cls.TESTRAIL_AUTH)
        test_suites_response.raise_for_status()
        suite_ids = {test_suite.get('id') for test_suite in test_suites_response.json() if test_suite.get('name') == test_suite_name}
        if len(suite_ids) > 1:
            raise ValueError('More than 1 test_suite identified for single test_suite scenario')
        run_response = post(cls._get_url(f'add_run/{cls.PROJECT_ID}'),
                            json={'milestone_id': milestone_id, 'name': test_run_name, 'suite_id': list(suite_ids)[0]},
                            auth=cls.TESTRAIL_AUTH, headers={'Content-Type': 'application/json'})
        run_response.raise_for_status()
        return run_response.json().get('id')

    @classmethod
    def create_test_plan(cls, milestone_id, test_plan_name) -> int:
        response = post(cls._get_url(f'add_plan/{cls.PROJECT_ID}'), auth=cls.TESTRAIL_AUTH,
                        headers={'Content-Type': 'application/json'}, json={'name': test_plan_name, 'milestone_id': milestone_id})
        response.raise_for_status()
        return response.json().get('id')

    @classmethod
    def create_plan_entries(cls, test_plan_id, entry_description, test_results) -> list:
        """Get TestRail Plan entry from test result execution"""
        run_id_test_results_map = list()
        user_id = cls._get_user_id()
        case_ids = {result.get('case_id') for result in test_results}
        for suite_id, test_case_ids in cls.get_suite_case_map():
            case_id_selection = case_ids.intersection(test_case_ids)
            if len(case_id_selection) == 0:
                continue
            response = post(cls._get_url(f'add_plan_entry/{test_plan_id}'), auth=cls.TESTRAIL_AUTH,
                            headers={'Content-Type': 'application/json'},
                            json={'suite_id': suite_id, 'description': entry_description,
                                  'assignedto_id': user_id, 'include_all': False, 'case_ids': list(case_id_selection)})
            response.raise_for_status()
            run_id_test_results_map.append((response.json().get('runs')[0].get('id'),
                                            list(filter(lambda x: x.get('case_id') in case_id_selection, test_results))))
        return run_id_test_results_map

    @classmethod
    def close_test_run(cls, test_run_id):
        """Close test run after report submission"""
        response = post(cls._get_url(f'close_run/{test_run_id}'), auth=cls.TESTRAIL_AUTH, headers={'Content-Type': 'application/json'})
        response.raise_for_status()

    @classmethod
    def close_test_plan(cls, test_plan_id):
        """Close TestRail Plan after test report submission"""
        response = post(cls._get_url(f'close_plan/{test_plan_id}'), auth=cls.TESTRAIL_AUTH, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
    # endregion

    # region Private methods
    @staticmethod
    def _get_property(test_case: Element, custom_property) -> str:
        """Read property from TestCase element in XML Report"""
        for element in test_case.iter('property'):
            if element.get('name') == custom_property:
                return element.get('value')
        raise ValueError(f'{custom_property} not found for passed test_case element')

    @staticmethod
    def _build_comment(case_name):
        """Build testRail comment field for Test results"""
        try:
            case_length = case_name.index('[')
        except ValueError:
            case_length = len(case_name)
        return '\n'.join((case_name[:case_length], case_name[case_length:])) if case_length < len(
            case_name) else case_name

    @staticmethod
    def _get_testrail_status(test_case: Element):
        """Get test case result of test element in XML report"""
        if test_case.find('error') is not None or test_case.find('failure') is not None:
            return TestRailStatus.Failed.value
        elif test_case.find('skipped') is not None:
            return TestRailStatus.Blocked.value
        else:
            return TestRailStatus.Passed.value

    @classmethod
    def _has_todo_tag(cls, testrail_status_id: int, test_case: Element):
        """Check if XML report has `todo` tag specified"""
        if testrail_status_id == TestRailStatus.Blocked.value:
            skip_message = test_case.find('skipped').get('message')
            if skip_message == cls.TODO_MESSAGE:
                return True
        return False

    @classmethod
    def _get_url(cls, relative_path):
        """Construct testRail API url from relative path"""
        return path.join(cls.BASE_URL, relative_path).replace('\\', '/')

    @classmethod
    def _get_user_id(cls) -> int:
        """Get current testRail user Id"""
        response = get(cls._get_url('get_current_user'), auth=cls.TESTRAIL_AUTH, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json().get('id')
    # endregion
