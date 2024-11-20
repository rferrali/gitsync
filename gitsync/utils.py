from dotenv import dotenv_values
from pathlib import Path
from importlib.resources import files
import json
from jsonschema import validate
from filecmp import dircmp
import os

def read_config():
    # check if config file exists
    config_file = Path("gitsync.json")
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found. Please create it using 'gitsync create'")
    # check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        raise FileNotFoundError(f".env file not found. Please create it using 'gitsync create'")
    env = dotenv_values(env_file)
    # check if config file is a valid json
        # can it be loaded? 
    try:
        with config_file.open() as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Config file is not a well-formatted json. Error: {e}")
        # does it conform to the schema? 
    schema_file = files('gitsync.data').joinpath('gitsync.schema.json')
    with schema_file.open() as f:
        schema = json.load(f)
    validate(config, schema)
        # do the paths exist?
    if not Path(config['assets']).exists():
        raise FileNotFoundError(f"Assets directory not found: {config['assets']}")
    for project in config['projects']:
        if not Path(project['local']).exists():
            raise FileNotFoundError(f"Project {project['name']}: local directory not found: {project['local']}")
    for project in config['projects']:
        try: 
            remote = env['GITSYNC_' + project['name'].upper()]
        except KeyError:
            raise KeyError(f".env does not contain a remote path for project {project['name']}. Set a variable named GITSYNC_{project['name'].upper()} in your .env file.")
        if not Path(remote).exists():
            raise FileNotFoundError(f"Project {project['name']}: remote directory not found: {remote}")
        project['remote'] = remote
    return config

def check_push(local, remote):
    compare = dircmp(local, remote)
    return diff_files(compare, local, remote)

def diff_files(dcmp, local, remote, name = ''):
    out = {
        "right_only": [],
        "diff_files": []
    }
    for v in dcmp.right_only:
        out["right_only"].append(os.path.join(name, v))
    for v in dcmp.diff_files:
        v = os.path.join(name, v)
        local_path = os.path.join(local, v)
        remote_path = os.path.join(remote, v)
        # if remote is more recent than local, add to diff_files
        if os.path.getmtime(remote_path) > os.path.getmtime(local_path):
            out["diff_files"].append(v)
    for sub_name, sub_dcmp in dcmp.subdirs.items():
        o = diff_files(sub_dcmp, local, remote, os.path.join(name, sub_name))
        out["right_only"].extend(o["right_only"])
        out["diff_files"].extend(o["diff_files"])
    return out