# Disney Universal KB

Public-facing Git repository for the Orlando trip planning vault.

## What this repo contains

- The Obsidian-compatible Markdown knowledge base
- Images and supporting assets used by the vault
- A lightweight `index.html` viewer for GitHub Pages
- `site-files.json`, generated from the current file tree, so the browser can navigate the vault

## GitHub Pages

This repository is intended to be published with GitHub Pages from the `main` branch root.

Once Pages is enabled, the site URL should be:

- <https://rodrigofalco.github.io/disney-universal-kb/>

## Updating the site index

When files are added, removed, or renamed, regenerate the file list:

```bash
python3 scripts/build_site.py
```

Then commit and push the result.

## Notes

- The web viewer resolves common Obsidian wikilinks such as `[[Page]]` and `[[path/to/Page|Alias]]`.
- It is a simple static viewer, not a full Obsidian replacement.
