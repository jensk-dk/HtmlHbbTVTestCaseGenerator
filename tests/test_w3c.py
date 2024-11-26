import pytest
from playwright.sync_api import Page, expect
import os

def test_example_test_case(page: Page):
    # Load the test case
    page.goto(f"file://{os.path.abspath(\"test_templates/TEST_001_step_sequence/test.html\")}")
    
    # Wait for first step to complete
    first_step = page.get_by_text("Step 1: PASS - Automatic step completed")
    expect(first_step).to_be_visible(timeout=5000)
    
    # Wait for first manual verification prompt
    manual_prompt = page.get_by_text("Did you see the previous step pass?")
    expect(manual_prompt).to_be_visible(timeout=5000)
    
    # Click Yes
    yes_button = page.get_by_role("button", name="Yes")
    yes_button.click()
    
    # Wait for second step to complete
    second_step = page.get_by_text("Step 2: PASS - Manual verification succeeded")
    expect(second_step).to_be_visible(timeout=5000)
    
    # Wait for final manual verification prompt
    final_prompt = page.get_by_text("Is everything working as expected?")
    expect(final_prompt).to_be_visible(timeout=5000)
    
    # Click Yes
    yes_button = page.get_by_role("button", name="Yes")
    yes_button.click()
    
    # Wait for final step and test completion
    final_step = page.get_by_text("Step 3: PASS - Final verification succeeded")
    expect(final_step).to_be_visible(timeout=5000)
    test_end = page.get_by_text("Test ended: PASS - Test completed with success")
    expect(test_end).to_be_visible(timeout=5000)

def test_example_test_case_manual_fail(page: Page):
    # Load the test case
    page.goto(f"file://{os.path.abspath(\"test_templates/TEST_001_step_sequence/test.html\")}")
    
    # Wait for first step to complete
    first_step = page.get_by_text("Step 1: PASS - Automatic step completed")
    expect(first_step).to_be_visible(timeout=5000)
    
    # Wait for first manual verification prompt
    manual_prompt = page.get_by_text("Did you see the previous step pass?")
    expect(manual_prompt).to_be_visible(timeout=5000)
    
    # Click No
    no_button = page.get_by_role("button", name="No")
    no_button.click()
    
    # Wait for failure message
    fail_step = page.get_by_text("Step 2: FAIL - Manual verification failed")
    expect(fail_step).to_be_visible(timeout=5000)
    
    # Wait for final manual verification prompt
    final_prompt = page.get_by_text("Is everything working as expected?")
    expect(final_prompt).to_be_visible(timeout=5000)
    
    # Click No
    no_button = page.get_by_role("button", name="No")
    no_button.click()
    
    # Wait for final failure messages
    final_step = page.get_by_text("Step 3: FAIL - Final verification failed")
    expect(final_step).to_be_visible(timeout=5000)
    test_end = page.get_by_text("Test ended: FAIL - Test completed with failures")
    expect(test_end).to_be_visible(timeout=5000)
