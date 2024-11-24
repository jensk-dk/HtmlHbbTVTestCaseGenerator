# HtmlHbbTVTestCaseGenerator

A Python script that generates both HTML and HbbTV test cases from a templated common code base.

## Features

- Generate both HbbTV and W3C browser test cases from a single template
- Automatic generation of HbbTV test harness XML files:
  - `implementation.xml` - Test implementation details
  - `ait.xml` - Application Information Table
  - `playoutset.xml` - DVB playout configuration

## Directory Structure

```
test_templates/                    # Templates directory
├── base.html                     # Base template for all test cases
└── TEST_001_step_sequence/       # Example test case
    └── test.html                # Test implementation

tests/                           # Generated test cases (not in git)
├── HbbTV/
│   └── TEST_001/
│       ├── index.html          # HbbTV test case
│       ├── implementation.xml  # Test implementation
│       ├── ait.xml            # Application info
│       ├── playoutset.xml     # DVB configuration
│       └── resources/         # Test resources (if any)
└── Html/
    └── TEST_001/
        ├── index.html         # W3C browser test
        └── resources/         # Test resources (if any)
```

The generator uses `base.html` as a template to create both HbbTV and W3C versions of each test case. Test cases are organized in their own directories under `test_templates/`, with each test case defined in a `test.html` file.

## Try it out

You can try the W3C version of an example test case [here](https://jensk-dk.github.io/HtmlHbbTVTestCaseGenerator/test/TEST_001.html). This test demonstrates:
1. Automatic test steps
2. Manual verification with Yes/No buttons
3. Success and failure paths
4. Progress reporting

## Usage

1. Create a test template in `test_templates/YOUR_TEST_ID/test.html`. Here's an example from `test_templates/TEST_001_step_sequence/test.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <script>
    // Test metadata
    var TEST_METADATA = {
        "test_id": "TEST_001",
        "test_name": "Example Test Case - Step Sequence",
        "https_required": false
    };

    // Test initialization code
    var TEST_INIT = `
        var testSteps = ["step1", "step2", "step3"];
        var currentStep = 0;
    `;

    // Test execution code
    var TEST_BODY = `
        async function checkStep() {
            switch(testSteps[currentStep]) {
                case "step1":
                    reportStep(1, "PASS", "First step completed");
                    currentStep++;
                    setTimeout(checkStep, 1000);
                    break;
                    
                case "step2":
                    const manualResult = await askManual("Did you see the first step complete successfully?");
                    if (manualResult) {
                        reportStep(2, "PASS", "Manual verification successful");
                        currentStep++;
                        setTimeout(checkStep, 1000);
                    } else {
                        reportStep(2, "FAIL", "Manual verification failed");
                        endTest("FAIL", "Manual verification failed at step 2");
                    }
                    break;
                    
                case "step3":
                    reportStep(3, "PASS", "Third step completed");
                    endTest("PASS", "All steps completed successfully");
                    break;
            }
        }
        
        checkStep();
    `;
    </script>
</head>
<body>
    <div id="test-container">
        <p>This test verifies a sequence of steps with timing and manual verification.</p>
    </div>
</body>
</html>
```

The test template supports:
- Test metadata (ID, name, HTTPS requirement)
- Initialization code (variables, setup)
- Test execution code (steps, logic)
- Manual verification using `askManual(question)`
- Progress reporting with `reportStep(id, result, message)`
- Test completion with `endTest(result, message)`

2. Run the generator:
```bash
python test_generator.py
```

3. Find the generated test cases in:
   - `tests/HbbTV/TEST_001/` - HbbTV test case with XML files
   - `tests/Html/TEST_001/` - W3C browser test case

4. Run the tests:
   - HbbTV: Load in test harness
   - W3C: Open in browser or run with Playwright:
     ```bash
     pytest tests/test_w3c.py --browser chromium
     ```

## License

GNU Affero General Public License v3.0
