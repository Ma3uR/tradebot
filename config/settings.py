"""
settings.py

This file contains functions for loading and updating settings from a JSON file.

Functions:
- load_settings: Load settings from a JSON file.
- update_settings: Update settings for a specific strategy.
"""

import json
import logging
from pathlib import Path
from typing import Any
from os import path

logger = logging.getLogger('app.settings')

ROOT_PATH = path.dirname(path.realpath(__file__))

_PATH_TO_SETTINGS = Path(
    str(Path(__file__).parent)
    + '/settings.json'
)


def load_settings() -> dict[str, Any]:
    """
    Load settings from a JSON file.

    Returns:
        A dictionary containing the settings.

    Raises:
        FileNotFoundError: If the settings file doesn't exist.
    """

    if not _PATH_TO_SETTINGS.exists():
        raise FileNotFoundError(
            f'File "{_PATH_TO_SETTINGS}" doesn\'t exist. '
            f'Put file with settings into "config" directory.'
        )

    with open(_PATH_TO_SETTINGS, 'r') as settings_file:
        settings = json.load(settings_file)

    return settings


def update_settings(
        strategy_name: str,
        new_settings: dict[str, Any],
) -> None:
    """
    Update settings for a specific strategy.

    Args:
        strategy_name (str): The name of the strategy.
        new_settings (dict[str, Any]): The new settings for the strategy.

    Returns:
        None
    """

    settings = load_settings()
    settings['strategies'][strategy_name] = new_settings

    with open(_PATH_TO_SETTINGS, 'w') as settings_file:
        json.dump(settings, settings_file, indent=2)
