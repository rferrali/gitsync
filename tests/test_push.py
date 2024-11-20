import os
from gitsync.push import push

def test_sync():
    # Test syncing a dummy repo to a folder
    repo_url = "https://github.com/someuser/somerepo.git"
    local_repo = "temp_repo"
    target_folder = "synced_folder"
    
    sync_repo_to_folder(repo_url, local_repo, target_folder)
    assert os.path.exists(target_folder)