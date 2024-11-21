import click
from dotenv import set_key
from pathlib import Path
import shutil
from importlib.resources import files
import gitsync.utils as utils

@click.group()
def cli():
    pass

@click.command()
def push():
    """Push projects to their remote directories."""
    click.echo(f"Pushing projects to their remote directories...")
    config = utils.read_config()
    for project in config['projects']:
        click.echo(f"Project {project['name']}")
        click.echo(f"  Pushing {project['local']} to {project['remote']}...")
        # compare local and remote
        check = utils.check_push(project['local'], project['remote'], config['assets'])
        if len(check['right_only']) > 0 or len(check['diff_files']) > 0:
            click.echo(f"  Pushing may delete some content you need in the remote directory.")
            if len(check['right_only']) > 0:
                click.echo(f"  These files and foldersare not in local:")
                for f in check['right_only']:
                    click.echo(f"    {f}")
            if len(check['diff_files']) > 0:
                click.echo(f"  These files are more recent in remote:")
                for f in check['diff_files']:
                    click.echo(f"    {f}")
            # click.confirm("Are you sure you want to push?", abort=True)
        utils.push_project(project['local'], project['remote'])
    click.echo(f"Done!")

@click.command()
def create():
    """Initialize a repo"""
    click.echo(f"Initializing...")
    env_file = Path(".env")
    config_file = Path("gitsync.json")
    # Create the gitsync.json file if it does not exist.
    if config_file.exists():
        click.echo(f"Config file already exists. Skipping...")
        return
    shutil.copyfile(files('gitsync.data').joinpath('gitsync.json'), config_file)
    # Create the .env file if it does not exist.
    if not env_file.exists():
        click.echo(f"Creating .env file...")
        env_file.touch(mode=0o600, exist_ok=False)
    set_key(env_file, "GITSYNC_ARTICLE", "/some/path/to/article")
    click.echo(f"Done! Please update gitsync.json and .env with your own paths.")

cli.add_command(create)
cli.add_command(push)
