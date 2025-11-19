# Todu Skills Test Environment

This directory contains the test environment setup for developing and
validating todu skills.

## Directory Structure

```text
tests/
├── config.yaml           # Test API configuration
├── fixtures/             # Sample JSON responses from todu commands
│   ├── project-list.json
│   ├── task-list.json
│   └── task-show.json
├── helpers/              # Setup and teardown scripts
│   ├── setup.sh
│   └── teardown.sh
└── README.md            # This file
```

## Test Configuration

The `config.yaml` file points to a test API instance (not production).
When you run todu commands from this directory, they will use this
configuration automatically.

```yaml
api_url: "http://localhost:8005"
```

## Setup and Teardown

### Setup Test Environment

Run the setup script to create a clean test environment:

```bash
cd tests
./helpers/setup.sh
```

This script will:

1. Verify todu CLI is installed
2. Check test API accessibility
3. Create a local project named `todu-tests`
4. Create sample tasks for testing:
   - A high-priority task with multiple labels
   - A medium-priority task
   - A completed task

### Teardown Test Environment

When you're done testing, clean up the test environment:

```bash
cd tests
./helpers/teardown.sh
```

This script will:

1. Remove the `todu-tests` project and all associated tasks

## Fixture Files

The `fixtures/` directory contains sample JSON responses from todu
commands. These files are useful for:

- Understanding the structure of API responses
- Validating skill output formats
- Testing without making live API calls
- Documentation and examples

### Available Fixtures

- **project-list.json**: Output from `todu project list --format json`
- **task-list.json**: Output from `todu task list --format json`
- **task-show.json**: Output from `todu task show <id> --format json`

### Regenerating Fixtures

If you need to regenerate fixture files with fresh data:

```bash
cd tests

# Run setup to create test project and tasks
./helpers/setup.sh

# Generate fixture files
todu project list --format json > fixtures/project-list.json
todu task list --format json > fixtures/task-list.json
todu task show 1 --format json > fixtures/task-show.json

# Clean up when done
./helpers/teardown.sh
```

## Usage Examples

### Running Skills Against Test Environment

```bash
cd tests

# Setup test environment
./helpers/setup.sh

# Run your skill (example)
# Skills will use the test API automatically
todu task list --project todu-tests

# Teardown when done
./helpers/teardown.sh
```

### Using Fixture Files

```bash
cd tests

# View sample project list structure
cat fixtures/project-list.json | jq .

# View sample task structure
cat fixtures/task-show.json | jq .

# Count tasks in fixture
cat fixtures/task-list.json | jq '. | length'
```

## Notes

- The test environment uses a local system type, so no external synchronization occurs
- Test data is isolated and won't affect production projects
- Always run teardown.sh when finished to clean up test data
- Fixture files are committed to the repository for reference
