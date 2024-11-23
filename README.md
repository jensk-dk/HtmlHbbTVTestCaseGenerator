# HtmlHbbTVTestCaseGenerator

A Python script that generates both HTML and HbbTV test cases from a templated common code base. The generator creates functionally identical test cases that can run in standard W3C browsers and HbbTV test harnesses.

## Specifications

The generator follows these specifications:

- [HbbTV Test Specification v2024-1](https://www.hbbtv.org/wp-content/uploads/2024/03/HbbTV_Test_Spec_v2024-1_v1.0.pdf) - Defines the test harness requirements, APIs, and XML formats
- [ETSI TS 102 796](https://www.etsi.org/deliver/etsi_ts/102700_102799/102796/01.07.01_60/ts_102796v010701p.pdf) - Core HbbTV technical specification

## Features

- Generates both HbbTV and W3C browser compatible test cases
- Uses a template system for creating test cases
- Maintains identical functionality between versions
- Generates required HbbTV test harness XML files:
  - `implementation.xml` - Test implementation details
  - `ait.xml` - Application Information Table
  - `playoutset.xml` - DVB playout configuration

## Directory Structure

```
test_templates/           # Test case templates
└── TEST_001/
    ├── test.html        # Test template
    └── resources/       # Test-specific resources

tests/                   # Generated test cases
├── HbbTV/
│   └── TEST_001/
│       ├── index.html          # HbbTV test case
│       ├── implementation.xml  # Test implementation
│       ├── ait.xml            # Application info
│       ├── playoutset.xml     # DVB configuration
│       └── resources/         # Test resources
└── Html/
    └── TEST_001/
        ├── index.html         # W3C browser test
        └── resources/         # Test resources
```

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
        var testSteps = ['step1', 'step2', 'step3'];
        var currentStep = 0;
    `;

    // Test execution code
    var TEST_BODY = `
        function checkStep() {
            switch(testSteps[currentStep]) {
                case 'step1':
                    reportStep(1, "PASS", "First step completed");
                    currentStep++;
                    setTimeout(checkStep, 1000);
                    break;
                    
                case 'step2':
                    reportStep(2, "PASS", "Second step completed");
                    currentStep++;
                    setTimeout(checkStep, 1000);
                    break;
                    
                case 'step3':
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
        <p>This test verifies a sequence of steps with timing.</p>
    </div>
</body>
</html>
```

2. Run the generator:
```bash
$ python test_generator.py
Generated test files:

From template TEST_001_step_sequence:
  HbbTV: tests/HbbTV/TEST_001/index.html
  W3C: tests/Html/TEST_001/index.html
```

3. Check the generated files:
```bash
$ ls -R tests/
tests/:
HbbTV  Html

tests/HbbTV:
TEST_001

tests/HbbTV/TEST_001:
ait.xml  implementation.xml  index.html  playoutset.xml

tests/Html:
TEST_001

tests/Html/TEST_001:
index.html
```

The generator creates:

- **W3C Browser Version** (`tests/Html/TEST_001/index.html`):
  - Uses console.log for debugging
  - Shows test progress on screen
  - Visual pass/fail indicators
  - No HbbTV dependencies

- **HbbTV Version** (`tests/HbbTV/TEST_001/`):
  - `index.html` - HbbTV test case
  - `implementation.xml` - Test implementation details:
    ```xml
    <?xml version="1.0" ?>
    <testImplementation xmlns="http://www.hbbtv.org/2012/testImplementation" id="TEST_001">
      <playoutSets>
        <playoutSet id="1" definition="playoutset.xml"/>
      </playoutSets>
    </testImplementation>
    ```
  - `ait.xml` - Application Information Table
  - `playoutset.xml` - DVB playout configuration

Both versions maintain identical test logic and functionality while using platform-appropriate APIs for reporting and execution.

## Requirements

- Python 3.6+
- Jinja2
- BeautifulSoup4

## Installation

```bash
pip install jinja2 beautifulsoup4
```

## License

GNU Affero General Public License v3.0
