import subprocess

GITHUB_USERNAME = "your-github-username"
REPO_NAME = "Venture_Launcher_Tasks"
REMOTE_NAME = "push_url"
BRANCH_NAME = "main"
COMMIT_MESSAGE = "Update Venture Launcher Tasks"

github_url = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"


def run(command):
    subprocess.run(command, check=True)


# initialize git
run(["git", "init"])

# add all files
run(["git", "add", "."])

# commit changes
try:
    run(["git", "commit", "-m", COMMIT_MESSAGE])
except subprocess.CalledProcessError:
    print("Nothing to commit, or commit failed. Continuing...")

# add or update remote named push_url
remotes = subprocess.run(
    ["git", "remote"],
    capture_output=True,
    text=True
).stdout.split()

if REMOTE_NAME in remotes:
    run(["git", "remote", "set-url", REMOTE_NAME, github_url])
else:
    run(["git", "remote", "add", REMOTE_NAME, github_url])

# make sure branch is main
run(["git", "branch", "-M", BRANCH_NAME])

# force push
run(["git", "push", "--force", "-u", REMOTE_NAME, BRANCH_NAME])