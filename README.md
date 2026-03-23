# Disney Universal KB

Public Quartz site for the Orlando trip planning vault.

## Stack

- [Quartz 4](https://quartz.jzhao.xyz/)
- Obsidian-flavored Markdown content under `content/`
- GitHub Actions deployment to GitHub Pages

## Local development

```bash
npm ci
npx quartz build --serve
```

## Publish

Push to `main`. GitHub Actions builds Quartz and deploys to GitHub Pages.

## Site URL

- <https://rodrigofalco.github.io/disney-universal-kb/>

## Notes

- Source notes for the public site live in `content/`
- `Assets/` is currently excluded from the public repo to keep the site lightweight
- Quartz already supports Obsidian-style wikilinks and related Markdown features
