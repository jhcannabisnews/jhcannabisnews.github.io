"""Show which gated blocks are visible on a page at given moments (mirrors release.js)."""
import re, sys
from datetime import datetime

def visible_blocks(html, now):
    out = []
    for m in re.finditer(r'<div class="(episode|next-date)"([^>]*)>(.*?)</div>', html, re.S):
        attrs, body = m.group(2), m.group(3)
        show = re.search(r'data-show-after="([^"]+)"', attrs)
        hide = re.search(r'data-hide-after="([^"]+)"', attrs)
        if not show and not hide:
            ok = True
        else:
            ok = ((not show or now >= datetime.fromisoformat(show.group(1))) and
                  (not hide or now < datetime.fromisoformat(hide.group(1))))
        if ok:
            label = re.search(r'(EPISODE \d+[^<]*)', body)
            out.append(f"{m.group(1)}: {label.group(1).strip() if label else body.strip()[:40]}")
    return out

for page in sys.argv[1:]:
    html = open(page, encoding="utf-8").read()
    for when in ["2026-10-12T22:00:00-05:00", "2026-10-13T12:00:00-05:00", "2026-10-14T12:00:00-05:00"]:
        print(f"{page} @ {when[:16]}: {visible_blocks(html, datetime.fromisoformat(when))}")
