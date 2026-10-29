# simple personal website

my simple website

## files

- `index.html` home page
- `yolo.html`, `ipick.html`, `cofair.html` project pages
- `styles.css` all the styling (colors are at the top)
- `script.js` fades sections in as you scroll

## to see it

double-click `index.html`, or open the folder in vs code and use the live server extension.

## to finish

- make an `images/` (and `videos/`) folder and swap each grey placeholder for an `<img>` or `<video>`. every placeholder has a comment above it showing the exact line to use
- fill in the `[bracketed]` parts on the project pages
- swap `you@example.com` for your email in `index.html` (it's in two spots)
- update the hevy numbers in `index.html` by hand whenever you want

## hevy stats

the lifting card reads `hevy.json`. a github action (`.github/workflows/hevy.yml`) runs `scripts/update_hevy.py` once a day, pulls stats from hevy, and commits a fresh `hevy.json`.

one-time setup:
1. repo settings → secrets and variables → actions → new repository secret
2. name it `HEVY_API_KEY` and paste your key (from hevy.com/settings?developer). never put the key in the code
3. actions tab → "update hevy stats" → run workflow, so you don't have to wait a day

the card only fills in on the live site. opening `index.html` by double-clicking can't load `hevy.json`, so it'll say the stats load once the site is online.

## to put it online

repo settings → pages → deploy from branch `main`, root folder. it'll be live at `aydaneddiegonzalez.github.io/simple-personal-website`.
