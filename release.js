// Time-gated blocks, so scheduled episodes go live on the site at their YouTube release times.
//   data-show-after="<ISO>"  hidden before that moment
//   data-hide-after="<ISO>"  hidden from that moment on
// A block can carry both (e.g. "latest episode" until the next one replaces it).
// Iframes inside a visible block get their src from data-src.
(function () {
  const now = Date.now();
  document.querySelectorAll("[data-show-after], [data-hide-after]").forEach(el => {
    const shown = (!el.dataset.showAfter || now >= Date.parse(el.dataset.showAfter)) &&
                  (!el.dataset.hideAfter || now < Date.parse(el.dataset.hideAfter));
    el.hidden = !shown;
    if (shown) el.querySelectorAll("iframe[data-src]").forEach(f => { if (!f.src) f.src = f.dataset.src; });
  });
})();
