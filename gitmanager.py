import os
import subprocess as sp
from sh.contrib import git
from sh import ErrorReturnCode as GitError

import core
from utils import log, log_exception


def get_commit_info(ref='HEAD'):
    try:
        data = sp.check_output(['git', 'log', '-1', '--pretty=%H%n%an%n%s', ref], stderr=sp.STDOUT)
    except sp.CalledProcessError as e:
        log_exception(e)
        return None
    full_id, author, message = data.decode('utf-8').strip().split("\n")
    commit_info = {'id': full_id[:7], 'full_id': full_id, 'author': author, 'message': message}
    return commit_info


def is_same_commit(head_a, head_b):
    sha_a = str(git('rev-parse', head_a)).strip()
    sha_b = str(git('rev-parse', head_b)).strip()
    return sha_a == sha_b


def is_commit_pullable(ref):
    try:
        # git diff-tree --no-commit-id --name-only -r <>
        files = git('diff-tree', '--no-commit-id', '--name-only', '-r', ref.strip())
        files = str(files).split()
        return "noexec" not in files
    except GitError as e:
        log_exception(e)
        return False


def pull_update():
    # Force pull update
    try:
        git.branch('-D', 'temp')
    except GitError:
        pass
    git.checkout('-b', 'temp', "origin/deploy")
    git.branch('-M', 'deploy')
    os._exit(0)


def check_for_updates():
    try:
        git.remote.update()
        if is_same_commit("HEAD", "origin/deploy"):
            return
        elif not is_commit_pullable("origin/deploy"):
            return
        commit_info = get_commit_info("origin/deploy")
        log('info',
            "Pulling [{}] {}: {}".format(
                commit_info['id'], commit_info['author'], commit_info['message']))
        pull_update()
    except Exception as e:
        log_exception(e)
