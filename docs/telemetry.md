# Public GitHub telemetry

The profile displays a dated snapshot, rendered as self-hosted SVGs in both themes. It does not depend on an external badge or chart service.

## Scope and definitions

- Repository inventory: current publicly visible repositories owned by `araxis07`, including archived repositories and forks. Private and deleted repositories are absent.
- Primary languages: each repository contributes once under GitHub's `language` field. Shares use the full inventory as the denominator. Null language values appear as `Unclassified`. This measures repository shares, not code-byte shares or proficiency.
- Repository creation: the current inventory grouped by the UTC year in `created_at`. This is not a historical inventory or a release/commit velocity measure.
- Stars: sum of `stargazers_count` over the public inventory.
- Public PRs and issues authored: GitHub issue-search totals for `author:araxis07 is:public`, separately filtered with `is:pr` and `is:issue`.
- Featured projects: the six entries in the profile's project list.

Source URLs, per-repository rows and the snapshot date are stored in [github-stats.json](../data/github-stats.json). The initial snapshot was collected through the connected GitHub tools; the refresh script uses the equivalent public REST data.

## Refresh

Run with Python 3.9 or later:

```sh
python scripts/refresh_github_stats.py
```

The script retrieves the public repository inventory and public authored PR/issue totals, updates the snapshot date in Asia/Tokyo, and rebuilds the local README and SVGs. GitHub's unauthenticated API rate limits apply. The script does not push changes or install a scheduled workflow.

To reproduce the images from the stored snapshot without network access:

```sh
python scripts/build_profile.py
```
