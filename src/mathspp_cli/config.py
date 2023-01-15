"""Module defining the command `mathspp config`."""

import configparser
from pathlib import Path

import typer


APP_NAME = "mathspp-cli"
CONFIG_FILE_NAME = "mathspp_cli.ini"
APP_DIR = Path(typer.get_app_dir(APP_NAME))
APP_DIR.mkdir(parents=True, exist_ok=True)  # Ensure app dir exists.
CONFIG_PATH = APP_DIR / CONFIG_FILE_NAME

app = typer.Typer()


def default_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config["site"] = {"path": ""}
    return config


def ensure_config() -> None:
    """Ensure there is a config file. Write defaults if not."""
    config_path = CONFIG_PATH
    if not config_path.exists():
        write_config(default_config())


def write_config(config: configparser.ConfigParser) -> None:
    config_path = CONFIG_PATH
    config_path.touch()
    with open(config_path, "w") as config_file:
        config.write(config_file)


def get_config() -> configparser.ConfigParser:
    config_path = CONFIG_PATH
    ensure_config()
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


@app.command()
def read():
    """Read the current configuration."""
    config = get_config()
    for section in config.sections():
        print(f"[{section}]")
        for key, value in config[section].items():
            print(f"{key}: {value!r}")


@app.command()
def path():
    """Get the path to the configuration file."""
    print(CONFIG_PATH)


@app.command()
def set(
    path: Path = typer.Option(None, help="Path to the site directory."),
):
    """Set configuration values."""

    config = get_config()
    if path is not None:
        assert path.exists()
        config["site"]["path"] = str(path)
    write_config(config)
