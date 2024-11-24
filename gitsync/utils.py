from dotenv import dotenv_values
from pathlib import Path
from importlib.resources import files
from yaml import safe_load
from filecmp import dircmp
import os
from shutil import copytree, rmtree
import click

def read_config():
    # check if config file exists
    config_file = Path("gitsync.yaml")
    if not config_file.exists():
        raise click.ClickException(f"\u274c Config file not found. Perhaps you didn't run 'gitsync create'? Or you're not using gitsync at the root of the local directory.")
    # check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        raise click.ClickException(f"\u274c .env file not found. Perhaps you didn't run 'gitsync create'? Or you're not using gitsync at the root of the local directory.")
    env = dotenv_values(env_file)
    # check if config file is valid
        # can it be loaded? 
    try:
        with config_file.open() as f:
            config = safe_load(f)
    except Exception as e:
        raise click.ClickException(f"\u274c Config file is not a well-formatted yaml.\n{e}")
        # do the paths exist?
    try: 
        assets = Path(config['assets'])
    except KeyError:
        raise click.ClickException(f"\u274c The config file must contain a key named 'assets' that points to the assets directory")
    if not assets.exists():
        raise click.ClickException(f"\u274c Assets directory not found: {config['assets']}")
    try: 
        dirty_projects = config['projects']
    except KeyError:
        raise click.ClickException(f"\u274c The config file must contain a key named 'projects' that contains the names and local paths of each project")
    projects = []
    for d_name, d_local in dirty_projects.items():
        local = Path(d_local)
        if not local.exists():
            raise click.ClickException(f"\u274c Project {d_name}: local directory not found: {d_local}")
        try: 
            remote = env['GITSYNC_' + d_name.upper()]
        except KeyError:
            raise click.ClickException(f"\u274c .env does not contain a remote path for project {d_name}. Set a variable named GITSYNC_{d_name.upper()} in your .env file (mind the case).")
        if not Path(remote).exists():
            raise click.ClickException(f"\u274c Project {d_name}: remote directory not found: {remote}")
        assets_link_path = local.joinpath(assets.name)
        if not assets_link_path.exists():
            click.echo(f"\u2757 Project {d_name}: the local folder does not contain a symlink pointing to the assets library")
            if click.confirm("Do you want to create one?", abort=True):
                assets_link_path.symlink_to(assets.absolute(), target_is_directory=True)
        if not assets_link_path.is_symlink(): 
            click.echo(f"\u2757 Project {d_name}: {assets_link_path} is not a symlink pointing to the assets library")
            if click.confirm("Do you want to delete this folder and create a symlink instead?", abort=True):
                rmtree(assets_link_path, ignore_errors=True)
                assets_link_path.symlink_to(assets.absolute(), target_is_directory=True)
        if not assets_link_path.resolve().absolute() == assets.absolute():
            click.echo(f"\u2757 Project {d_name}: the {assets_link_path} symlink does not point to the assets library")
            if click.confirm("Do you want to fix this symlink?", abort=True):
                assets_link_path.unlink()
                assets_link_path.symlink_to(assets.absolute(), target_is_directory=True)
        project = {
            'name': d_name, 
            'local': d_local,
            'remote': remote
        }
        projects.append(project)
    config["projects"] = projects
    return config

def check_push(local, remote, assets):
    compare = dircmp(local, remote)
    # extract folder name from assets path
    assets = Path(assets).name
    return diff_files(compare, local, remote, assets)

def diff_files(dcmp, local, remote, assets, name=''):
    out = {
        "right_only": [],
        "diff_files": []
    }
    for v in dcmp.right_only:
        # ignore assets folder in root
        if name == '' and v == assets:
            continue
        out["right_only"].append(os.path.join(name, v))
    for v in dcmp.diff_files:
        v = os.path.join(name, v)
        local_path = os.path.join(local, v)
        remote_path = os.path.join(remote, v)
        # if remote is more recent than local, add to diff_files
        if os.path.getmtime(remote_path) > os.path.getmtime(local_path):
            out["diff_files"].append(v)
    for sub_name, sub_dcmp in dcmp.subdirs.items():
        # ignore assets folder in root
        if name == '' and sub_name == assets:
            continue
        o = diff_files(sub_dcmp, local, remote, assets, os.path.join(name, sub_name))
        out["right_only"].extend(o["right_only"])
        out["diff_files"].extend(o["diff_files"])
    return out

# copy contents of local to remote
def push_project(local, remote):
    rmtree(remote, ignore_errors=True)
    copytree(local, remote)

def pull_project(local, remote, assets):
    rmtree(local, ignore_errors=True)
    copytree(remote, local)
    assets_path = Path(assets)
    assets_link_path = Path(local).joinpath(assets_path.name)
    rmtree(assets_link_path, ignore_errors=True)
    assets_link_path.symlink_to(assets_path.absolute(), target_is_directory=True)