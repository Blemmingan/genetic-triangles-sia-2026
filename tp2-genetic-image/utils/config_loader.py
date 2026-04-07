import argparse
import json
import os
from typing import Any, Dict


def load_config(config_path: str, cli_args: argparse.Namespace) -> Dict[str, Any]:
    """
    Loads default configuration from the provided JSON path and overrides
    variables dynamically with any provided CLI arguments.

    :param config_path: Path to the default configuration JSON file.
    :param cli_args: Parsed command-line arguments.
    :return: A dictionary containing the final configuration.
    """
    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)

    # Map CLI arg names to config keys if they differ
    arg_to_config_key = {
        "selection": "selection_method",
        "crossover": "crossover_method",
        "mutation": "mutation_method",
        "replacement": "replacement_method",
    }

    for key, value in vars(cli_args).items():
        # Override config only if the value was explicitly passed
        if value is not None and key not in ["config", "image"]:
            config_key = arg_to_config_key.get(key, key)
            config[config_key] = value

    return config
