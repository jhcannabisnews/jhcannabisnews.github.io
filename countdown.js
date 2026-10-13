// Live countdowns. Any element with data-target="<ISO date>" ticks every second.
// data-kind="law" shows IN EFFECT once the date passes; anything else shows PASSED.
// The home page "next big date" box (#next-date) picks the soonest upcoming entry below.
const JH_DATES = [
  { when: "2026-10-30T09:00:00-05:00", kind: "event", what: "Texas — Travis County hearing on the THC ban" },
  { when: "2026-11-03T00:00:00-05:00", kind: "event", what: "Election Day — Massachusetts Question 8 & the Idaho amendment" },
  { when: "2026-11-12T00:00:00-05:00", kind: "law",   what: "Federal — delta-8 & lab-made cannabinoids lose hemp status" },
  { when: "2026-12-11T00:00:00-05:00", kind: "law",   what: "Federal — 0.4 mg total-THC cap on hemp products" },
];

function jhFormat(ms, kind) {
  if (ms <= 0) {
    if (-ms < 86400000) return { text: "HAPPENING TODAY", live: true };
    return { text: kind === "law" ? "IN EFFECT" : "PASSED", live: kind === "law" };
  }
  const s = Math.floor(ms / 1000);
  const d = Math.floor(s / 86400), h = Math.floor(s % 86400 / 3600),
        m = Math.floor(s % 3600 / 60), sec = s % 60;
  const pad = n => String(n).padStart(2, "0");
  return { text: `${d}d ${pad(h)}h ${pad(m)}m ${pad(sec)}s`, live: false };
}

function jhTick() {
  const now = Date.now();
  document.querySelectorAll("[data-target]").forEach(el => {
    const r = jhFormat(new Date(el.dataset.target) - now, el.dataset.kind);
    el.textContent = r.text;
    el.classList.toggle("live", r.live);
  });
}

function jhNextDate() {
  const box = document.getElementById("next-date");
  if (!box) return;
  const now = Date.now();
  const next = JH_DATES.find(d => new Date(d.when) - now > -86400000);
  if (!next) { box.remove(); return; }
  box.innerHTML =
    `<div class="label">⏱ NEXT BIG DATE</div>` +
    `<div class="what">${next.what}</div>` +
    `<div class="countdown" data-target="${next.when}" data-kind="${next.kind}"></div>` +
    `<a href="watchlist.html" style="color:var(--purple);font-size:.9rem">Full watch list →</a>`;
}

// Site-wide federal hemp-ban banner under the nav (every page loads this script).
// Shows both deadlines until the day after the second one.
function jhBanner() {
  const nav = document.querySelector("nav");
  if (!nav || document.getElementById("hemp-banner")) return;
  if (Date.now() > Date.parse("2026-12-12T00:00:00-05:00")) return;
  const b = document.createElement("a");
  b.id = "hemp-banner"; b.href = "watchlist.html";
  b.innerHTML =
    `<span class="hb-label">⏳ FEDERAL HEMP BAN</span>` +
    `<span>Delta-8 &amp; lab-made THC: <b data-target="2026-11-12T00:00:00-05:00" data-kind="law"></b></span>` +
    `<span>0.4 mg THC cap: <b data-target="2026-12-11T00:00:00-05:00" data-kind="law"></b></span>` +
    `<span class="hb-more">Watch list →</span>`;
  nav.after(b);
}

jhBanner();
jhNextDate();
jhTick();
setInterval(jhTick, 1000);
