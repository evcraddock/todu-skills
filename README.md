# Todu Skills

Claude Code skills for working with the `todu` CLI.

This repo contains the `todu` plugin/skill pack, not the `todu` application
itself.

## What it includes

Skills for:

- tasks
- projects
- habits
- recurring tasks
- next actions

The skills are written for the current `todu` CLI, including commands like:

- `todu task ...`
- `todu project ...`
- `todu habit ...`
- `todu recurring ...`
- `todu note ...`
- `todu integration ...`

## Requirements

- Claude Code with plugin support
- `todu` installed and on your `PATH`
- a working `todu` config

Quick check:

```bash
todu --help
```

## Installation

Install the `todu` plugin from this repository using your normal Claude Code
plugin workflow.

## Development

- skill definitions live in `skills/`
- plugin metadata lives in `.claude-plugin/`
- test setup lives in `tests/`

If you are testing locally, run `todu` commands from `tests/` so the test config
is used instead of your normal config.

## License

MIT. See [LICENSE](./LICENSE).
