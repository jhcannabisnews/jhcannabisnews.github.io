// Renders data/headlines.json into <ul id="headlines" data-limit="N">.
// Reads the raw GitHub copy first so a fresh fetch shows up without waiting for a Pages rebuild.
const JH_SOURCES = [
  "https://raw.githubusercontent.com/jhcannabisnews/jhcannabisnews.com/main/data/headlines.json",
  "data/headlines.json",
];

function jhAgo(iso) {
  const mins = Math.round((Date.now() - new Date(iso)) / 60000);
  if (mins < 60) return `${Math.max(mins, 1)} min ago`;
  const hrs = Math.round(mins / 60);
  if (hrs < 24) return `${hrs} hr${hrs > 1 ? "s" : ""} ago`;
  const days = Math.round(hrs / 24);
  return `${days} day${days > 1 ? "s" : ""} ago`;
}

function jhEsc(s) {
  return String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

async function jhLoadHeadlines() {
  for (const url of JH_SOURCES) {
    try {
      const r = await fetch(url, { cache: "no-store" });
      if (r.ok) return await r.json();
    } catch (e) { /* try the next source */ }
  }
  return null;
}

(async () => {
  const list = document.getElementById("headlines");
  if (!list) return;
  const data = await jhLoadHeadlines();
  if (!data || !data.items.length) {
    list.innerHTML = "<li>Headlines are refreshing — check back in a few minutes.</li>";
    return;
  }
  const limit = parseInt(list.dataset.limit || "0", 10);
  const render = filter => {
    let items = data.items.filter(i => !filter || i.tags.includes(filter));
    if (limit) items = items.slice(0, limit);
    list.innerHTML = items.map(i =>
      `<li><a href="${jhEsc(i.url)}" target="_blank" rel="noopener">${jhEsc(i.title)}</a>` +
      `<div class="meta">${i.tags.map(t => `<span class="chip${t === "Federal" ? " federal" : ""}">${jhEsc(t)}</span>`).join("")}` +
      `${jhEsc(i.source)} · ${jhAgo(i.published)}</div></li>`).join("") ||
      "<li>No headlines for this filter right now.</li>";
  };
  render(null);

  const upd = document.getElementById("headlines-updated");
  if (upd) upd.textContent = `Updated ${jhAgo(data.updated)}`;

  const bar = document.getElementById("headline-filters");
  if (bar) {
    const counts = {};
    data.items.forEach(i => i.tags.forEach(t => counts[t] = (counts[t] || 0) + 1));
    const tags = Object.keys(counts).sort((a, b) =>
      (b === "Federal") - (a === "Federal") || counts[b] - counts[a]);
    bar.innerHTML = [`<button class="on" data-f="">All</button>`]
      .concat(tags.map(t => `<button data-f="${jhEsc(t)}">${jhEsc(t)} (${counts[t]})</button>`)).join("");
    bar.addEventListener("click", e => {
      const b = e.target.closest("button");
      if (!b) return;
      bar.querySelectorAll("button").forEach(x => x.classList.toggle("on", x === b));
      render(b.dataset.f || null);
    });
  }
})();
