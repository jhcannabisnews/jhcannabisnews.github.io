"""J&H Cannabis News package insert card for Printify (6x4 in, 1795x1193 px upload, ~4 mm white border).
White/transparent background (Printify: solid fills can over-saturate), black text, pink/purple/red accents, never yellow.
Output: Desktop\\J&H Cannabis News\\Printify\\Store uploads\\insert-card.png (+ a preview on white)."""
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

W, H = 1795, 1193
OUT = r"C:\Users\THEVI\OneDrive\Desktop\J&H Cannabis News\Printify\Store uploads"
LOGO = r"C:\Users\THEVI\OneDrive\Desktop\J&H Cannabis News\Brand\J&H Cannabis News - Round Logo.png"
F = r"C:\Windows\Fonts"
VIBES = r"C:\Users\THEVI\Videos\CannaNews\fonts\GreatVibes-Regular.ttf"
BLACK, GREY, RED = (14, 14, 18), (70, 70, 78), (220, 30, 45)
PINK, PURPLE = (255, 45, 149), (150, 48, 255)
SUB = "https://www.youtube.com/@jhcannabisnews?sub_confirmation=1"

font = lambda name, size: ImageFont.truetype(os.path.join(F, name), size)
card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(card)


def gradient_bar(y, x0=110, x1=W - 110, h=10):
    for x in range(x0, x1):
        t = (x - x0) / (x1 - x0)
        c = tuple(int(PINK[i] + (PURPLE[i] - PINK[i]) * t) for i in range(3))
        d.line([(x, y), (x, y + h)], fill=c + (255,))


gradient_bar(110)
gradient_bar(H - 120)

# left: round logo + slogan
logo = Image.open(LOGO).convert("RGBA")
logo.thumbnail((470, 470), Image.LANCZOS)
lx, ly = 120 + (500 - logo.width) // 2, 175
card.alpha_composite(logo, (lx, ly))
d.text((370, ly + logo.height + 70), "Regulate, don't ban.", font=font("segoeuib.ttf", 46), fill=RED, anchor="mm")

# right: thank-you block
x = 680
d.text((x, 150), "THANK YOU", font=font("ariblk.ttf", 138), fill=BLACK)
d.text((x + 4, 330), "for supporting J&H Cannabis News", font=font("segoeuib.ttf", 50), fill=PURPLE)
msg = ["Every order helps a real husband and wife in",
       "Texas keep covering cannabis law: the bills,",
       "the courts and the votes. We hope you love it."]
for i, line in enumerate(msg):
    d.text((x + 4, 420 + i * 56), line, font=font("segoeui.ttf", 40), fill=GREY)
d.text((x + 4, 590), "James & Hope", font=ImageFont.truetype(VIBES, 92), fill=PINK)

# bottom: QR to subscribe + links
qr = qrcode.QRCode(border=1, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(SUB)
qr.make(fit=True)
q = qr.make_image(fill_color=BLACK, back_color="white").convert("RGBA").resize((250, 250), Image.NEAREST)
qy = 790
card.alpha_composite(q, (x, qy))
tx = x + 290
d.text((tx, qy + 6), "Scan to subscribe", font=font("segoeuib.ttf", 44), fill=BLACK)
links = [("YouTube", "youtube.com/@jhcannabisnews"),
         ("Website", "jhcannabisnews.github.io"),
         ("Discord", "discord.gg/EXqpgyQyBq")]
for i, (k, v) in enumerate(links):
    y = qy + 80 + i * 54
    d.text((tx, y), k, font=font("segoeuib.ttf", 34), fill=PURPLE)
    d.text((tx + 160, y), v, font=font("segoeui.ttf", 34), fill=BLACK)

# Printify's safe area (dashed line) sits ~120 px in from each edge; shrink everything to clear it with room to spare
SCALE = 0.86
small = card.resize((round(W * SCALE), round(H * SCALE)), Image.LANCZOS)
card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
card.alpha_composite(small, ((W - small.width) // 2, (H - small.height) // 2))

os.makedirs(OUT, exist_ok=True)
out = os.path.join(OUT, "insert-card.png")
card.save(out, dpi=(300, 300))
prev = Image.new("RGB", (W, H), "white")
prev.paste(card, (0, 0), card)
ImageDraw.Draw(prev).rectangle([47, 47, W - 48, H - 48], outline=(200, 200, 200), width=3)  # ~4 mm border line
prev.save(os.path.join(OUT, "insert-card-preview.jpg"), quality=92)
print(out)
