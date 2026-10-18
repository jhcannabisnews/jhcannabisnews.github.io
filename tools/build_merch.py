"""Build the Merch pages from the Printify Pop-Up store's products.
merch.html               public "coming soon" page: photos, no prices, no buy links.
merch-preview-jh7q.html  unlisted preview for James & Hope: prices + store links (noindex, not in sitemap).
Images are saved in merch/ so the pages don't depend on Printify's image links.
Run: py -3 tools/build_merch.py"""
import os, urllib.request
from PIL import Image

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = "https://jh-cannabis-news.printify.me"
MOCK = "https://images-api.printify.com/mockup/"
P = [  # (slug, name, price, store product id, mockup path)
    ("regulate-tee", "Regulate, Don't Ban Tee", "$25.99", "33235134", "6ad3d87452df4727670b123d/18102/102044/regulate-dont-ban-tee.jpg?camera_label=front-2"),
    ("neon-tee", "Neon Logo Tee", "$25.99", "33235131", "6ad3d86219a9e3ef6c0947bf/18102/102044/neon-logo-tee.jpg?camera_label=front-2"),
    ("dec11-tee", "Dec 11 Hemp Fight Tee", "$25.99", "33235129", "6ad3d86b19a9e3ef6c0947c8/18102/102044/dec-11-hemp-fight-tee.jpg?camera_label=front-2"),
    ("texas-tee", "Texas Cannabis News Tee", "$25.99", "33235127", "6ad3d87119a9e3ef6c0947cb/18102/102044/texas-cannabis-news-tee.jpg?camera_label=front-2"),
    ("classic-tee", "Classic Logo Tee", "$25.99", "33235120", "6ad0c64a59ac88d91604b02e/18102/102044/classic-logo-tee.jpg?camera_label=front-2"),
    ("neon-hoodie", "Neon Logo Hoodie", "$44.99", "33235119", "6ad3e9e2dd9ae60ca105fac6/32920/98424/neon-logo-hoodie.jpg?camera_label=front"),
    ("classic-hoodie", "Classic Logo Hoodie", "$44.99", "33235116", "6ad0ce6bf0531fc34e0f53e5/32920/98424/classic-logo-hoodie.jpg?camera_label=front"),
    ("hat", "Classic Logo Hat", "$27.99", "33235117", "6ad0c80c59ac88d91604b16b/125365/135054/classic-logo-hat.jpg?camera_label=front"),
    ("beanie", "Embroidered Logo Beanie", "$27.99", "33236558", "6ad40b96753e48c73f0b13b5/116417/109382/embroidered-logo-beanie.jpg?camera_label=front"),
    ("gavel-tumbler", "Galaxy Gavel 20oz Tumbler", "$29.99", "33235122", "6ad3d9c17388cdd94b0a08d3/108286/104182/galaxy-gavel-20oz-tumbler.jpg?camera_label=front"),
    ("badge-tumbler", "Vintage Press Badge 20oz Tumbler", "$29.99", "33235121", "6ad3d9b63f189567a901e49a/108286/104182/vintage-press-badge-20oz-tumbler.jpg?camera_label=front"),
    ("classic-tumbler", "Classic Logo 20oz Tumbler", "$29.99", "33235118", "6ad0c89a97db1f1b0d0e6710/108286/104182/classic-logo-20oz-tumbler.jpg?camera_label=front"),
    ("mug", "Regulate, Don't Ban Black Mug", "$16.99", "33236223", "6ad408bd18e0243bd10d307d/65217/6405/regulate-dont-ban-black-mug.jpg?camera_label=front"),
    ("cooler", "Vintage Press Badge Can Cooler", "$11.99", "33236365", "6ad40a1b18e0243bd10d31e6/78460/38485/vintage-press-badge-can-cooler.jpg?camera_label=flat-front"),
    ("phone", "Galaxy Gavel Phone Case", "$24.99", "33236461", "6ad40aecf83da0fa840da465/62582/97458/galaxy-gavel-phone-case.jpg?camera_label=front-and-side"),
    ("sticker-neon", "Neon Logo Sticker", "from $4.99", "33236027", "6ad40726f83da0fa840da152/45750/16655/neon-logo-sticker.jpg?camera_label=front"),
    ("sticker-gavel", "Galaxy Gavel Sticker", "from $4.99", "33236092", "6ad407aa07b78bf56e0d21e4/45750/16655/galaxy-gavel-sticker.jpg?camera_label=front"),
    ("sticker-regulate", "Regulate, Don't Ban Sticker", "from $4.99", "33236155", "6ad407a1f83da0fa840da1c8/45750/16655/regulate-dont-ban-sticker.jpg?camera_label=front"),
]

