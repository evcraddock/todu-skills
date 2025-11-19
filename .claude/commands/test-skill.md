---
description: Run test environment setup and execute a skill test
---

# Test Skill Command

Execute this workflow to test a todu skill:

1. **Change to tests directory**: Navigate to `/Users/erik/code/github/evcraddock/todu-skills/tests`

2. **Run setup script**: Execute `bash helpers/setup.sh` to initialize the test environment with:
   - Test project "todu-tests"
   - Sample tasks for testing
   - Verify the output shows successful setup

3. **Load test file**:
   - If a test file was specified as an argument (e.g., `/test-skill project-register`), load the contents of `tests/<test-name>.md`
   - If no argument was provided, list all available test markdown files in the tests directory (excluding subdirectories) and ask the user which test to run

4. **Execute the test**:
   - Parse the test markdown file for code blocks containing test prompts
   - Execute each prompt sequentially as if the user typed it
   - For "register project" prompts, invoke the `core:project-register` skill with the project name
   - Display the results of each test execution
   - Continue through all test scenarios in the file

5. **Cleanup prompt**: After completing the test, use the AskUserQuestion tool to ask:
   - Question: "Test execution complete. Would you like to run the teardown script to clean up the test environment?"
   - Options:
     - "Yes, run teardown" - Run `bash helpers/teardown.sh` to remove test project and tasks
     - "No, keep test data" - Leave the test environment as is for further testing

## Usage Examples

- `/test-skill project-register` - Run the project-register test
- `/test-skill` - Show list of available tests and let user choose

## Notes

- The setup script creates a "todu-tests" project with sample tasks
- The teardown script removes the test project and all associated tasks
- Test files are markdown files in the tests directory
