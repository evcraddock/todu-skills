#!/usr/bin/env bash
set -euo pipefail

repo_url="${TODU_CODEX_REPO_URL:-https://github.com/evcraddock/todu-skills.git}"
plugin_dir="${TODU_CODEX_PLUGIN_DIR:-$HOME/plugins/todu}"
marketplace_file="${TODU_CODEX_MARKETPLACE:-$HOME/.agents/plugins/marketplace.json}"

mkdir -p "$(dirname "$plugin_dir")" "$(dirname "$marketplace_file")"

if [ -d "$plugin_dir/.git" ]; then
  git -C "$plugin_dir" pull --ff-only
elif [ -e "$plugin_dir" ]; then
  echo "Refusing to replace existing non-git path: $plugin_dir" >&2
  exit 1
else
  git clone "$repo_url" "$plugin_dir"
fi

MARKETPLACE_FILE="$marketplace_file" python3 <<'PY'
import json
import os
from pathlib import Path

path = Path(os.environ["MARKETPLACE_FILE"]).expanduser()

if path.exists():
    data = json.loads(path.read_text())
else:
    data = {
        "name": "local",
        "interface": {"displayName": "Local Plugins"},
        "plugins": [],
    }

data.setdefault("name", "local")
data.setdefault("interface", {}).setdefault("displayName", "Local Plugins")
plugins = data.setdefault("plugins", [])

todu_entry = {
    "name": "todu",
    "source": {
        "source": "local",
        "path": "./plugins/todu",
    },
    "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    },
    "category": "Productivity",
}

plugins[:] = [plugin for plugin in plugins if plugin.get("name") != "todu"]
plugins.append(todu_entry)

path.write_text(json.dumps(data, indent=2) + "\n")
PY

echo "Installed Todu Codex plugin at $plugin_dir"
echo "Updated $marketplace_file"
echo "Restart Codex, then install or enable Todu from Local Plugins."
