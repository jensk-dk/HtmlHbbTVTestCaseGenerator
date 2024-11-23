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

1. Create a test template in `test_templates/YOUR_TEST_ID/test.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <script>
    // Test metadata
    var TEST_METADATA = {
        "test_id": "YOUR_TEST_ID",
        "test_name": "Your Test Name",
        "https_required": false
    };

    // Initialization code
    var TEST_INIT = `
        // Your initialization code
    `;

    // Test execution code
    var TEST_BODY = `
        // Your test steps
    `;
    </script>
</head>
<body>
    <div id="test-container">
        <!-- Your test-specific HTML -->
    </div>
</body>
</html>
```

2. Run the generator:
```bash
python test_generator.py
```

The generator will create both HbbTV and W3C versions in the `tests` directory.

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
