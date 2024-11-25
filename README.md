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

You can try the W3C version of an example test case [here](https://jensk-dk.github.io/HtmlHbbTVTestCaseGenerator/test/TEST_001_step_sequence/test.html). This test demonstrates:
1. Grid-based layout with:
   - Top left: Logo and test metadata
   - Bottom left: Test-specific HTML elements
   - Right half: Test output and evaluation
2. Automatic and manual test steps
3. Manual verification with:
   - Semi-transparent overlay for focus
   - Clear Yes/No buttons with visual feedback
   - Proper cleanup after response
4. Success and failure paths with color-coded output

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
        "test_name": "Basic Step Sequence Test",
        "https_required": false
    };

    // Test initialization code
    var TEST_INIT = `
        var stepCount = 0;
    `;

    // Test execution code
    var TEST_BODY = `
        stepCount++;
        if (stepCount === 1) {
            reportStep(stepCount, 'PASS', 'Automatic step completed');
            setTimeout(runTest, 1000);
        } else if (stepCount === 2) {
            askManual('Did you see the previous step pass?').then(function(result) {
                reportStep(stepCount, result ? 'PASS' : 'FAIL', 
                    'Manual verification ' + (result ? 'succeeded' : 'failed'));
                setTimeout(runTest, 1000);
            });
        } else {
            askManual('Is everything working as expected?').then(function(result) {
                reportStep(stepCount, result ? 'PASS' : 'FAIL', 
                    'Final verification ' + (result ? 'succeeded' : 'failed'));
                endTest(result ? 'PASS' : 'FAIL', 
                    'Test completed with ' + (result ? 'success' : 'failures'));
            });
        }
    `;

    // Additional styles for this test
    var TEST_STYLES = `
        #test-elements ol {
            margin-left: 20px;
            line-height: 1.5;
        }
    `;
    </script>
</head>
<body>
    <div id="test-elements">
        <p>This test demonstrates a sequence of steps with both automatic and manual verification:</p>
        <ol>
            <li>Automatic step that always passes</li>
            <li>Manual verification of the first step</li>
            <li>Final manual verification of the entire test</li>
        </ol>
    </div>
</body>
</html>
```

The test template supports:
- Test metadata (ID, name, HTTPS requirement)
- Initialization code (variables, setup)
- Test execution code (steps, logic)
- Manual verification using `askManual(question)` with overlay and buttons
- Progress reporting with `reportStep(id, result, message)` in the right panel
- Test completion with `endTest(result, message)` and color-coded status
- Additional styles for test-specific customization
- Grid-based layout with dedicated areas for logo, metadata, test elements, and output

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
