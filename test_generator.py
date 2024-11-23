from jinja2 import Environment, FileSystemLoader
import os
import json
import re
import shutil
from typing import Dict, List, Union, Literal
from bs4 import BeautifulSoup
from xml_generator import HbbTVXMLGenerator

class TestCaseGenerator:
    def __init__(self, templates_dir: str = "test_templates"):
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.xml_generator = HbbTVXMLGenerator()
        self.ensure_base_template(templates_dir)
        
    def ensure_base_template(self, templates_dir: str):
        """Create base template if it doesn't exist"""
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
        
        base_template_path = os.path.join(templates_dir, "base.html")
        if not os.path.exists(base_template_path):
            self.create_base_template(base_template_path)
    
    def create_base_template(self, base_template_path: str):
        """Create default template files"""
        base_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{ test_id }} - {{ test_name }}</title>
    {% if target == "hbbtv" %}
    <script type="text/javascript" src="../../RES/testsuite.js"></script>
    {% endif %}
    <script>
    {% if target == "hbbtv" %}
    var testapi;
    window.onload = function() {
        testapi = new HbbTVTestAPI();
        testapi.init();
        startTest();
    };
    {% else %}
    window.onload = function() {
        startTest();
    };
    {% endif %}

    function startTest() {
        {% if target == "hbbtv" %}
        testapi.reportMessage("Starting test {{ test_id }}");
        {% else %}
        console.log("Starting test {{ test_id }}");
        {% endif %}
        
        {{ test_init }}
        
        runTest();
    }

    function runTest() {
        {{ test_body }}
    }

    function reportStep(stepId, result, message) {
        {% if target == "hbbtv" %}
        testapi.reportStepResult(stepId, result, message);
        {% else %}
        console.log(`Step ${stepId}: ${result} - ${message}`);
        const div = document.createElement('div');
        div.textContent = `Step ${stepId}: ${result} - ${message}`;
        div.className = result.toLowerCase();
        document.body.appendChild(div);
        {% endif %}
    }

    function endTest(result, message) {
        {% if target == "hbbtv" %}
        testapi.endTest(result, message);
        {% else %}
        console.log(`Test ended: ${result} - ${message}`);
        const div = document.createElement('div');
        div.textContent = `Test ended: ${result} - ${message}`;
        div.className = `test-end ${result.toLowerCase()}`;
        document.body.appendChild(div);
        {% endif %}
    }
    </script>
    <style>
    {% if target == "w3c" %}
    .pass { color: green; }
    .fail { color: red; }
    .test-end { 
        margin-top: 20px;
        font-weight: bold;
    }
    {% endif %}
    {{ additional_styles }}
    </style>
</head>
<body>
    <h1>{{ test_name }}</h1>
    <p>Test ID: {{ test_id }}</p>
    {% if target == "w3c" %}
    <div id="test-output"></div>
    {% endif %}
    {{ test_html }}
