import os
import shutil
from git import Repo

def push(repo_url, local_repo_path, target_folder):
    # Clone or update repo
    if not os.path.exists(local_repo_path):
        Repo.clone_from(repo_url, local_repo_path)
    else:
        repo = Repo(local_repo_path)
        repo.git.pull()

    # Sync to target folder
    if os.path.exists(target_folder):
        shutil.rmtree(target_folder)
    shutil.copytree(local_repo_path, target_folder)