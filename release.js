// Time-gated blocks, so a scheduled episode goes live on the site at its YouTube release time.
//   data-show-after="<ISO>"  hidden until that moment; iframes inside get src from data-src then
//   data-hide-after="<ISO>"  shown until that moment
(function () {
  const now = Date.now();
  document.querySelectorAll("[data-show-after]").forEach(el => {
    if (now >= Date.parse(el.dataset.showAfter)) {
      el.hidden = false;
      el.querySelectorAll("iframe[data-src]").forEach(f => { f.src = f.dataset.src; });
    } else {
      el.hidden = true;
    }
  });
  document.querySelectorAll("[data-hide-after]").forEach(el => {
    el.hidden = now >= Date.parse(el.dataset.hideAfter);
  });
})();
