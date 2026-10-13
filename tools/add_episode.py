"""Add a scheduled episode to Home + Episodes, release-gated (reusable for every episode).

usage: py -3 tools/add_episode.py <num> <video_id> <release ISO> <prev release ISO> "<title>" "<blurb>" "<date label>"
- Episodes page: a premiere countdown (from the previous release until this one) + the episode block
- Home: same countdown + the episode as "Latest episode"; the previous latest stops showing at release
"""
import os, sys
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
num, vid, rel, prev, title, blurb, datelabel = sys.argv[1:8]

iframe = (f'<iframe class="video" data-src="https://www.youtube-nocookie.com/embed/{vid}"\n'
          f'            title="Episode {num}: {title}" loading="lazy"\n'
          '            allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; web-share"\n'
          '            allowfullscreen></iframe>')
teaser = (f'  <div class="next-date" data-show-after="{prev}" data-hide-after="{rel}" hidden>\n'
          f'    <div class="label">▶ EPISODE {num} PREMIERES</div>\n'
          f'    <div class="what">{title}</div>\n'
          f'    <div class="countdown" data-target="{rel}" data-kind="event"></div>\n'
          '  </div>\n')
head = (f'    <span class="ep-num">EPISODE {num} · {datelabel.upper()}</span>\n'
        f'    <h3>{title}</h3>\n')

# Episodes page: newest on top, right under the page bar
p = os.path.join(SITE, "episodes.html")
t = open(p, encoding="utf-8").read()
assert vid not in t, "already added"
anchor = '  <div class="bar"></div>\n'
block = (teaser + f'  <div class="episode" data-show-after="{rel}" hidden>\n' + head +
         f'    <p>{blurb}</p>\n    {iframe}\n  </div>\n\n')
t = t.replace(anchor, anchor + "\n" + block, 1)
open(p, "w", encoding="utf-8", newline="\n").write(t)

# Home: the current latest (shown after prev) now also hides at this release
p = os.path.join(SITE, "index.html")
t = open(p, encoding="utf-8").read()
cur = f'  <div class="episode" data-show-after="{prev}" hidden>'
assert cur in t, "previous latest-episode block not found"
t = t.replace(cur, f'  <div class="episode" data-show-after="{prev}" data-hide-after="{rel}" hidden>', 1)
anchor = '  <h2>Latest episode</h2>\n'
block = (teaser + f'  <div class="episode" data-show-after="{rel}" hidden>\n' + head + f'    {iframe}\n'
         '    <p style="margin-top:12px"><a style="color:var(--purple)" href="episodes.html">All episodes →</a></p>\n'
         '  </div>\n')
t = t.replace(anchor, anchor + block, 1)
open(p, "w", encoding="utf-8", newline="\n").write(t)
print(f"Episode {num} added, live at {rel}")
