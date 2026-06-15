# Git Reference

A practical reference for git. Definitions first, then common workflows at the bottom.

---

## Core Concepts

**Repository (repo):** A directory tracked by git. Contains your files plus a hidden `.git/` folder that stores the entire history.

**Commit:** A snapshot of your tracked files at a point in time. Every commit has a unique hash (e.g. `a3f92c1`), a message, a timestamp, and a pointer to the previous commit.

**Staging area (index):** A buffer between your working directory and commits. You explicitly add changes to staging before committing. This lets you commit only part of your current changes.

**Branch:** A named pointer to a commit. Creating a branch lets you diverge from the main line of development without affecting it. `main` (or `master`) is the default branch.

**HEAD:** A pointer to whatever commit you currently have checked out. Usually points to the tip of your current branch. "Detached HEAD" means HEAD points to a specific commit instead of a branch.

**Remote:** A version of the repo hosted elsewhere (GitHub, GitLab, etc.). `origin` is the conventional name for the remote you cloned from.

**Tracking branch:** A local branch linked to a remote branch. `git push` and `git pull` use this link to know where to send/receive changes.

**Working tree:** The actual files on disk that you edit. Separate from what's staged and what's committed.

---

## Command Reference

### Setup

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```
Set your identity. This attaches your name and email to every commit you make. Run once after installing git.

```bash
git init
```
Initialize a new repo in the current directory. Creates the `.git/` folder.

```bash
git clone <url>
```
Download a remote repo to your local machine and set `origin` to point at `<url>`.

---

### Staging and Committing

```bash
git status
```
Show which files are modified, staged, or untracked. Run this constantly. It tells you exactly what git sees.

```bash
git add <file>  # specific
git add .       # all 
```
Stage a specific file, or stage all changes in the current directory. Files must be staged before they can be committed.

```bash
git diff
git diff --staged
```
Show unstaged changes (vs. last commit), or staged changes (vs. what will be in the next commit).

```bash
git commit -m "message"
```
Create a commit with everything currently staged. The message should say what changed and why, not just what files were touched.

```bash
git commit --amend -m "message" # modifies just message
git commit --amend              # general
```
Rewrite the most recent commit. Adds any staged changes and lets you edit the message. Only use this before pushing. Amending a pushed commit causes problems for anyone who pulled it.

---

### Branches

```bash
git branch
git branch -a
```
List local branches, or list all branches including remote-tracking ones.

```bash
git branch <name>
```
Create a new branch at the current commit. Does not switch to it.

```bash
git checkout <branch>
git switch <branch>
```
Switch to a branch. `switch` is the modern version; `checkout` also works and is more common in older docs.

```bash
git checkout -b <name>
git switch -c <name>
```
Create a new branch and switch to it in one step.

```bash
git branch -d <name>
```
Delete a branch. Git refuses if the branch has unmerged changes. Use `-D` to force delete.

```bash
git branch -m <branch>
```
Rename a branch. Replace "<branch>" with the new name.

```bash
git merge <branch>
```
Merge `<branch>` into your current branch. Creates a merge commit if the histories have diverged.

```bash
git rebase <branch>
```
Replay your current branch's commits on top of `<branch>`. Produces a linear history. Do not rebase commits that have been pushed to a shared remote.

---

### Remotes

```bash
git remote -v
```
List remotes and their URLs.

```bash
git remote add origin <url>
```
Add a remote named `origin` pointing to `<url>`. Do this after `git init` to connect a local repo to GitHub.

```bash
git remote set-url origin <url>
```
Change the URL of an existing remote. Useful if you renamed a repo or switched from HTTPS to SSH.

```bash
git fetch
git fetch origin
```
Download changes from the remote without merging them into your local branch. Updates remote-tracking branches (e.g. `origin/main`) but doesn't touch your working tree.

```bash
git pull
git pull origin main
```
Fetch and immediately merge (or rebase) into your current branch. Equivalent to `git fetch` followed by `git merge`.

```bash
git push
git push origin main
git push -u origin main
```
Push your current branch to the remote. `-u` sets the upstream tracking link so future `git push` calls don't need the branch name.

```bash
git push --force-with-lease
```
Force push but only if the remote matches what you last fetched. Safer than `--force` because it won't silently overwrite someone else's commits.

---

### Inspecting History

```bash
git log
git log --oneline
git log --oneline --graph --all
```
Show commit history. `--oneline` is compact. `--graph --all` shows a visual branch graph across all branches.

```bash
git show <hash>
```
Show the changes introduced by a specific commit.

```bash
git blame <file>
```
Show which commit last modified each line of a file. Useful for tracking down when and why something changed.

```bash
git log -p <file>
```
Show the full diff history of a specific file.

---

### Undoing Things

```bash
git restore <file>
```
Discard unstaged changes to a file. Reverts it to the last commit. Permanent.

```bash
git restore --staged <file>
```
Unstage a file without discarding the changes. The edits remain in your working tree.

```bash
git reset HEAD~1
```
Undo the last commit but keep the changes staged. The commit disappears; the work stays.

```bash
git reset --hard HEAD~1
```
Undo the last commit and discard all changes. The commit and the work both disappear. Permanent.

```bash
git revert <hash>
```
Create a new commit that undoes the changes from `<hash>`. Safe for shared history because it doesn't rewrite commits.

```bash
git stash
git stash pop
```
Temporarily shelve uncommitted changes so you can switch branches. `pop` restores them.

---

### Tagging

```bash
git tag v1.0
git tag -a v1.0 -m "Release 1.0"
```
Mark a specific commit with a label. Annotated tags (`-a`) include a message and are recommended for releases.

```bash
git push origin --tags
```
Push all tags to the remote. Tags are not pushed by default with `git push`.

---

### Useful Utilities

```bash
git grep "search term"
```
Search the contents of tracked files. Faster than regular grep for repos.

```bash
git clean -fd
```
Delete all untracked files and directories. Useful for clearing build artifacts. Permanent.

```bash
git bisect start
git bisect bad
git bisect good <hash>
```
Binary search through commit history to find which commit introduced a bug. Git checks out commits in the middle of the range; you mark each as `good` or `bad` until it finds the culprit.

---

## .gitignore

A `.gitignore` file lists patterns for files git should never track. One per repo, committed alongside the code.

Common entries:
```
__pycache__/
*.pyc
.env
.DS_Store
*.egg-info/
dist/
.ipynb_checkpoints/
wandb/
```

Use `git check-ignore -v <file>` to diagnose why a file is or isn't being ignored.

---

## In Practice

### Create a new local repo and push it to GitHub

```bash
# 1. Create and enter the directory
mkdir my-project && cd my-project

