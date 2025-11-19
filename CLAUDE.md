- DONT USE MY URL's as examples

## Development and Testing

**CRITICAL - READ THIS FIRST**:

- **Development** means: making changes to ANY files in this project (code, tests, documentation, etc.)
- **ALWAYS** change to the `tests/` directory before running ANY `todu` commands during development or testing
- **NEVER** run `todu` commands from the project root during development
- This ensures `todu` uses `tests/config.yaml` instead of the production config file
- Example: `cd tests && todu project list` instead of `todu project list`
- **FAILURE TO DO THIS WILL MODIFY PRODUCTION DATA**
- No exceptions - this rule applies to all development and testing work
