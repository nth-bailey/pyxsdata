from contextlib import suppress
from importlib import metadata


def load_entry_points(name: str) -> None:
    """Load the plugins for the given hook name."""
    entry_points = metadata.entry_points()

    if hasattr(entry_points, "select"):
        plugins = entry_points.select(group=name)
    else:
        plugins = entry_points.get(name, [])

    for plugin in plugins:
        with suppress(Exception):
            plugin.load()