</body>
</html>'''
        
        with open(os.path.join(templates_dir, "base.html"), "w") as f:
            f.write(base_template)

    def extract_test_info(self, template_path: str) -> Dict:
        """
        Extract test information from a template file
        
        Args:
            template_path: Path to the template file
            
        Returns:
            Dictionary containing test metadata, init code, body code, and HTML
        """
        with open(template_path, 'r') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract metadata
        metadata_script = soup.find('script', text=re.compile(r'TEST_METADATA'))
        if not metadata_script:
            raise ValueError(f"No TEST_METADATA found in {template_path}")
        
        # Extract the JSON object from the JavaScript variable
        metadata_match = re.search(r'TEST_METADATA\s*=\s*({[^}]+})', metadata_script.string)
        if not metadata_match:
            raise ValueError(f"Invalid TEST_METADATA format in {template_path}")
        metadata = json.loads(metadata_match.group(1))
        
        # Extract initialization code
        init_match = re.search(r'TEST_INIT\s*=\s*`([^`]+)`', content)
        if not init_match:
            raise ValueError(f"No TEST_INIT found in {template_path}")
        init_code = init_match.group(1).strip()
        
        # Extract test body code
        body_match = re.search(r'TEST_BODY\s*=\s*`([^`]+)`', content)
        if not body_match:
            raise ValueError(f"No TEST_BODY found in {template_path}")
        body_code = body_match.group(1).strip()
        
        # Extract any additional HTML from body
        test_container = soup.find('div', id='test-container')
        test_html = str(test_container) if test_container else ""
        
        # Extract any additional styles
        style_tag = soup.find('style')
        additional_styles = style_tag.string if style_tag else ""
        
        return {
            'metadata': metadata,
            'init_code': init_code,
            'body_code': body_code,
            'test_html': test_html,
            'additional_styles': additional_styles
        }
    
    def generate_test_case(self, 
                          test_id: str,
                          test_name: str,
                          test_init: str,
                          test_body: str,
                          target: Literal["hbbtv", "w3c"],
                          test_html: str = "",
                          additional_styles: str = "") -> str:
        """
        Generate a test case for the specified target platform
        
        Args:
            test_id: Unique identifier for the test
            test_name: Human readable name of the test
            test_init: JavaScript code for test initialization
            test_body: JavaScript code for the test steps
            test_html: Additional HTML content for the test
            additional_styles: Additional CSS styles
            target: Target platform ("hbbtv" or "w3c")
            
        Returns:
            The generated HTML test case as a string
        """
        template = self.env.get_template("base.html")
        return template.render(
            test_id=test_id,
            test_name=test_name,
            test_init=test_init,
            test_body=test_body,
            test_html=test_html,
            additional_styles=additional_styles,
            target=target
        )
    
    def generate_from_template(self,
                             template_dir: str,
                             output_base_dir: str = "tests") -> Dict[str, str]:
        """
        Generate both HbbTV and W3C versions of a test case from a template directory
        
        Args:
            template_dir: Path to the template directory containing test.html
            output_base_dir: Base directory for output files
            
        Returns:
            Dictionary with paths to generated files
        """
        template_path = os.path.join(template_dir, "test.html")
        if not os.path.exists(template_path):
            raise ValueError(f"No test.html found in {template_dir}")
            
        # Extract test information
        test_info = self.extract_test_info(template_path)
        test_id = test_info['metadata']['test_id']
        
        # Create output directories
        hbbtv_dir = os.path.join(output_base_dir, "HbbTV", test_id)
        html_dir = os.path.join(output_base_dir, "Html", test_id)
        os.makedirs(hbbtv_dir, exist_ok=True)
        os.makedirs(html_dir, exist_ok=True)
        
        # Generate both versions
        hbbtv_test = self.generate_test_case(
            test_info['metadata']['test_id'],
            test_info['metadata']['test_name'],
            test_info['init_code'],
            test_info['body_code'],
            "hbbtv",
            test_info['test_html'],
            test_info['additional_styles']
        )
        
        w3c_test = self.generate_test_case(
            test_info['metadata']['test_id'],
            test_info['metadata']['test_name'],
            test_info['init_code'],
            test_info['body_code'],
            "w3c",
            test_info['test_html'],
            test_info['additional_styles']
        )
        
        # Save HTML files
        hbbtv_path = os.path.join(hbbtv_dir, "index.html")
        w3c_path = os.path.join(html_dir, "index.html")
        
        with open(hbbtv_path, "w") as f:
            f.write(hbbtv_test)
        with open(w3c_path, "w") as f:
            f.write(w3c_test)
            
        # Generate HbbTV test harness XML files
        https_required = test_info['metadata'].get('https_required', False)
        self.xml_generator.generate_test_xml_files(
            test_info['metadata']['test_id'],
            test_info['metadata']['test_name'],
            hbbtv_dir,
            https_required
        )
            
        # Copy any additional files from template directory (e.g., images, styles)
        for item in os.listdir(template_dir):
            if item != "test.html":
                src_path = os.path.join(template_dir, item)
                if os.path.isfile(src_path):
                    shutil.copy2(src_path, hbbtv_dir)
                    shutil.copy2(src_path, html_dir)
                elif os.path.isdir(src_path):
                    hbbtv_dest = os.path.join(hbbtv_dir, item)
                    html_dest = os.path.join(html_dir, item)
                    if os.path.exists(hbbtv_dest):
                        shutil.rmtree(hbbtv_dest)
                    if os.path.exists(html_dest):
                        shutil.rmtree(html_dest)
                    shutil.copytree(src_path, hbbtv_dest)
                    shutil.copytree(src_path, html_dest)
            
        return {
            "hbbtv": hbbtv_path,
            "w3c": w3c_path
        }
    
    def generate_all_templates(self, 
                             templates_dir: str = "test_templates", 
                             output_dir: str = "tests") -> Dict[str, Dict[str, str]]:
        """
        Generate test cases from all template directories
        
        Args:
            templates_dir: Root directory containing test case directories
            output_dir: Base directory for output files
            
        Returns:
            Dictionary mapping test IDs to their generated file paths
        """
        results = {}
        
        # Find all directories in templates_dir
        for item in os.listdir(templates_dir):
            template_dir = os.path.join(templates_dir, item)
            if os.path.isdir(template_dir):
                try:
                    results[item] = self.generate_from_template(template_dir, output_dir)
                except Exception as e:
                    print(f"Error processing {item}: {str(e)}")
                
        return results

# Example usage
if __name__ == "__main__":
    generator = TestCaseGenerator()
    
    # Generate all test cases from templates
    results = generator.generate_all_templates()
    
    print("Generated test files:")
    for template, files in results.items():
        print(f"\nFrom template {template}:")
        print(f"  HbbTV: {files['hbbtv']}")
        print(f"  W3C: {files['w3c']}")