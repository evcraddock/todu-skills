"""
Plugin registry for todu task management systems.

Discovers plugins from marketplace.json and provides access to their
scripts and capabilities.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class Plugin:
    """Represents a todu plugin."""

    def __init__(self, plugin_dir: Path):
        self.plugin_dir = plugin_dir
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"

        if not manifest_path.exists():
            raise FileNotFoundError(f"Plugin manifest not found: {manifest_path}")

        with open(manifest_path) as f:
            self.manifest = json.load(f)

        # Standard fields from plugin.json
        self.name = self.manifest['name']
        self.description = self.manifest.get('description', '')
        self.version = self.manifest.get('version', '0.0.0')

        # Extended fields from todu.json
        todu_path = plugin_dir / ".claude-plugin" / "todu.json"
        if todu_path.exists():
            with open(todu_path) as f:
                todu_manifest = json.load(f)

            self.system = todu_manifest.get('system', self.name)
            self.display_name = todu_manifest.get('displayName', self.name.title())
            self.capabilities = todu_manifest.get('capabilities', {})
            self.scripts = todu_manifest.get('scripts', {})
            self.requirements = todu_manifest.get('requirements', {})
            self.interface = todu_manifest.get('interface', {})
        else:
            # Fallback to defaults if todu.json doesn't exist
            self.system = self.name
            self.display_name = self.name.title()
            self.capabilities = {}
            self.scripts = {}
            self.requirements = {}
            self.interface = {}

    def get_script_path(self, operation: str) -> Path:
        """Get path to script for an operation.

        Args:
            operation: The operation name (create, update, sync, view, comment)

        Returns:
            Path to the script

        Raises:
            ValueError: If operation is not supported
            FileNotFoundError: If script file doesn't exist
        """
        if operation not in self.scripts:
            raise ValueError(
                f"Operation '{operation}' not supported by {self.system}. "
                f"Available: {', '.join(self.scripts.keys())}"
            )

        script_path = self.plugin_dir / self.scripts[operation]

        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")

        return script_path

    def is_available(self) -> bool:
        """Check if plugin requirements are met.

        Returns:
            True if all required environment variables are set
        """
        for env_var in self.requirements.get('env', []):
            if not os.environ.get(env_var):
                return False
        return True

    def build_args(self, operation: str, task_data: Optional[Dict] = None, params: Optional[Dict] = None) -> List[str]:
        """Build command line arguments for an operation based on interface spec.

        Args:
            operation: The operation name (create, update, sync, view, comment)
            task_data: Task data dictionary (contains systemData, etc.)
            params: Additional parameters to pass to the script

        Returns:
            List of command line arguments

        Raises:
            ValueError: If operation is not supported or required args missing
        """
        if not self.interface or 'operations' not in self.interface:
            raise ValueError(f"No interface specification found for {self.system}")

        if operation not in self.interface['operations']:
            raise ValueError(
                f"Operation '{operation}' not in interface spec for {self.system}. "
                f"Available: {', '.join(self.interface['operations'].keys())}"
            )

        args = []
        task_data = task_data or {}
        params = params or {}

        op_spec = self.interface['operations'][operation]

        for arg_name, arg_spec in op_spec['args'].items():
            source = arg_spec['source']
            flag = arg_spec['flag']
            optional = arg_spec.get('optional', False)

            # Resolve value from source
            value = None

            if source == 'param':
                # Value comes from params dict
                value = params.get(arg_name)
            elif source.startswith('systemData.'):
                # Value comes from task_data.systemData.field
                field = source.split('.', 1)[1]
                value = task_data.get('systemData', {}).get(field)
            else:
                # Value comes from params directly (for repo, project_id, etc.)
                value = params.get(source)

            # Add to args if value exists
            if value is not None:
                args.extend([flag, str(value)])
            elif not optional:
                raise ValueError(
                    f"Required argument '{arg_name}' (source: {source}) "
                    f"not found for operation '{operation}' on {self.system}"
                )

        return args

    def __repr__(self):
        return f"Plugin({self.system}, available={self.is_available()})"


class PluginRegistry:
    """Discovers and manages todu plugins."""

    def __init__(self, todu_root: Optional[Path] = None):
        if todu_root is None:
            # Default to todu root (3 levels up from this script)
            todu_root = Path(__file__).resolve().parent.parent.parent

        self.todu_root = Path(todu_root)
        self.plugins: Dict[str, Plugin] = {}
        self._discover_plugins()

    def _discover_plugins(self):
        """Discover plugins from marketplace.json."""
        marketplace_path = self.todu_root / ".claude-plugin" / "marketplace.json"

        if not marketplace_path.exists():
            raise FileNotFoundError(f"Marketplace file not found: {marketplace_path}")

        with open(marketplace_path) as f:
            marketplace = json.load(f)

        for plugin_info in marketplace.get('plugins', []):
            plugin_dir = self.todu_root / plugin_info['source'].lstrip('./')

            try:
                plugin = Plugin(plugin_dir)
                # Only register if it has task management capabilities
                if plugin.capabilities.get('taskManagement'):
                    self.plugins[plugin.system] = plugin
            except Exception as e:
                # Don't fail if one plugin can't be loaded
                print(f"Warning: Failed to load plugin from {plugin_dir}: {e}")

    def get_plugin(self, system: str) -> Optional[Plugin]:
        """Get plugin by system name.

        Args:
            system: The system name (github, forgejo, todoist)

        Returns:
            Plugin instance or None if not found
        """
        return self.plugins.get(system)

    def get_available_systems(self) -> List[Dict]:
        """Get list of available task management systems.

        Returns:
            List of dicts containing system info
        """
        systems = []
        for plugin in self.plugins.values():
            systems.append({
                'system': plugin.system,
                'displayName': plugin.display_name,
                'description': plugin.description,
                'available': plugin.is_available(),
                'requirements': plugin.requirements
            })
        return systems

    def get_script_path(self, system: str, operation: str) -> Path:
        """Get path to script for system and operation.

        Args:
            system: The system name (github, forgejo, todoist)
            operation: The operation name (create, update, sync, view, comment)

        Returns:
            Path to the script

        Raises:
            ValueError: If system not found or operation not supported
            FileNotFoundError: If script file doesn't exist
        """
        plugin = self.get_plugin(system)
        if not plugin:
            available = ', '.join(self.plugins.keys())
            raise ValueError(
                f"System '{system}' not found. "
                f"Available systems: {available}"
            )
        return plugin.get_script_path(operation)

    def build_args(self, system: str, operation: str, task_data: Optional[Dict] = None, params: Optional[Dict] = None) -> List[str]:
        """Build command line arguments for an operation.

        Args:
            system: The system name (github, forgejo, todoist)
            operation: The operation name (create, update, sync, view, comment)
            task_data: Task data dictionary (contains systemData, etc.)
            params: Additional parameters to pass to the script

        Returns:
            List of command line arguments

        Raises:
            ValueError: If system not found or required args missing
        """
        plugin = self.get_plugin(system)
        if not plugin:
            available = ', '.join(self.plugins.keys())
            raise ValueError(
                f"System '{system}' not found. "
                f"Available systems: {available}"
            )
        return plugin.build_args(operation, task_data, params)

    def __repr__(self):
        return f"PluginRegistry({len(self.plugins)} plugins: {', '.join(self.plugins.keys())})"


# Global registry instance (singleton pattern)
_registry: Optional[PluginRegistry] = None


def get_registry(todu_root: Optional[Path] = None) -> PluginRegistry:
    """Get the global plugin registry (singleton).

    Args:
        todu_root: Optional path to todu root directory

    Returns:
        The global PluginRegistry instance
    """
    global _registry
    if _registry is None:
        _registry = PluginRegistry(todu_root)
    return _registry


def get_script_path(system: str, operation: str, todu_root: Optional[Path] = None) -> Path:
    """Convenience function to get script path.

    Args:
        system: The system name (github, forgejo, todoist)
        operation: The operation name (create, update, sync, view, comment)
        todu_root: Optional path to todu root directory

    Returns:
        Path to the script
    """
    return get_registry(todu_root).get_script_path(system, operation)


def get_available_systems(todu_root: Optional[Path] = None) -> List[Dict]:
    """Convenience function to get available systems.

    Args:
        todu_root: Optional path to todu root directory

    Returns:
        List of available systems with their info
    """
    return get_registry(todu_root).get_available_systems()
