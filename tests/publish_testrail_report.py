#!/usr/bin/env python3
from os import getenv
from argparse import ArgumentParser
from requests.auth import HTTPBasicAuth

from utility.file_utility import FileUtility
from utility.testrail.report_utility import ReportUtility
from utility.testrail.testrail_case_types import TestRailCaseTypes

if __name__ == '__main__':
    command_line_parser = ArgumentParser('Process keyword arguments')
    command_line_parser.add_argument('--env', default='QA', help='Test environment(QA/PPE)')
    command_line_parser.add_argument('--test_modules', default='calculator', help='Test module name')
    command_line_parser.add_argument('--milestone_name', default='Python_BDD', help='Milestone name in TestRail')
    command_line_parser.add_argument('--multi_suite_report', action='store_const', const=True, default=False,
                                     help='Is test case results in report consist from multiple test suite?')
    args = command_line_parser.parse_args()

    ReportUtility.TESTRAIL_AUTH = HTTPBasicAuth(getenv('TESTRAIL_ID'), getenv('TESTRAIL_KEY'))
    ReportUtility.XML_REPORT_PATH = FileUtility.get_file_path(file_name='execution_results.xml',
                                                              relative_directory=f'reports/{args.test_modules}')
    potential_test_cases = ReportUtility.identify_potential_cases()
    if len(potential_test_cases) > 0:
        ReportUtility.create_testrail_cases(potential_test_cases, TestRailCaseTypes.AUTOMATED)
    test_results = ReportUtility.get_test_result()
    milestone_id = ReportUtility.get_milestone_id(args.milestone_name)
    test_module_name = args.test_modules.title().replace('_', ' ')
    test_name = f'{args.env} {test_module_name} - Test automation'
    if not args.multi_suite_report:
        run_id = ReportUtility.create_test_run(milestone_id, test_name, test_module_name)
        ReportUtility.submit_execution_report(run_id, test_results)
        ReportUtility.close_test_run(run_id)
    else:
        test_plan_id = ReportUtility.create_test_plan(milestone_id, test_name)
        run_id_test_result_map = ReportUtility.create_plan_entries(test_plan_id, '', test_results)
        for run_id, results in run_id_test_result_map:
            ReportUtility.submit_execution_report(run_id, results)
        ReportUtility.close_test_plan(test_plan_id)
