# New-episode checklist (jhcannabisnews.com)

The site is static; a push to `main` deploys it. Run everything from the repo root
(`C:\Users\THEVI\Videos\CannaNews\website`). Pull first: `git pull --rebase origin main`
(bots push headline, bill-tracker and subscriber-bar refreshes).

## 1. Episodes page + Home "Latest episode"

```
py -3 tools/add_episode.py <num> <video_id> <release ISO> <prev release ISO> "<title>" "<blurb>" "<date label>"
```

Example (Ep 44):

```
py -3 tools/add_episode.py 44 VIDEOID 2026-11-26T06:00:00-06:00 2026-11-25T06:00:00-06:00 "Title as uploaded" "One or two factual sentences, 40-60 words." "Thu Nov 26, 2026"
```

- Release ISO: the real YouTube schedule. Mon-Fri 6:00 AM CT; Saturday and Sunday episodes have been 8:00 AM CT. Offset is `-06:00` (CST, after Nov 1).
- Prev release ISO: copy the previous episode's `data-show-after` from `index.html` (the script fails if the previous Home block is not found).
- Blurb: facts from the upload kit description only. Say "cannabis", not "weed". Neutral on parties.
- Docuseries parts (e.g. Cannabis on Trial) are added by hand: a block in `episodes.html` and `index.html`, with the Home block's `data-hide-after` set to the next episode's release and the previous Home block's `data-hide-after` set to the part's release.

## 2. Blog article (one per episode)

1. Copy `texas-marijuana-legalization-bills-2027.html` to `<search-friendly-slug>.html` (for example `white-house-cbd-hemp-ban-request-texas.html`).
2. Change: `<title>`, meta description, canonical, og tags, og:image and twitter:image (`https://i.ytimg.com/vi/<video_id>/maxresdefault.jpg`), the three JSON-LD blocks (NewsArticle, VideoObject, FAQPage), the iframe `src` and title, the episode label and date, headline, dek, body, FAQ, sources and the "Watch the episode" link.
3. 500-800 words, facts only from that episode's `script.md`, `fact_check.md` and `upload_kit.md` sources, with links. Name party labels, attribute ban arguments ("ban backers say"), end with "News reporting and commentary, not legal advice", slogan exactly "Regulate, Don't Ban". No "weed", no alcohol or smoking wording.
4. Card on `blog.html`: add a new `<a class="card" ...>` at the top of `<div class="cards">`, copying an existing card, with `data-show-after` set to the episode's release ISO.
5. Link from the episode: in `episodes.html`, add ` <a style="color:var(--purple)" href="<slug>.html">Read the full write-up →</a>` to the end of the episode blurb. On `index.html`, add it to the "All episodes →" line of the latest-episode block if wanted.
6. Sitemap: add `<url><loc>https://jhcannabisnews.com/<slug>.html</loc><lastmod>YYYY-MM-DD</lastmod></url>` before `</urlset>` in `sitemap.xml`.

Do NOT run `tools/sync_meta.py` to do this: its description table is out of date and it overwrites the hand-written meta descriptions on several pages (contact-your-lawmakers, privacy and others) and rewrites the sitemap without lastmod dates. `tools/sync_nav.py` is only needed when the nav bar changes.

## 3. Check, commit, push

- Open `episodes.html`, `index.html` and the new article in a browser. The Home "Latest episode" and the blog card appear only after their release time (`release.js` gates them).
- Check for duplicate video IDs and balanced `<div>` tags; `py -3 tools/simulate_release.py` can preview release gating.
- Stage explicit paths: `git add -- index.html episodes.html blog.html sitemap.xml <slug>.html`
- Commit, then `git pull --rebase origin main` and `git push origin main`.
- Leave `thumbs/_tmp_ep13.json`, `tools/__pycache__` and `tools/pinterest_log.md` alone.
