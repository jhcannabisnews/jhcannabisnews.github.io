"""One-time: add Episode 2 (release-gated at Oct 13 2026 6:00 AM CT) to Home and Episodes."""
import os
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = "2026-10-13T06:00:00-05:00"
EP2_IFRAME = ('<iframe class="video" data-src="https://www.youtube-nocookie.com/embed/jLO5KEm5NW8"\n'
              '            title="Episode 2: A Judge Just PAUSED Marijuana Rescheduling" loading="lazy"\n'
              '            allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; web-share"\n'
              '            allowfullscreen></iframe>')
TEASER = (f'  <div class="next-date" data-hide-after="{REL}">\n'
          '    <div class="label">▶ EPISODE 2 PREMIERES</div>\n'
          '    <div class="what">A Judge Just PAUSED Marijuana Rescheduling — Tuesday, Oct 13 at 6:00 AM Central</div>\n'
          f'    <div class="countdown" data-target="{REL}" data-kind="event"></div>\n'
          '  </div>\n')

# --- Episodes page: Ep2 block on top (shown at release) + teaser until then
p = os.path.join(SITE, "episodes.html")
t = open(p, encoding="utf-8").read()
anchor = '  <!-- EPISODE TEMPLATE:'
block = (TEASER +
         f'  <div class="episode" data-show-after="{REL}" hidden>\n'
         '    <span class="ep-num">EPISODE 2 · OCTOBER 13, 2026</span>\n'
         '    <h3>A Judge Just PAUSED Marijuana Rescheduling — Here\'s What Happens Now</h3>\n'
         '    <p>Medical marijuana moved to Schedule III, then a DEA judge paused the rest. Plus\n'
         '    Massachusetts Question 8, the federal hemp countdown, and news from five more states.</p>\n'
         f'    {EP2_IFRAME}\n'
         '  </div>\n\n')
assert anchor in t and "jLO5KEm5NW8" not in t
t = t.replace(anchor, block + anchor, 1)
t = t.replace('</footer>\n</body>', '</footer>\n<script src="countdown.js"></script>\n'
              '<script src="release.js"></script>\n</body>', 1)
open(p, "w", encoding="utf-8", newline="\n").write(t)

# --- Home: Ep1 stays "latest" until release, then Ep2 takes over
p = os.path.join(SITE, "index.html")
t = open(p, encoding="utf-8").read()
old = '  <h2>Latest episode</h2>\n  <div class="episode">\n    <span class="ep-num">EPISODE 1'
new = ('  <h2>Latest episode</h2>\n'
       + TEASER +
       f'  <div class="episode" data-show-after="{REL}" hidden>\n'
       '    <span class="ep-num">EPISODE 2 · OCTOBER 13, 2026</span>\n'
       '    <h3>A Judge Just PAUSED Marijuana Rescheduling — Here\'s What Happens Now</h3>\n'
       f'    {EP2_IFRAME}\n'
       '    <p style="margin-top:12px"><a style="color:var(--purple)" href="episodes.html">All episodes →</a></p>\n'
       '  </div>\n'
       f'  <div class="episode" data-hide-after="{REL}">\n    <span class="ep-num">EPISODE 1')
assert old in t
t = t.replace(old, new, 1)
t = t.replace('<script src="headlines.js"></script>', '<script src="headlines.js"></script>\n'
              '<script src="release.js"></script>', 1)
open(p, "w", encoding="utf-8", newline="\n").write(t)
print("Ep2 added (release-gated)")
