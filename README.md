# Todu Skills

Claude Code and Codex skills for working with the `todu` CLI.

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

- Claude Code with plugin support or Codex with plugin support
- `todu` installed and on your `PATH`
- a working `todu` config

Quick check:

```bash
todu --help
```

## Claude Code Installation

Install the `todu` plugin from this repository using your normal Claude Code
plugin workflow.

## Codex Installation

Codex plugins are installed from a local marketplace entry. To install directly
from GitHub:

```bash
curl -fsSL https://raw.githubusercontent.com/evcraddock/todu-skills/main/scripts/install-codex-plugin.sh | bash
```

Or install manually by cloning this repository into `~/plugins/todu`:

```bash
mkdir -p ~/plugins
git clone https://github.com/evcraddock/todu-skills.git ~/plugins/todu
```

Then create or update `~/.agents/plugins/marketplace.json`:

```json
{
  "name": "local",
  "interface": {
    "displayName": "Local Plugins"
  },
  "plugins": [
    {
      "name": "todu",
      "source": {
        "source": "local",
        "path": "./plugins/todu"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

Restart Codex, then install or enable the Todu plugin from the local plugin
marketplace.

## Development

- skill definitions live in `skills/`
- Claude Code plugin metadata lives in `.claude-plugin/`
- Codex plugin metadata lives in `.codex-plugin/`

For local Codex development, symlink this checkout into `~/plugins/todu` and
add the marketplace entry above:

```bash
mkdir -p ~/plugins
ln -sfn /path/to/todu-skills ~/plugins/todu
```

## License

MIT. See [LICENSE](./LICENSE).
