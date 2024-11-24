import pytest
from playwright.sync_api import Page, expect
import os

def test_example_test_case(page: Page):
    # Load the test case
    page.goto(f"file://{os.path.abspath(\"tests/Html/TEST_001/index.html\")}")
    
    # Wait for first step to complete
    first_step = page.get_by_text("Step 1: PASS - First step completed")
    expect(first_step).to_be_visible(timeout=5000)
    
    # Wait for manual verification prompt
    manual_prompt = page.get_by_text("Did you see the first step complete successfully?")
    expect(manual_prompt).to_be_visible(timeout=5000)
    
    # Click Yes
    yes_button = page.get_by_role("button", name="Yes")
    yes_button.click()
    
    # Wait for second step to complete
    second_step = page.get_by_text("Step 2: PASS - Manual verification successful")
    expect(second_step).to_be_visible(timeout=5000)
    
    # Wait for third step to complete
    third_step = page.get_by_text("Step 3: PASS - Third step completed")
    expect(third_step).to_be_visible(timeout=5000)
    
    # Wait for test completion
    test_end = page.get_by_text("Test ended: PASS - All steps completed successfully")
    expect(test_end).to_be_visible(timeout=5000)

def test_example_test_case_manual_fail(page: Page):
    # Load the test case
    page.goto(f"file://{os.path.abspath(\"tests/Html/TEST_001/index.html\")}")
    
    # Wait for first step to complete
    first_step = page.get_by_text("Step 1: PASS - First step completed")
    expect(first_step).to_be_visible(timeout=5000)
    
    # Wait for manual verification prompt
    manual_prompt = page.get_by_text("Did you see the first step complete successfully?")
    expect(manual_prompt).to_be_visible(timeout=5000)
    
    # Click No
    no_button = page.get_by_role("button", name="No")
    no_button.click()
    
    # Wait for failure message
    fail_step = page.get_by_text("Step 2: FAIL - Manual verification failed")
    expect(fail_step).to_be_visible(timeout=5000)
    
    # Wait for test completion
    test_end = page.get_by_text("Test ended: FAIL - Manual verification failed at step 2")
    expect(test_end).to_be_visible(timeout=5000)
