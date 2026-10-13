"""Add a scheduled Short to the Shorts page, release-gated (newest on top).

usage: py -3 tools/add_short.py <video_id> <release ISO> <episode num> "<title>"
"""
import os, sys
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vid, rel, ep, title = sys.argv[1:5]

p = os.path.join(SITE, "shorts.html")
t = open(p, encoding="utf-8").read()
assert vid not in t, "already added"
anchor = '  <div class="shorts-grid">\n'
assert anchor in t, "shorts grid not found"
block = (f'    <div class="short" data-show-after="{rel}" hidden>\n'
         f'      <iframe data-src="https://www.youtube-nocookie.com/embed/{vid}"\n'
         f'              title="Short: {title}" loading="lazy"\n'
         '              allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; web-share"\n'
         '              allowfullscreen></iframe>\n'
         f'      <h3>{title}</h3>\n'
         f'      <a href="episodes.html">Full story: Episode {ep} →</a>\n'
         '    </div>\n')
t = t.replace(anchor, anchor + block, 1)
open(p, "w", encoding="utf-8", newline="\n").write(t)
print(f"Short {vid} added, live at {rel}")
