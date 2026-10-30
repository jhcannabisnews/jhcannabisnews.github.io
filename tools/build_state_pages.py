"""Write one search-friendly "Is delta-8 legal in <State>?" page per state in STATES, straight from data/legal.js
(the checker's data), so the pages never disagree with the checker. Rerun after any legal.js change, then
py -3 tools/sync_nav.py && py -3 tools/sync_meta.py:  py -3 tools/build_state_pages.py"""
import html, json, os, re

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATES = ["tx", "fl", "ga", "nc", "tn", "oh", "ca", "il", "mo", "ny", "pa", "mi", "al", "ok", "ky"]

src = open(os.path.join(SITE, "data", "legal.js"), encoding="utf-8").read()
CHECKED = re.search(r'const LEGAL_CHECKED = "([^"]+)"', src).group(1)
LEGAL = {k: dict(n=n, rec=r, med=m, hemp=h, note=note.replace("\\'", "'"))
         for k, n, r, m, h, note in re.findall(
             r'\b(\w\w):\{n:"([^"]+)",rec:"(\w+)",med:"(\w+)",hemp:"(\w+)",note:"((?:[^"\\]|\\.)*)"\}', src)}

# Same wording as checker.html, so a state reads the same in both places
REC = {"yes": "Recreational marijuana is legal for adults 21+, sold in licensed stores.",
       "partial": "Adults can possess a limited amount, but there are no licensed recreational stores yet.",
       "no": "Recreational marijuana is illegal."}
MED = {"full": "There is a medical marijuana program for qualifying patients.",
       "limited": "Medical use is limited to low-THC or CBD products for specific conditions.",
       "none": "There is no medical marijuana program."}
FED = ("The federal hemp changes apply in every state: on Nov 12, 2026, cannabinoids the plant can't make naturally "
       "(like THC-O) lose federal hemp status, and on Dec 11, 2026, a finished hemp product with more than 0.4 mg of "
       "total THC per container (THCA counts) is no longer hemp under federal law, unless Congress changes it. "
       "Analysts disagree on whether delta-8 made from CBD is affected Nov 12 or Dec 11, so don't count on the later date.")


def slug(name):
    return "is-delta-8-legal-in-" + re.sub(r"[^a-z]+", "-", name.lower()).strip("-") + ".html"


def page(k):
    s = LEGAL[k]
    n, e = s["n"], html.escape
    if s["hemp"] == "ban":
        short = f"Mostly no. {n} bans or tightly restricts intoxicating hemp THC like delta-8."
        verdict = ("❌", "Banned or tightly restricted", f"{n} bans or tightly restricts intoxicating hemp THC like delta-8, "
                   "and in some cases THCA flower. Don't assume a store-bought hemp product is legal here.")
    else:
        short = (f"For now, we couldn't confirm a statewide delta-8 ban in {n}, but the federal hemp ban "
                 "reaches every state on Nov 12 and Dec 11, 2026.")
        verdict = ("⚠️", "No statewide ban confirmed, for now", f"We couldn't confirm a statewide ban in {n}, but rules vary "
                   "and change often, and the federal changes on Nov 12 and Dec 11 apply here too. Check before you buy.")
    title = f"Is Delta-8 Legal in {n}? 2026 Hemp THC & Marijuana Law — J&H Cannabis News"
    desc = f"Is delta-8 legal in {n}? {short} Plus {n}'s marijuana laws, THCA flower and the federal hemp ban dates. Updated {CHECKED}."
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f"Is delta-8 legal in {n}?",
         "acceptedAnswer": {"@type": "Answer", "text": f"{verdict[2]} {FED}"}},
        {"@type": "Question", "name": f"Is THCA flower legal in {n} after December 11, 2026?",
         "acceptedAnswer": {"@type": "Answer", "text": "From Dec 11, 2026 the federal hemp test counts total THC, including THCA, "
                            "so most THCA flower is treated as marijuana under federal law in every state. " + REC[s["rec"]]}},
        {"@type": "Question", "name": f"Is marijuana legal in {n}?",
         "acceptedAnswer": {"@type": "Answer", "text": f"{REC[s['rec']]} {MED[s['med']]}"}}]}
    others = " · ".join(f'<a href="{slug(LEGAL[o]["n"])}">{e(LEGAL[o]["n"])}</a>' for o in STATES if o != k)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="x-desc" content="{e(desc)}">
<link rel="icon" href="logo.png"><link rel="stylesheet" href="style.css">
<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>
</head>
<body>
<nav></nav>
<div class="wrap">
<article>
  <span class="ep-num" style="color:var(--red);font-weight:900;letter-spacing:.06em">STATE LAW · UPDATED {e(CHECKED.upper())}</span>
  <h1>Is delta-8 legal in {e(n)}?</h1>
  <p class="dek">{e(short)}</p>

  <div class="box"><p style="margin:0"><strong>{verdict[0]} Delta-8 &amp; hemp THC: {e(verdict[1])}.</strong> {e(verdict[2])}</p></div>

  <h2>The latest in {e(n)}</h2>
  <p>{e(s["note"])}</p>

  <h2>Marijuana in {e(n)}</h2>
  <p>{e(REC[s["rec"]])} {e(MED[s["med"]])}</p>

  <h2>The federal hemp ban: Nov 12 and Dec 11, 2026</h2>
  <p>{e(FED)}</p>
  <p><a style="color:var(--purple)" href="federal-hemp-ban-explained.html">The federal hemp ban, explained →</a></p>

  <div class="box center" style="margin-top:18px">
    <p style="margin:0 0 10px"><strong>These rules change every week.</strong> We cover every change in a new video every day,
    so you hear it before Dec 11, not after.</p>
    <a class="btn" href="https://www.youtube.com/@jhcannabisnews?sub_confirmation=1">▶ Subscribe free</a>
    <a class="btn ghost" href="https://www.youtube.com/@jhcannabisnews/videos">Watch the latest episode</a>
    <a class="btn ghost" href="checker.html#{k}">🗺️ Check another state</a>
  </div>

  <p class="reviewed" style="margin-top:20px">Last checked {e(CHECKED)}. Sources: Ballotpedia, NORML, the Marijuana Policy
  Project, state regulators and hemp-law trackers, cross-checked. This is news and general information, not legal advice.
  Before you buy, carry or sell, check {e(n)}'s official rules or talk to a local attorney.
  <a style="color:var(--purple)" href="ask.html">Spot something out of date? Tell us →</a></p>
  <p style="color:var(--grey);font-size:.9rem">Other states: {others}</p>
</article>
</div>
<footer>
  News reporting and commentary for educational purposes — not legal advice.
  · <a href="mailto:james@jhcannabisnews.com">james@jhcannabisnews.com</a> · <a href="https://discord.gg/EXqpgyQyBq">💬 Join our Discord</a>
</footer>
</body>
</html>
"""


for k in STATES:
    name = slug(LEGAL[k]["n"])
    open(os.path.join(SITE, name), "w", encoding="utf-8", newline="\n").write(page(k))
    print("wrote", name)
