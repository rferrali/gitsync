import click
from dotenv import set_key
from pathlib import Path
import shutil
from importlib.resources import files

@click.group()
def cli():
    pass

@click.command()
def hello():
    """Simple program that greets."""
    click.echo(f"Hello!")

@click.command()
def create():
    """Initialize a repo"""
    click.echo(f"Initializing...")
    env_file = Path(".env")
    config_file = Path("gitsync.json")
    # Create the gitsync.json file if it does not exist.
    if not config_file.exists():
        shutil.copyfile(files('gitsync.data').joinpath('gitsync.json'), config_file)
    # Create the .env file if it does not exist.
    if not env_file.exists():
        env_file.touch(mode=0o600, exist_ok=False)
    # Save some values to the file.
    set_key(dotenv_path=env_file, key_to_set="USERNAME", value_to_set="Romain")
    set_key(dotenv_path=env_file, key_to_set="EMAIL", value_to_set="abc@gmail.com")

cli.add_command(create)
cli.add_command(hello)
