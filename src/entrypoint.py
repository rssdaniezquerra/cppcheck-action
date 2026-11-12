import os
import re
import shlex
import subprocess as sp
import sys


GITHUB_EVENT_NAME = os.environ['GITHUB_EVENT_NAME']

# Set repository
CURRENT_REPOSITORY = os.environ['GITHUB_REPOSITORY']
# TODO: How about PRs from forks?
TARGET_REPOSITORY = os.environ['INPUT_TARGET_REPOSITORY'] or CURRENT_REPOSITORY
PULL_REQUEST_REPOSITORY = os.environ['INPUT_PULL_REQUEST_REPOSITORY'] or TARGET_REPOSITORY
REPOSITORY = PULL_REQUEST_REPOSITORY if GITHUB_EVENT_NAME == 'pull_request' else TARGET_REPOSITORY

# Set branches
GITHUB_REF = os.environ['GITHUB_REF']
print("GITHUB_REF: " + GITHUB_REF)
GITHUB_HEAD_REF = os.environ['GITHUB_HEAD_REF']
print("GITHUB_HEAD_REF: " + GITHUB_HEAD_REF)
GITHUB_BASE_REF = os.environ['GITHUB_BASE_REF']
CURRENT_BRANCH = GITHUB_HEAD_REF or '/'.join(GITHUB_REF.rsplit('/', 1)[2:])
TARGET_BRANCH = os.environ['INPUT_TARGET_BRANCH'] or CURRENT_BRANCH
PULL_REQUEST_BRANCH = os.environ['INPUT_PULL_REQUEST_BRANCH'] or GITHUB_BASE_REF
BRANCH = PULL_REQUEST_BRANCH if GITHUB_EVENT_NAME == 'pull_request' else TARGET_BRANCH

GITHUB_ACTOR = os.environ['GITHUB_ACTOR']
GITHUB_REPOSITORY_OWNER = os.environ['GITHUB_REPOSITORY_OWNER']
GITHUB_TOKEN = os.environ['INPUT_GITHUB_TOKEN']

# command related inputs

CHECK_LIBRARY = os.environ['INPUT_CHECK_LIBRARY'] or 'disable'
SKIP_PREPROCESSOR = os.environ['INPUT_SKIP_PREPROCESSOR'] or 'disable'
ENABLE = os.environ['INPUT_ENABLE'] or 'all'
EXCLUDE_CHECK = os.environ['INPUT_EXCLUDE_CHECK'] or 'disable'
INCONCLUSIVE = os.environ['INPUT_INCONCLUSIVE'] or 'enable'
INLINE_SUPPRESSION = os.environ['INPUT_INLINE_SUPPRESSION'] or 'disable'
FORCE_LANGUAGE = os.environ['INPUT_FORCE_LANGUAGE'] or 'disable'
MAX_CTU_DEPTH = os.environ['INPUT_MAX_CTU_DEPTH'] or 'disable'
OUTPUT_FILE = os.environ['INPUT_OUTPUT_FILE'] or 'cppcheck_report.txt'
PLATFORM = os.environ['INPUT_PLATFORM'] or 'disable'
STD = os.environ.get('INPUT_STD') or 'c++17'
# Severities that make the job fail (comma separated). "none" never fails
FAIL_ON = os.environ.get('INPUT_FAIL_ON') or 'error,warning'
# Checks to suppress (comma separated, each as cppcheck --suppress takes it: id, id:file or id:file:line). "none" keeps all
SUPPRESS = os.environ.get('INPUT_SUPPRESS') or 'missingInclude,missingIncludeSystem'

command = ""