# 2. Initialize git
git init

# 3. Create a first file
echo "# My Project" > README.md

# 4. Stage and commit
git add README.md
git commit -m "Initial commit"

# 5. Create the repo on GitHub (via browser or gh CLI)
gh repo create my-project --private --source=. --remote=origin

# 6. Push
git push -u origin main
```

---

### Connect an existing local repo to a new GitHub remote

```bash
# Run inside the existing repo directory
git remote add origin https://github.com/yourname/my-project.git
git push -u origin main
```

---

### Everyday feature workflow

```bash
# Start from an up-to-date main
git checkout main
git pull

# Create a branch for your work
git switch -c feature/my-thing

# Work, stage, commit in a loop
git add <files>
git commit -m "Add X"

# Push the branch to GitHub
git push -u origin feature/my-thing

# Open a pull request (on GitHub or via CLI)
gh pr create --title "Add X" --body "..."

# After the PR is merged, clean up
git checkout main
git pull
git branch -d feature/my-thing
```

---

### Fix the last commit before pushing

```bash
# Staged some additional changes
git add <forgotten file>
git commit --amend --no-edit    # keeps the same commit message
```

---

### Undo a commit you already pushed

```bash
# Safe: creates a new revert commit
git revert <hash>
git push

# Do NOT use git reset --hard on shared branches.
# It rewrites history and breaks everyone else's clones.
```

---

### Pull in changes from main while on a feature branch

```bash
# Option 1: merge (adds a merge commit)
git fetch origin
git merge origin/main

# Option 2: rebase (linear history, rewrites your commits)
git fetch origin
git rebase origin/main
# Only do this if your branch hasn't been pushed, or if you're the only one on it.
```

---

### Resolve a merge conflict

```bash
git merge origin/main
# git stops and marks conflicts in the affected files with <<<<<<< / =======/ >>>>>>>
# Open the file, edit it to the correct final state, remove the markers

git add <resolved-file>
git commit    # completes the merge
```

---

### Stash changes to switch context quickly

```bash
# You're mid-edit but need to switch branches
git stash

git checkout other-branch
# do whatever you need to do

git checkout -
git stash pop    # restores your work
```

---

### Check what's different between your branch and main

```bash
git diff main...HEAD                  # diff of all changes on your branch
git log main..HEAD --oneline          # commits your branch has that main doesn't
```
