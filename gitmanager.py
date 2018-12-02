import subprocess as sp
from sh.contrib import git
from sh import ErrorReturnCode as GitError

import core
from utils import log, log_exception


def get_commit_info():
    try:
        data = sp.check_output(['git', 'log', '-1', '--pretty=%H%n%an%n%s'], stderr=sp.STDOUT)
    except sp.CalledProcessError as e:
        log_exception(e)
        return
    full_id, author, message = data.decode('utf-8').strip().split("\n")
    return {'id': full_id[:7], 'full_id': full_id, 'author': author, 'message': message}


def is_same_commit(head_a, head_b):
    sha_a = str(git('rev-parse', head_a)).strip()
    sha_b = str(git('rev-parse', head_b)).strip()
    return sha_a == sha_b


def is_commit_pullable(ref):
    try:
        # git diff-tree --no-commit-id --name-only -r <>
        files = git('diff-tree', '--no-commit-id', '--name-only', '-r', ref.strip())
        files = str(files).split()
        return "noexec" in files
    except GitError as e:
        log_exception(e)
        return False


def pull_update():
    # Force pull update
    try:
        git.branch('-D', 'temp')
    except GitError:
        pass
    git.checkout('-b', 'temp', "origin/master")
    git.branch('-M', 'master')


def check_for_updates():
    try:
        git.remote.update()
        if not is_commit_pullable("origin/master"):
            return
        elif is_same_commit("HEAD", "origin/master"):
            return
        pull_update()
        commit_info = get_commit_info()
        log('info',
            "Pulled [{}] {}: {}".format(
                commit_info['id'], commit_info['author'], commit_info['message']))
    except Exception as e:
        log_exception(e)
