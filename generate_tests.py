from pathlib import Path
import sys

from javascript_generator import JavaScriptGenerator

def generateTestCase(testCaseDir: Path, outputDir: Path):
    jsg = JavaScriptGenerator()
    jsg.load_base(testCaseDir)




if __name__ == '__main__':

    # TODO: Take parameters

    testInputPath = Path("test_cases")
    testOutputPath = Path("out")

    if not testInputPath.exists():
        print(f"Test case input path {testInputPath} does not exists")
        sys.exit(1)

    if not testOutputPath.exists():
        testOutputPath.mkdir()

    for testCasePath in testInputPath.iterdir():


        if testCasePath.is_dir():
            generateTestCase(testCasePath, testOutputPath / testCasePath.name)
