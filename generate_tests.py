from pathlib import Path
import sys

from javascript_generator import JavaScriptGenerators

if __name__ == '__main__':

    # TODO: Take parameters

#    testInputPath = Path("test_cases")
#    testOutputPath = Path("out")

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
