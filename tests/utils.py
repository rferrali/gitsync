import os
import shutil
from pathlib import Path
from dotenv import set_key

def clean_up():
    os.remove("gitsync.yaml")
    os.remove(".env")
    shutil.rmtree("assets", ignore_errors=True)
    shutil.rmtree("remote", ignore_errors=True)
    shutil.rmtree("tex", ignore_errors=True)

def initialize():
    clean_up()
    shutil.copyfile("gitsync/data/gitsync.yaml", "gitsync.yaml")
    env_file = Path(".env")
    env_file.touch(mode=0o600, exist_ok=False)
    set_key(env_file, "GITSYNC_ARTICLE", "./remote/article")
    os.mkdir("remote")
    os.mkdir("remote/article")
    os.mkdir("tex")
    os.mkdir("tex/article")
