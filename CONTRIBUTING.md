# Contributing to Speech-to-Text Light

Welcome! This guide will help you understand how to work with Git and contribute to this project. If you're new to Git or need a refresher on pulls, commits, merges, and branches, this guide is for you.

## Table of Contents

- [Understanding Git Basics](#understanding-git-basics)
- [Working with Branches](#working-with-branches)
- [Making Changes (Commits)](#making-changes-commits)
- [Syncing with Remote (Pulls and Pushes)](#syncing-with-remote-pulls-and-pushes)
- [Merging Changes](#merging-changes)
- [Pull Requests Workflow](#pull-requests-workflow)
- [Common Git Commands](#common-git-commands)
- [Troubleshooting](#troubleshooting)

## Understanding Git Basics

Git is a version control system that tracks changes to your code over time. Think of it as a sophisticated "undo" system with superpowers.

### Key Concepts

- **Repository (Repo)**: A project folder that Git is tracking. This Speech-to-Text-Light project is a repository.
- **Commit**: A snapshot of your changes at a specific point in time. Like saving a checkpoint in a game.
- **Branch**: A parallel version of your code where you can work independently. The default branch is usually called `main` or `master`.
- **Remote**: The version of your repository stored on GitHub (or another server).
- **Local**: The version of your repository on your computer.

## Working with Branches

Branches allow you to work on features or fixes without affecting the main codebase.

### Viewing Branches

To see all branches in your repository:

```bash
# List local branches
git branch

# List all branches (local and remote)
git branch -a

# See which branch you're currently on
git status
```

### Creating a New Branch

When starting new work, create a branch:

```bash
# Create and switch to a new branch
git checkout -b feature/my-new-feature

# Or using newer syntax
git switch -c feature/my-new-feature
```

**Branch Naming Conventions:**
- `feature/description` - for new features
- `fix/description` - for bug fixes
- `docs/description` - for documentation changes
- `refactor/description` - for code refactoring

### Switching Between Branches

To navigate between existing branches:

```bash
# Switch to an existing branch
git checkout branch-name

# Or using newer syntax
git switch branch-name

# Example: Switch back to main
git checkout main
```

**Important**: Always commit or stash your changes before switching branches!

### Checking Branch Status

Before switching branches, check your current state:

```bash
# See current branch and file changes
git status

# See the difference in your changes
git diff
```

## Making Changes (Commits)

Commits are how you save your work in Git.

### The Commit Workflow

1. **Make your changes** to files
2. **Stage** the changes (tell Git which files to include)
3. **Commit** the changes with a descriptive message

```bash
# 1. Check what files have changed
git status

# 2. Stage specific files
git add app.py
git add README.md

# Or stage all changed files
git add .

# 3. Commit with a message
git commit -m "Add new voice recognition feature"
```

### Writing Good Commit Messages

A good commit message:
- Starts with a verb (Add, Fix, Update, Remove, Refactor)
- Is concise but descriptive
- Explains *what* and *why*, not *how*

**Examples:**
- ✅ Good: `Fix audio playback issue on Safari browsers`
- ✅ Good: `Add support for DOCX file uploads`
- ❌ Bad: `Fixed stuff`
- ❌ Bad: `Updated code`

### Viewing Commit History

To see past commits:

```bash
# See recent commits
git log

# See a compact view
git log --oneline

# See last 10 commits
git log --oneline -10

# See commits with a visual branch graph
git log --graph --oneline --all
```

## Syncing with Remote (Pulls and Pushes)

Git has two copies: your local repository and the remote (on GitHub). You need to keep them in sync.

### Push: Upload Your Changes

After committing locally, push to share your work:

```bash
# Push your current branch to GitHub
git push

# First time pushing a new branch
git push -u origin branch-name
```

### Pull: Download Changes

Get the latest changes from GitHub:

```bash
# Pull changes from the current branch
git pull

# Pull changes from a specific branch
git pull origin main
```

**What `git pull` does:**
1. Downloads (fetches) changes from GitHub
2. Automatically merges them into your current branch

### Fetch: Check What's New

Sometimes you want to see changes without merging them:

```bash
# Download info about changes without merging
git fetch

# See what's new
git log HEAD..origin/main
```

## Merging Changes

Merging combines changes from different branches.

### Basic Merge

To merge another branch into your current branch:

```bash
# First, switch to the branch you want to merge INTO
git checkout main

# Then merge the other branch
git merge feature/my-feature
```

### Merge Conflicts

Sometimes Git can't automatically combine changes. You'll see a message like:

```
CONFLICT (content): Merge conflict in app.py
```

**To resolve:**

1. Open the conflicted file(s)
2. Look for conflict markers:
```python
<<<<<<< HEAD
# Your current code
=======
# Incoming code
>>>>>>> feature/my-feature
```
3. Edit to keep what you want
4. Remove the conflict markers
5. Stage and commit:
```bash
git add app.py
git commit -m "Resolve merge conflict in app.py"
```

### Checking Merge Status

```bash
# See if you're in the middle of a merge
git status

# Abort a merge if you need to start over
git merge --abort
```

## Pull Requests Workflow

Pull Requests (PRs) are how you propose changes to the project on GitHub.

### Standard PR Workflow

1. **Create a branch** for your work:
   ```bash
   git checkout -b feature/awesome-feature
   ```

2. **Make changes and commit** them:
   ```bash
   git add .
   git commit -m "Add awesome feature"
   ```

3. **Push to GitHub**:
   ```bash
   git push -u origin feature/awesome-feature
   ```

4. **Open a Pull Request** on GitHub:
   - Go to the repository on GitHub
   - Click "Pull requests" → "New pull request"
   - Select your branch
   - Add a title and description
   - Click "Create pull request"

5. **Review and merge**:
   - Others review your code
   - Make requested changes if needed
   - Once approved, merge the PR on GitHub

6. **Clean up** after merge:
   ```bash
   # Switch back to main
   git checkout main
   
   # Pull the merged changes
   git pull
   
   # Delete your local branch (optional)
   git branch -d feature/awesome-feature
   ```

## Common Git Commands

### Quick Reference

```bash
# Check status
git status

# See changes
git diff

# Stage files
git add <file>
git add .

# Commit
git commit -m "message"

# Push
git push

# Pull
git pull

# Create branch
git checkout -b new-branch

# Switch branch
git checkout branch-name

# List branches
git branch

# Merge branch
git merge branch-name

# View history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard changes to a file
git checkout -- <file>

# Stash changes temporarily
git stash
git stash pop
```

## Troubleshooting

### "I'm on the wrong branch!"

```bash
# If you haven't committed yet, stash your changes
git stash

# Switch to the correct branch
git checkout correct-branch

# Apply your changes
git stash pop
```

### "I committed to the wrong branch!"

```bash
# Copy the commit to the correct branch
git checkout correct-branch
git cherry-pick <commit-hash>

# Go back and remove it from the wrong branch
git checkout wrong-branch
git reset --hard HEAD~1
```

### "I need to undo my last commit"

```bash
# Keep the changes but undo the commit
git reset --soft HEAD~1

# Discard the commit AND the changes (careful!)
git reset --hard HEAD~1
```

### "My branch is behind the main branch"

```bash
# Update your branch with main's changes
git checkout your-branch
git merge main

# Or use rebase for a cleaner history
git checkout your-branch
git rebase main
```

### "I have merge conflicts"

1. Open the conflicted files
2. Find the `<<<<<<<`, `=======`, and `>>>>>>>` markers
3. Keep the code you want
4. Remove the markers
5. Stage and commit:
```bash
git add .
git commit -m "Resolve merge conflicts"
```

### "I want to see what changed between branches"

```bash
# See differences between branches
git diff main..feature-branch

# See just the file names
git diff --name-only main..feature-branch
```

### "I accidentally deleted important changes"

```bash
# See your recent actions
git reflog

# Restore to a previous state
git checkout <commit-hash>

# Or create a new branch from that point
git checkout -b recovery <commit-hash>
```

## Best Practices

1. **Commit often**: Make small, focused commits rather than one giant commit
2. **Pull before you push**: Always pull the latest changes before pushing your work
3. **Use descriptive branch names**: `feature/add-pdf-support` is better than `temp-branch`
4. **Write clear commit messages**: Your future self will thank you
5. **Test before committing**: Make sure your code works before committing
6. **Keep commits focused**: One commit should address one thing
7. **Don't commit secrets**: Never commit API keys, passwords, or sensitive data

## Learning Resources

- [Git Official Documentation](https://git-scm.com/doc)
- [GitHub Git Guides](https://github.com/git-guides)
- [Interactive Git Tutorial](https://learngitbranching.js.org/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

## Getting Help

If you're stuck or have questions:
1. Check this guide's [Troubleshooting](#troubleshooting) section
2. Use `git --help` or `git <command> --help` for command documentation
3. Open an issue on GitHub describing your problem
4. Reach out to the project maintainers

---

Remember: Everyone struggles with Git at first. Don't be afraid to experiment in a test branch, and don't worry about making mistakes—Git makes it hard to lose your work permanently!
