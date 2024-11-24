import click
from dotenv import set_key
from pathlib import Path
import shutil
from importlib.resources import files
import gitsync.utils as utils
from git import Repo, InvalidGitRepositoryError

@click.group()
def cli():
    pass

@click.command()
def push():
    """Push projects to their remote directories."""
    click.echo(f"Pushing projects to their remote directories...")
    config = utils.read_config()
    is_git_repo = True
    try: 
        repo = Repo()
    except InvalidGitRepositoryError:
        click.echo(f"This is not a Git repository")
        is_git_repo = False
    if is_git_repo:
        # check if we're on the main branch
        if repo.active_branch.name != 'main':
            click.confirm(f"You are about to push content from branch {repo.active_branch.name} instead of the main branch. Do you want to continue?", abort=True)
        if repo.is_dirty():
            click.confirm(f"You are about to push content that has not been committed. Do you want to continue?", abort=True)
        # check if we're on the latest commit
        remote = repo.remote()
        remote.fetch()
        if repo.head.commit != remote.refs[0].commit:
            click.confirm(f"You are behind the latest commit. You might be pushing content that is not up to date. Do you want to continue?", abort=True)
    ok = True
    for project in config['projects']:
        click.echo(f"Project {project['name']}: checking that everything is ok...")
        # compare local and remote
        check = utils.check_push(project['local'], project['remote'], config['assets'])
        if len(check['right_only']) > 0 or len(check['diff_files']) > 0:
            ok = False
            click.echo(f"  Pushing may delete some content you need in the remote directory.")
            if len(check['right_only']) > 0:
                click.echo(f"  These files and directories are not in local:")
                for f in check['right_only']:
                    click.echo(f"    {f}")
            if len(check['diff_files']) > 0:
                click.echo(f"  These files are more recent in remote:")
                for f in check['diff_files']:
                    click.echo(f"    {f}")
    if not ok:
        click.confirm("Are you sure you want to push?", abort=True)
    for project in config['projects']:
        click.echo(f"Project {project['name']}: pushing {project['local']} to {project['remote']}")
        utils.push_project(project['local'], project['remote'])
    click.echo(f"Done!")

@click.command()
def pull():
    """Pull projects from their remote directories."""
    click.echo(f"Pulling projects from their remote directories...")
    is_git_repo = True
    try: 
        repo = Repo()
    except InvalidGitRepositoryError:
        click.echo(f"This is not a Git repository")
        is_git_repo = False
    if is_git_repo:
        # check if repo is dirty
        if repo.is_dirty():
            click.confirm(f"The repo has changes that have not been committed. Pulling may overwrite them. Do you want to continue?", abort=True)
    config = utils.read_config()
    for project in config['projects']:
        click.echo(f"Project {project['name']}")
        click.echo(f"  Pulling {project['remote']} to {project['local']}...")
        utils.pull_project(project['local'], project['remote'], config['assets'])
    click.echo(f"Done!")

@click.command()
def create():
    """Initialize a repo"""
    click.echo(f"Initializing...")
    env_file = Path(".env")
    config_file = Path("gitsync.yaml")
    # Create the gitsync.yaml file if it does not exist.
    if config_file.exists():
        click.echo(f"Config file already exists. Skipping...")
        return
    shutil.copyfile(files('gitsync.data').joinpath('gitsync.yaml'), config_file)
    # Create the .env file if it does not exist.
    if not env_file.exists():
        click.echo(f"Creating .env file...")
        env_file.touch(mode=0o600, exist_ok=False)
    set_key(env_file, "GITSYNC_ARTICLE", "/some/path/to/article")
    click.echo(f"Done! Please update gitsync.yaml and .env with your own paths.")

cli.add_command(create)
cli.add_command(push)
cli.add_command(pull)