CSS = """<style>
.merch-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:18px;margin:26px 0}
.item{background:var(--panel);border-radius:12px;overflow:hidden;border-bottom:4px solid var(--red);text-align:left}
.item img{width:100%;aspect-ratio:1/1;object-fit:cover;background:#fff;display:block}
.item .info{padding:12px 14px 16px}
.item h3{font-size:1.02rem;margin:0 0 6px;color:var(--white)}
.item .price{color:var(--red);font-weight:900}
.item .soon{color:var(--purple);font-weight:700;font-size:.9rem}
.item a.btn{margin-top:10px;padding:8px 14px;font-size:.9rem}
.notice{background:#3a1a1a;border:2px solid var(--red);border-radius:10px;padding:12px 16px;margin:18px auto;max-width:720px}
</style>"""

FOOT = """<footer>
  J&amp;H Cannabis News is news reporting and commentary for educational purposes. Nothing on
  this site or channel is legal advice. · <a href="mailto:jhcannabisnews@zohomail.com">jhcannabisnews@zohomail.com</a> · <a href="https://discord.gg/EXqpgyQyBq">💬 Join our Discord</a>
</footer>
</body>
</html>
"""


def fetch():
    os.makedirs(os.path.join(SITE, "merch"), exist_ok=True)
    for slug, _, _, _, path in P:
        out = os.path.join(SITE, "merch", slug + ".jpg")
        if os.path.exists(out):
            continue
        req = urllib.request.Request(MOCK + path, headers={"User-Agent": "Mozilla/5.0"})
        tmp = out + ".tmp"
        with open(tmp, "wb") as f:
            f.write(urllib.request.urlopen(req, timeout=60).read())
        im = Image.open(tmp).convert("RGB")
        im.thumbnail((700, 700))
        im.save(out, quality=85)
        os.remove(tmp)


def esc(s):
    return s.replace("&", "&amp;").replace("'", "&#39;")


def page(preview, nav):
    cards = []
    for slug, name, price, pid, _ in P:
        if preview:
            body = f'<span class="price">{price}</span><br><a class="btn" href="{STORE}/product/{pid}">View in store</a>'
        else:
            body = '<span class="soon">Coming soon</span>'
        cards.append(f'<div class="item"><img src="merch/{slug}.jpg" alt="{esc(name)}" loading="lazy">'
                     f'<div class="info"><h3>{esc(name)}</h3>{body}</div></div>')
    if preview:
        title, meta = "Merch Preview", '<meta name="robots" content="noindex,nofollow">'
        top = ('<div class="notice">🔒 <strong>Private preview for James &amp; Hope.</strong> This page isn\'t linked anywhere. '
               'Checkout stays off until the store is verified.</div>\n  <h1>J&amp;H Merch (preview)</h1>')
    else:
        title = "J&amp;H Merch"
        meta = ('<meta name="description" content="Official J&amp;H Cannabis News merch is coming soon: tees, hoodies, hats, '
                'tumblers, mugs, stickers and more.">')
        nav = nav.replace('<a href="merch.html">', '<a href="merch.html" class="active">')
        top = ('<h1>J&amp;H Merch</h1>\n  <div class="tag">Coming soon</div>\n  <div class="bar"></div>\n'
               '  <p class="lead">Official J&amp;H Cannabis News gear is almost here: tees, hoodies, hats, tumblers, mugs, '
               'stickers and more. <strong>Regulate, don\'t ban.</strong> Subscribe or join our Discord to hear the moment it drops.</p>\n'
               '  <a class="btn" href="https://www.youtube.com/@jhcannabisnews?sub_confirmation=1">▶ Subscribe</a>\n'
               '  <a class="btn ghost" href="https://discord.gg/EXqpgyQyBq">💬 Join our Discord</a>')
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{title}</title>\n{meta}\n<link rel="icon" href="logo.png"><link rel="stylesheet" href="style.css">\n{CSS}\n</head>\n<body>\n'
            f'<nav>{nav}</nav>\n<div class="wrap center">\n  {top}\n  <div class="merch-grid">\n    '
            + "\n    ".join(cards) + "\n  </div>\n</div>\n" + FOOT)


if __name__ == "__main__":
    fetch()
    idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    nav = idx.split("<nav>")[1].split("</nav>")[0].replace(' class="active"', '')
    open(os.path.join(SITE, "merch.html"), "w", encoding="utf-8", newline="\n").write(page(False, nav))
    open(os.path.join(SITE, "merch-preview-jh7q.html"), "w", encoding="utf-8", newline="\n").write(page(True, nav))
    print("built", len(P), "items")
