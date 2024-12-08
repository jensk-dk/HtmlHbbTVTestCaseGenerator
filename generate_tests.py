from pathlib import Path
import sys
import argparse

import json

from javascript_generator import JavaScriptGenerator

DESCRIPTION_FILE = 'description.json'

HBBTV_FILES_KEY = 'hbbtv_files'
W3C_FILES_KEY = 'w3c_files'

TEST_CASE_NAME_KEY = 'test_case_name'

JAVASCRIPT_GENERATOR = JavaScriptGenerator()

def generate_test(data: dict[str, any], output_path_hbbtv: Path, output_path_w3c: Path) -> None:

    if HBBTV_FILES_KEY in data:
        output_path = output_path_hbbtv / data[TEST_CASE_NAME_KEY]

        if not output_path.exists():
            output_path.mkdir()

        JAVASCRIPT_GENERATOR.generate_main_js_file(data[HBBTV_FILES_KEY], output_path)

    if W3C_FILES_KEY in data:
        output_path = output_path_w3c / data[TEST_CASE_NAME_KEY]
        if not output_path.exists():
            output_path.mkdir()
            JAVASCRIPT_GENERATOR.generate_main_js_file(data[W3C_FILES_KEY], output_path)

def load_description(test_path: Path) -> dict[str, any]:

    description_path = test_path / DESCRIPTION_FILE

    data = None

    with open(description_path, 'r') as description_file:
        data = json.load(description_file)
    return data

if __name__ == '__main__':


    argument_parser = argparse.ArgumentParser(prog="HTMLTESTGENERATOR", description='Allows for generating HbbTV test cases')
    argument_parser.add_argument('-m', '--multiple_test_directory', help='Path to a directory that contains multiple test cases directories')
    argument_parser.add_argument('-s', '--single_test_directory', help='Path to a directory containing a single test case')


    parsed_arguments = argument_parser.parse_args()

    if parsed_arguments.multiple_test_directory:
        test_directory = Path(parsed_arguments.multiple_test_directory)
        if test_directory.exists() and test_directory.is_dir():
            print('x')
        else:
            print(f'Path: {test_directory} either does not exists or is not a directory')


        """
    hbbtv_js = [Path('./test_cases/demo/main.js'), Path('./test_cases/demo/hbbtv.js')]
    hbbtv_js_a = [Path('./test_cases/demo/main.js'), Path('./test_cases/demo/hbbtv.js'), Path('./test_cases/demo/hbbtv_2.js')]
    hbbtv_js_b = [Path('./test_cases/demo/main.js'), Path('./test_cases/demo/hbbtv_2.js'), Path('./test_cases/demo/hbbtv.js')]
    w3c_js = [Path('./test_cases/demo/main.js'), Path('./test_cases/demo/normal.js')]
    hbbtv_js_c = [Path('./test_cases/demo/hbbtv.js')]

    output_path_hbbtv_js = Path('./out/hbbtv_main.js')
    output_path_hbbtv_js_a = Path('./out/hbbtv_main_a.js')
    output_path_hbbtv_js_b = Path('./out/hbbtv_main_b.js')
    output_path_hbbtv_js_c = Path('./out/hbbtv_main_c.js')
    output_path_w3c_js = Path('./out/w3c_main.js')

    js_gen = JavaScriptGenerator()
    js_gen.generate_main_js_file(hbbtv_js, output_path_hbbtv_js)
    js_gen.generate_main_js_file(hbbtv_js_a, output_path_hbbtv_js_a)
    js_gen.generate_main_js_file(hbbtv_js_b, output_path_hbbtv_js_b)
    js_gen.generate_main_js_file(hbbtv_js_c, output_path_hbbtv_js_c)

    js_gen.generate_main_js_file(w3c_js, output_path_w3c_js)
"""
