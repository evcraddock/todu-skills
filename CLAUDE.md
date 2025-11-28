# Development Guidelines

- DONT USE MY URL's as examples

## Development and Testing

**CRITICAL - READ THIS FIRST**:

- **Development Mode** is ONLY active when the user explicitly says "We are in"
  or "Switch to" followed by "Dev Mode" or "Development Mode"
- When in Development Mode:
  - **ALWAYS** change to the `tests/` directory before running ANY `todu`
    commands
  - **NEVER** run `todu` commands from the project root
  - This ensures `todu` uses `tests/config.yaml` instead of the production
    config file
  - Example: `cd tests && todu project list` instead of `todu project list`
  - **FAILURE TO DO THIS WILL MODIFY PRODUCTION DATA**
- When NOT in Development Mode, run `todu` commands normally from any directory