def prepare_command():
    global command
    global out_file
    command = command + "cppcheck "
    # check every flags

    if CHECK_LIBRARY == 'enable':
        command = command + " --check-library"

    if SKIP_PREPROCESSOR == 'enable':
        command = command + " --E"

    enable_val = 'all'  # default fallback value

    if ENABLE == 'warning':
        enable_val = 'warning'
    elif ENABLE == 'style':
        enable_val = 'style'
    elif ENABLE == 'performance':
        enable_val = 'performance'
    elif ENABLE == 'portability':
        enable_val = 'portability'
    elif ENABLE == 'information':
        enable_val = 'information'
    elif ENABLE == 'unusedFunction':
        enable_val = "unusedFunction"
    elif ENABLE == 'missingInclude':
        enable_val = 'missingInclude'

    # multiple checks ; comma separated , skipping additional error checking
    if ',' in ENABLE:
        enable_val = ENABLE

    command = command + f" --enable={enable_val}"

    if EXCLUDE_CHECK != 'disable':
        command = command + f" -i {EXCLUDE_CHECK}"
        # assuming user passes a valid path
    if INCONCLUSIVE != 'disable':
        command = command + ' --inconclusive'

    if INLINE_SUPPRESSION == "enable":
        command = command + " --inline-suppr"

    if FORCE_LANGUAGE != 'disable':
        command = command + f" --language={FORCE_LANGUAGE}"
    if MAX_CTU_DEPTH != 'disable':
        command = command + f" --max-ctu-depth={MAX_CTU_DEPTH}"

    if PLATFORM != 'disable':
        command = command + f" --platform={PLATFORM}"


    # C++ standard of the checked code (the leading space matters: it used to produce "--std=c++14--library=qt",
    # which cppcheck >= 2.14 rejects, so no analysis ran at all)
    command = command + f" --std={STD}"

    #Add support for qt libraries
    command = command + " --library=qt"

    for suppression in SUPPRESS.split(','):
        suppression = suppression.strip()

        if suppression and (suppression != 'none'):
            command = command + f" --suppress={shlex.quote( suppression )}"

    out_file = OUTPUT_FILE


def run_cppcheck():
    """Runs cppcheck. Returns its exit code: non-zero means it could not analyse (bad option, crash...)."""
    global command
    command = command + f" --output-file={out_file} ."
    print("Running: " + command)
    return sp.call(command, shell=True)


def count_findings():
    """Counts the findings of the report whose severity is in FAIL_ON."""
    severities = [s.strip() for s in FAIL_ON.split(',') if s.strip() and s.strip() != 'none']
    if not severities:
        return 0

    pattern = re.compile(r'^[^:\s][^:]*:\d+:\d+: (' + '|'.join(map(re.escape, severities)) + r'):')
    found = 0

    with open(out_file, encoding='utf-8', errors='replace') as report:
        for line in report:
            if pattern.match(line):
                print(line.rstrip())
                found += 1

    return found


def commit_changes():
    """Commits changes.
    """
    set_email = 'git config --local user.email "flawfinder-action@master"'
    set_user = 'git config --local user.name "flawfinder-action"'

    sp.call(set_email, shell=True)
    sp.call(set_user, shell=True)

    print("target branch: "+TARGET_BRANCH)
    git_fetch = f'git fetch'
    git_stash = f'git stash'
    git_stash_pop = f'git stash pop'
    git_checkout = f'git checkout {TARGET_BRANCH}'
    git_main = f'git checkout main'
    git_add = f'git add {out_file}'
    git_commit = 'git commit -m "cppcheck report added/updated"'
    git_branch = f'git branch checker'
    git_merge = f'git merge checker'
    git_branch_del = f'git branch rm checker'
    print('Committing reports.......')

    #sp.call(git_checkout, shell=True)
    #sp.call(git_branch, shell=True)
    sp.call(git_stash, shell=True)
    sp.call(git_fetch, shell=True)
    sp.call(git_checkout, shell=True)
    sp.call(git_stash_pop, shell=True)
    sp.call(git_add, shell=True)
    sp.call(git_commit, shell=True)


def push_changes():
    """Pushes commit.
    """
    set_url = f'git remote set-url origin https://x-access-token:{GITHUB_TOKEN}@github.com/{TARGET_REPOSITORY}'
    git_push = f'git push origin {TARGET_BRANCH}'
    sp.call(set_url, shell=True)
    sp.call(git_push, shell=True)


def main():

    # It used to return here on every pull request whose author was not the repository owner (an organization
    # never opens pull requests), so the analysis never ran on pull requests

    prepare_command()
    cppcheck_result = run_cppcheck()

    if (cppcheck_result != 0) or (not os.path.isfile(out_file)):
        print(f"cppcheck failed (exit code {cppcheck_result}): no report was generated")
        sys.exit(1)

    findings = count_findings()

    commit_changes()
    push_changes()

    if findings > 0:
        print(f"cppcheck: {findings} finding(s) with severity in [{FAIL_ON}]. See {out_file}")
        sys.exit(1)

    print(f"cppcheck: no findings with severity in [{FAIL_ON}]")


if __name__ == '__main__':
    main()
