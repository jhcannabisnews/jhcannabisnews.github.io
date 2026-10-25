"""Build the Merch pages from the Printify Pop-Up store's products.
merch.html               public "coming soon" page: photos, no prices, no buy links.
merch-preview-jh7q.html  unlisted preview for James & Hope: prices + store links (noindex, not in sitemap).
Images are saved in merch/ so the pages don't depend on Printify's image links.
Run: py -3 tools/build_merch.py"""
import os, re, urllib.request
from PIL import Image

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = "https://jh-cannabis-news.printify.me"
MOCK = "https://images-api.printify.com/mockup/"
P = [  # (slug, name, price, store product id, mockup path)
    # acrylic keychain (10-24): Printify has no mockup for it, so merch/<slug>.jpg is our own shop photo (thumbs/merch-keychain-*.jpg)
    ("veterans-deserve-access-patch-keychain", "Veterans Deserve Access Patch Keychain", "$9.99", "33512356", ""),
    # die-cut magnets (10-24): 2", 3", 4" in 4 designs
    ("veterans-deserve-access-patch-magnet", "Veterans Deserve Access Patch Magnet", "from $8.99", "33508054", "6add4b2d21de5de625023847/76776/23708/veterans-deserve-access-patch-magnet.jpg?camera_label=front"),
    ("veterans-dog-tags-magnet", "Veterans Dog Tags Magnet", "from $8.99", "33508293", "6add4bd32f0d45364d02e1c7/76776/23708/veterans-dog-tags-magnet.jpg?camera_label=front&revision=1792896641908"),
    ("jh-cannabis-news-logo-magnet", "J&H Cannabis News Logo Magnet", "from $8.99", "33508328", "6add4bb451bc2a904809f807/76776/23708/jh-cannabis-news-logo-magnet.jpg?camera_label=front"),
    ("regulate-dont-ban-magnet", "Regulate, Don't Ban Magnet", "from $8.99", "33508295", "6add4be551bc2a904809f822/76776/23708/regulate-dont-ban-magnet.jpg?camera_label=front"),
    # Veterans Dog Tags (10-24): tee, black mug, 20oz tumbler, hoodie (big back print + J&H chest logo)
    ("veterans-dog-tags-tee", "Veterans Dog Tags Tee", "$25.99", "33491616", "6adcdb7b0842128e3b04764a/18102/102044/veterans-dog-tags-tee.jpg?camera_label=front-2"),
    ("veterans-dog-tags-hoodie", "Veterans Dog Tags Hoodie", "$47.99", "33491781", "6adcdb956e278da11903e470/32920/98425/veterans-dog-tags-hoodie.jpg?camera_label=back"),
    ("veterans-dog-tags-black-mug", "Veterans Dog Tags Black Mug", "$16.99", "33491648", "6adcdbac5bb45b7c640f424e/65217/6405/veterans-dog-tags-black-mug.jpg?camera_label=front"),
    ("veterans-dog-tags-20oz-tumbler", "Veterans Dog Tags 20oz Tumbler", "$29.99", "33491685", "6adcdb8d022966bc72071e9f/108286/104182/veterans-dog-tags-20oz-tumbler.jpg?camera_label=front"),
    # Veterans Deserve Access patch (10-24): hat + sticker
    ("veterans-deserve-access-patch-hat", "Veterans Deserve Access Patch Hat", "$27.99", "33496007", "6adcf939a01c71b40b093479/125365/135054/veterans-deserve-access-patch-hat.jpg?camera_label=front"),
    ("veterans-deserve-access-patch-sticker", "Veterans Deserve Access Patch Sticker", "from $4.99", "33496006", "6adcf94351bc2a904809b3eb/45750/16655/veterans-deserve-access-patch-sticker.jpg?camera_label=front"),
    # women's line (10-23): 3 bright pink/purple designs across tees, tumblers, cases, stickers
    ("flower-power-peace-sign-tee", "Flower Power Peace Sign Tee", "$25.99", "33456195", "6adb75eb04ff64518d0e294e/18102/102044/flower-power-peace-sign-tee.jpg?camera_label=front-2"),
    ("texas-grown-texas-regulated-butterfly-tee", "Texas Grown Texas Regulated Butterfly Tee", "$25.99", "33456350", "6adb75f4abc2ab63bd0aac56/18102/102044/texas-grown-texas-regulated-butterfly-tee.jpg?camera_label=front-2"),
    ("good-vibes-clear-laws-moon-tee", "Good Vibes Clear Laws Moon Tee", "$25.99", "33456454", "6adb75f9d155d127b5025190/18102/102044/good-vibes-clear-laws-moon-tee.jpg?camera_label=front-2"),
    ("flower-power-peace-sign-20oz-tumbler", "Flower Power Peace Sign 20oz Tumbler", "$29.99", "33456247", "6adb75fe577086f0460372d8/108286/104182/flower-power-peace-sign-20oz-tumbler.jpg?camera_label=front"),
    ("texas-grown-texas-regulated-butterfly-20oz-tumbler", "Texas Grown Texas Regulated Butterfly 20oz Tumbler", "$29.99", "33456367", "6adb7603577086f0460372e3/108286/104182/texas-grown-texas-regulated-butterfly-20oz-tumbler.jpg?camera_label=front"),
    ("good-vibes-clear-laws-moon-20oz-tumbler", "Good Vibes Clear Laws Moon 20oz Tumbler", "$29.99", "33456464", "6adb7608ca2c490d9d08755b/108286/104182/good-vibes-clear-laws-moon-20oz-tumbler.jpg?camera_label=front"),
    ("flower-power-peace-sign-phone-case", "Flower Power Peace Sign Phone Case", "$24.99", "33456318", "6adb76510c4296642f0ada2a/62582/97458/flower-power-peace-sign-phone-case.jpg?camera_label=front-and-side"),
    ("texas-grown-texas-regulated-butterfly-phone-case", "Texas Grown Texas Regulated Butterfly Phone Case", "$24.99", "33456402", "6adb7656b25b080af50443dd/62582/97458/texas-grown-texas-regulated-butterfly-phone-case.jpg?camera_label=front-and-side"),
    ("good-vibes-clear-laws-moon-phone-case", "Good Vibes Clear Laws Moon Phone Case", "$24.99", "33456485", "6adb765bd155d127b50251e8/62582/97458/good-vibes-clear-laws-moon-phone-case.jpg?camera_label=front-and-side"),
    ("flower-power-peace-sign-sticker", "Flower Power Peace Sign Sticker", "from $4.99", "33456271", "6adb760e577086f0460372e5/45750/16655/flower-power-peace-sign-sticker.jpg?camera_label=front"),
    ("texas-grown-texas-regulated-butterfly-sticker", "Texas Grown Texas Regulated Butterfly Sticker", "from $4.99", "33456381", "6adb7613577086f0460372e6/45750/16655/texas-grown-texas-regulated-butterfly-sticker.jpg?camera_label=front"),
    ("good-vibes-clear-laws-moon-sticker", "Good Vibes Clear Laws Moon Sticker", "from $4.99", "33456474", "6adb761804ff64518d0e296c/45750/16655/good-vibes-clear-laws-moon-sticker.jpg?camera_label=front"),
    # older-men line (10-22): 8 designs across tees, hoodies, tumblers, mugs, cases, hats, stickers
    ("hemp-for-victory-tee", "Hemp for Victory Tee", "$25.99", "33440144", "6adab91d2e39dc5ae40a382f/18102/102044/hemp-for-victory-tee.jpg?camera_label=front-2"),
    ("texas-hemp-pickup-tee", "Texas Hemp Pickup Tee", "$25.99", "33440219", "6adaba1c3f8f83bb360e5dcb/18102/102044/texas-hemp-pickup-tee.jpg?camera_label=front-2"),
    ("old-enough-to-remember-tee", "Old Enough to Remember Tee", "$25.99", "33440262", "6adaba88fffc9a39740d2792/18102/102044/old-enough-to-remember-tee.jpg?camera_label=front-2"),
    ("veterans-for-medical-cannabis-tee", "Veterans for Medical Cannabis Tee", "$25.99", "33440331", "6adabaf4fffc9a39740d27cc/18102/102044/veterans-for-medical-cannabis-tee.jpg?camera_label=front-2"),
    ("texas-grown-texas-regulated-tee", "Texas Grown Texas Regulated Tee", "$25.99", "33440370", "6adabb6194b6dff42c071190/18102/102044/texas-grown-texas-regulated-tee.jpg?camera_label=front-2"),
    ("we-the-people-tee", "We the People Tee", "$25.99", "33440403", "6adabbc594b6dff42c0711cb/18102/102044/we-the-people-tee.jpg?camera_label=front-2"),
    ("ask-me-about-the-farm-bill-tee", "Ask Me About the Farm Bill Tee", "$25.99", "33440452", "6adabc24fffc9a39740d28e6/18102/102044/ask-me-about-the-farm-bill-tee.jpg?camera_label=front-2"),
    ("gone-fishin-for-better-laws-tee", "Gone Fishin for Better Laws Tee", "$25.99", "33440521", "6adabcaa9f9e2d088d0c3bfb/18102/102044/gone-fishin-for-better-laws-tee.jpg?camera_label=front-2"),
    ("hemp-for-victory-hoodie", "Hemp for Victory Hoodie", "$47.99", "33440585", "6adabd142e39dc5ae40a3af6/32920/98425/hemp-for-victory-hoodie.jpg?camera_label=back"),
    ("texas-hemp-pickup-hoodie", "Texas Hemp Pickup Hoodie", "$47.99", "33440729", "6adabe242e39dc5ae40a3bea/32920/98425/texas-hemp-pickup-hoodie.jpg?camera_label=back"),
    ("veterans-for-medical-cannabis-hoodie", "Veterans for Medical Cannabis Hoodie", "$47.99", "33440802", "6adabe8d3f8f83bb360e614e/32920/98425/veterans-for-medical-cannabis-hoodie.jpg?camera_label=back"),
    ("texas-grown-texas-regulated-hoodie", "Texas Grown Texas Regulated Hoodie", "$47.99", "33440895", "6adabef92e39dc5ae40a3caa/32920/98425/texas-grown-texas-regulated-hoodie.jpg?camera_label=back"),
    ("texas-hemp-pickup-20oz-tumbler", "Texas Hemp Pickup 20oz Tumbler", "$29.99", "33440959", "6adabf8f9645f8de5f03646b/108286/104182/texas-hemp-pickup-20oz-tumbler.jpg?camera_label=front"),
    ("old-enough-to-remember-20oz-tumbler", "Old Enough to Remember 20oz Tumbler", "$29.99", "33440998", "6adac042f538eea0950c6fc6/108286/104182/old-enough-to-remember-20oz-tumbler.jpg?camera_label=front"),
    ("veterans-for-medical-cannabis-20oz-tumbler", "Veterans for Medical Cannabis 20oz Tumbler", "$29.99", "33441067", "6adac0bd9645f8de5f03654a/108286/104182/veterans-for-medical-cannabis-20oz-tumbler.jpg?camera_label=front"),
    ("texas-grown-texas-regulated-20oz-tumbler", "Texas Grown Texas Regulated 20oz Tumbler", "$29.99", "33441194", "6adac1399f9e2d088d0c3f4d/108286/104182/texas-grown-texas-regulated-20oz-tumbler.jpg?camera_label=front"),
    ("gone-fishin-for-better-laws-20oz-tumbler", "Gone Fishin for Better Laws 20oz Tumbler", "$29.99", "33441347", "6adac20f301df6d475047858/108286/104182/gone-fishin-for-better-laws-20oz-tumbler.jpg?camera_label=front"),
    ("hemp-for-victory-black-mug", "Hemp for Victory Black Mug", "$16.99", "33441421", "6adac2dacb02d80c650d232a/65217/6405/hemp-for-victory-black-mug.jpg?camera_label=front"),
    ("old-enough-to-remember-black-mug", "Old Enough to Remember Black Mug", "$16.99", "33441453", "6adac35ff538eea0950c721e/65217/6405/old-enough-to-remember-black-mug.jpg?camera_label=front"),
    ("we-the-people-black-mug", "We the People Black Mug", "$16.99", "33441502", "6adac3d0fffc9a39740d2e5c/65217/6405/we-the-people-black-mug.jpg?camera_label=front"),
    ("ask-me-about-the-farm-bill-black-mug", "Ask Me About the Farm Bill Black Mug", "$16.99", "33441560", "6adac43ee4dd88219a0b0ba0/65217/6405/ask-me-about-the-farm-bill-black-mug.jpg?camera_label=front&revision=2"),
    ("hemp-for-victory-phone-case", "Hemp for Victory Phone Case", "$24.99", "33441670", "6adac4b56396b31e550dd530/62582/97458/hemp-for-victory-phone-case.jpg?camera_label=front-and-side"),
    ("texas-grown-texas-regulated-phone-case", "Texas Grown Texas Regulated Phone Case", "$24.99", "33441698", "6adac576bb2ab6380804fa28/62582/97458/texas-grown-texas-regulated-phone-case.jpg?camera_label=front-and-side"),
    ("gone-fishin-for-better-laws-phone-case", "Gone Fishin for Better Laws Phone Case", "$24.99", "33441739", "6adac5f6301df6d475047b77/62582/97458/gone-fishin-for-better-laws-phone-case.jpg?camera_label=front-and-side"),
    ("veterans-for-medical-cannabis-hat", "Veterans for Medical Cannabis Hat", "$27.99", "33441802", "6adac6816396b31e550dd69b/125365/135054/veterans-for-medical-cannabis-hat.jpg?camera_label=front"),
    ("ask-me-about-the-farm-bill-hat", "Ask Me About the Farm Bill Hat", "$27.99", "33441859", "6adac70ebb2ab6380804fb75/125365/135054/ask-me-about-the-farm-bill-hat.jpg?camera_label=front"),
    ("ask-me-about-the-farm-bill-sticker", "Ask Me About the Farm Bill Sticker", "from $4.99", "33441944", "6adac7916396b31e550dd78b/45750/16655/ask-me-about-the-farm-bill-sticker.jpg?camera_label=front"),
    ("veterans-for-medical-cannabis-sticker", "Veterans for Medical Cannabis Sticker", "from $4.99", "33442062", "6adac82d9645f8de5f036ac7/45750/16655/veterans-for-medical-cannabis-sticker.jpg?camera_label=front"),
    ("gone-fishin-for-better-laws-sticker", "Gone Fishin for Better Laws Sticker", "from $4.99", "33442431", "6adac8ef2e39dc5ae40a443f/45750/16655/gone-fishin-for-better-laws-sticker.jpg?camera_label=front"),
    ("regulate-hat", "Regulate, Don't Ban Hat", "$27.99", "33270537", "6ad5351333bc1400d808a564/125365/135054/regulate-dont-ban-hat.jpg?camera_label=front"),
    ("ftp-tee", "Free the Plant Tee", "$25.99", "33258810", "6ad4f0e64a251b0fe7031511/18102/102044/free-the-plant-tee.jpg?camera_label=front-2"),
    ("savehemp-tee", "Save Hemp Retro Tee", "$25.99", "33259010", "6ad4f17f50ccb453d0057801/18102/102044/save-hemp-retro-tee.jpg?camera_label=front-2"),
    ("nerd-tee", "Cannabis Law Nerd Tee", "$25.99", "33259072", "6ad4f1a7c5bf429b0a08272d/18102/102044/cannabis-law-nerd-tee.jpg?camera_label=front-2"),
    ("txfight-tee", "Texas Hemp Fight Tee", "$25.99", "33259113", "6ad4f1c0c5bf429b0a08275b/18102/102044/texas-hemp-fight-tee.jpg?camera_label=front-2"),
    ("vote-tee", "Vote Like Cannabis Matters Tee", "$25.99", "33259143", "6ad4f1dbe2ff8ddc0b0e5b76/18102/102044/vote-like-cannabis-matters-tee.jpg?camera_label=front-2"),
    ("ftp-hoodie", "Free the Plant Hoodie", "$47.99", "33259222", "6ad4f3825691679ca00861ad/32920/98425/free-the-plant-hoodie.jpg?camera_label=back"),
    ("savehemp-hoodie", "Save Hemp Retro Hoodie", "$47.99", "33259262", "6ad4f39b33bc1400d8086dd4/32920/98425/save-hemp-retro-hoodie.jpg?camera_label=back"),
    ("nerd-hoodie", "Cannabis Law Nerd Hoodie", "$47.99", "33259297", "6ad4f3b47e86416ffc097345/32920/98425/cannabis-law-nerd-hoodie.jpg?camera_label=back"),
    ("txfight-hoodie", "Texas Hemp Fight Hoodie", "$47.99", "33259347", "6ad4f3ce52e33f00a407cfc6/32920/98425/texas-hemp-fight-hoodie.jpg?camera_label=back"),
    ("ftp-tumbler", "Free the Plant 20oz Tumbler", "$29.99", "33259456", "6ad4f546e2ff8ddc0b0e5ea9/108286/104182/free-the-plant-20oz-tumbler.jpg?camera_label=front"),
    ("savehemp-tumbler", "Save Hemp Retro 20oz Tumbler", "$29.99", "33259502", "6ad4f55fc5bf429b0a082b07/108286/104182/save-hemp-retro-20oz-tumbler.jpg?camera_label=front"),
    ("21plus-tumbler", "21+ and Regulated 20oz Tumbler", "$29.99", "33259518", "6ad4f5775691679ca00863ec/108286/104182/21-and-regulated-20oz-tumbler.jpg?camera_label=front"),
    ("regulate-tee", "Regulate, Don't Ban Tee", "$25.99", "33235134", "6ad3d87452df4727670b123d/18102/102044/regulate-dont-ban-tee.jpg?camera_label=front-2"),
    ("neon-tee", "Neon Logo Tee", "$25.99", "33235131", "6ad3d86219a9e3ef6c0947bf/18102/102044/neon-logo-tee.jpg?camera_label=front-2"),
    ("dec11-tee", "Dec 11 Hemp Fight Tee", "$25.99", "33235129", "6ad3d86b19a9e3ef6c0947c8/18102/102044/dec-11-hemp-fight-tee.jpg?camera_label=front-2"),
    ("texas-tee", "Texas Cannabis News Tee", "$25.99", "33235127", "6ad3d87119a9e3ef6c0947cb/18102/102044/texas-cannabis-news-tee.jpg?camera_label=front-2"),
    ("classic-tee", "Classic Logo Tee", "$25.99", "33235120", "6ad0c64a59ac88d91604b02e/18102/102044/classic-logo-tee.jpg?camera_label=front-2"),
    ("neon-hoodie", "Neon Logo Hoodie", "$47.99", "33235119", "6ad3e9e2dd9ae60ca105fac6/32920/98425/neon-logo-hoodie.jpg?camera_label=back"),
    ("classic-hoodie", "Classic Logo Hoodie", "$47.99", "33235116", "6ad0ce6bf0531fc34e0f53e5/32920/98425/classic-logo-hoodie.jpg?camera_label=back"),
    ("hat", "Classic Logo Hat", "$27.99", "33235117", "6ad0c80c59ac88d91604b16b/125365/135054/classic-logo-hat.jpg?camera_label=front"),
    ("beanie", "Embroidered Logo Beanie", "$27.99", "33236558", "6ad40b96753e48c73f0b13b5/116417/109382/embroidered-logo-beanie.jpg?camera_label=front"),
    ("neon-tumbler", "Neon Logo 20oz Tumbler", "$29.99", "33235122", "6ad3d9c17388cdd94b0a08d3/108286/104182/neon-logo-20oz-tumbler.jpg?camera_label=front&revision=1792690472000"),
    ("badge-tumbler", "Vintage Press Badge 20oz Tumbler", "$29.99", "33235121", "6ad3d9b63f189567a901e49a/108286/104182/vintage-press-badge-20oz-tumbler.jpg?camera_label=front"),
    ("classic-tumbler", "Classic Logo 20oz Tumbler", "$29.99", "33235118", "6ad0c89a97db1f1b0d0e6710/108286/104182/classic-logo-20oz-tumbler.jpg?camera_label=front"),
    ("mug", "Regulate, Don't Ban Black Mug", "$16.99", "33236223", "6ad408bd18e0243bd10d307d/65217/6405/regulate-dont-ban-black-mug.jpg?camera_label=front"),
    ("cooler", "Vintage Press Badge Can Cooler", "$11.99", "33236365", "6ad40a1b18e0243bd10d31e6/78460/38485/vintage-press-badge-can-cooler.jpg?camera_label=flat-front"),
    ("phone-regulate", "Regulate, Don't Ban Phone Case", "$24.99", "33236461", "6ad40aecf83da0fa840da465/62582/97458/regulate-dont-ban-phone-case.jpg?camera_label=front-and-side"),
    ("phone-classic", "J&H Cannabis News Classic Logo Phone Case", "$24.99", "33349247", "6ad7c7d249d13ef91309ec19/62582/97458/jh-cannabis-news-classic-logo-phone-case.jpg?camera_label=front-and-side"),
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
.shop{display:flex;gap:26px;align-items:flex-start;text-align:left;margin-top:22px}
.cats{position:sticky;top:14px;flex:0 0 190px;background:var(--panel);border-radius:12px;padding:10px}
.cats h2{font-size:.8rem;letter-spacing:.12em;color:var(--purple);margin:6px 10px 8px}
.cats button{display:flex;justify-content:space-between;width:100%;background:none;border:0;color:var(--white);
  font:inherit;font-weight:700;padding:10px 12px;border-radius:8px;cursor:pointer;text-align:left}
.cats button:hover{background:rgba(255,255,255,.06)}
.cats button.on{background:var(--red);color:#fff}
.cats .n{opacity:.7;font-weight:400}
.shop .merch-grid{flex:1;margin:0}
.shop .count{color:var(--grey,#aaa);font-size:.9rem;margin:0 0 12px}
.item[hidden]{display:none}
@media (max-width:760px){.shop{display:block}.cats{position:static;display:flex;gap:6px;overflow-x:auto;padding:6px;margin-bottom:16px}
  .cats h2{display:none}.cats button{width:auto;white-space:nowrap;gap:6px;flex:0 0 auto}}
</style>"""

CATS = [("shirts", "Shirts", "tee"), ("hoodies", "Hoodies", "hoodie"), ("mugs", "Mugs", "mug"),
        ("tumblers", "Tumblers", "tumbler"), ("hats", "Hats", ("hat", "beanie")), ("stickers", "Stickers", "sticker"),
        ("phone-cases", "Phone cases", "phone case"), ("can-coolers", "Can coolers", "cooler"),
        ("magnets", "Magnets", "magnet"), ("keychains", "Keychains", "keychain")]


def category(name):
    n = name.lower()
    for key, _, words in sorted(CATS, key=lambda c: c[0] != "hoodies"):   # "hoodie" before "tee" style matches
        if any(re.search(r"\b" + w + r"\b", n) for w in ((words,) if isinstance(words, str) else words)):
            return key
    raise ValueError("no merch category for " + name)


FILTER_JS = """<script>
(function(){
  var btns=[].slice.call(document.querySelectorAll('.cats button')),items=[].slice.call(document.querySelectorAll('.item')),
      cnt=document.querySelector('.shop .count');
  function show(c){
    var n=0;items.forEach(function(it){var on=c==='all'||it.dataset.cat===c;it.hidden=!on;if(on)n++;});
    btns.forEach(function(b){b.classList.toggle('on',b.dataset.cat===c);});
    cnt.textContent=n+(n===1?' item':' items');
  }
  btns.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.cat);
    history.replaceState(null,'',b.dataset.cat==='all'?location.pathname:'#'+b.dataset.cat);});});
  var h=location.hash.slice(1);show(btns.some(function(b){return b.dataset.cat===h;})?h:'all');
})();
</script>"""

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
    order = [c[0] for c in CATS]
    items = sorted(P, key=lambda p: order.index(category(p[1])))   # stable: newest-first order kept inside a category
    counts = {k: sum(category(p[1]) == k for p in P) for k in order}
    for slug, name, price, pid, _ in items:
        if preview:
            body = f'<span class="price">{price}</span><br><a class="btn" href="{STORE}/product/{pid}">View in store</a>'
        else:
            body = '<span class="soon">Coming soon</span>'
        cards.append(f'<div class="item" data-cat="{category(name)}"><img src="merch/{slug}.jpg" alt="{esc(name)}" loading="lazy">'
                     f'<div class="info"><h3>{esc(name)}</h3>{body}</div></div>')
    side = ('<aside class="cats"><h2>SHOP BY CATEGORY</h2>'
            f'<button data-cat="all">All <span class="n">{len(P)}</span></button>'
            + "".join(f'<button data-cat="{k}">{label} <span class="n">{counts[k]}</span></button>'
                      for k, label, _ in CATS if counts[k]) + '</aside>')
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
            f'<nav>{nav}</nav>\n<div class="wrap center">\n  {top}\n  <div class="shop">\n  {side}\n  <div style="flex:1">'
            '<p class="count"></p>\n  <div class="merch-grid">\n    '
            + "\n    ".join(cards) + "\n  </div></div>\n  </div>\n</div>\n" + FILTER_JS + "\n" + FOOT)


if __name__ == "__main__":
    fetch()
    idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    nav = idx.split("<nav>")[1].split("</nav>")[0].replace(' class="active"', '')
    open(os.path.join(SITE, "merch.html"), "w", encoding="utf-8", newline="\n").write(page(False, nav))
    open(os.path.join(SITE, "merch-preview-jh7q.html"), "w", encoding="utf-8", newline="\n").write(page(True, nav))
    print("built", len(P), "items")
