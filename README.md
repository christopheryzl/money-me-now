# Git Best Practices

A quick reference for working effectively with Git on this repository.

## Branching

- **Never commit directly to `main`.** Treat it as always deployable.
- Create a new branch for every feature, fix, or experiment:
  ```
  git checkout -b feature/short-description
  ```
- Use a consistent naming scheme, e.g. `feature/...`, `fix/...`, `chore/...`, `experiment/...`.
- Keep branches short-lived. Long-running branches drift from `main` and accumulate painful merge conflicts.
- Branch off the latest `main` (`git pull` first) so you're not building on stale code.
- Delete branches after they're merged (`git branch -d feature/short-description`) to keep the branch list clean.

## Pulling

- **Pull before you start work** each session to make sure you're building on the latest code.
- **Pull before you push** if others may have pushed in the meantime — this avoids unnecessary conflicts.
- Prefer `git pull --rebase` over a plain `git pull` on feature branches you own alone. It keeps history linear instead of creating merge commits for every sync.
  ```
  git pull --rebase origin main
  ```
- Never `pull --rebase` on a branch other people are also pushing to — it rewrites history they may depend on.

## Committing

- Commit early and often on your own branch; squash/clean up before merging if needed.
- Write commit messages that explain **why**, not just what — the diff already shows what changed.
- Keep commits focused on a single logical change. Avoid mixing unrelated changes in one commit.
- Don't commit secrets, credentials, or generated/build artifacts. Use a `.gitignore`.

## Merging / Pull Requests

- Open a pull request instead of pushing straight to `main`, even solo — it gives you a diff to review and a record of why the change happened.
- Prefer **squash merging** for feature branches to keep `main`'s history clean, one commit per change.
- Resolve conflicts locally (via rebase or merge) before requesting/using a PR merge — don't resolve them in the GitHub UI for anything non-trivial.

## Other Key Practices

- **`.gitignore` early.** Set it up before your first commit so build output, `node_modules`, `.env` files, etc. never enter history.
- **Tag releases** (`git tag v1.0.0`) for meaningful milestones so you can always check out a known-good state.
- **Use `git status` and `git diff` before every commit** to confirm exactly what you're staging.
- **Avoid force-pushing (`git push --force`) to shared branches.** If you must rewrite your own feature branch's history after pushing, use `git push --force-with-lease` instead — it fails safely if someone else pushed in the meantime.
- **Stash, don't discard.** If you need to switch branches with uncommitted work, use `git stash` rather than losing changes.
- **Review history with `git log --oneline --graph --all`** to understand branch structure at a glance.
- **Never rewrite published history on `main`** (no `rebase`, `commit --amend`, or `reset --hard` on commits others may have pulled).
