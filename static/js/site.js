(function () {
  "use strict";
  var root = document.documentElement;
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---- header: transparent over the hero, solid once you scroll
  var ticking = false;
  function onScroll() {
    root.classList.toggle("is-scrolled", window.scrollY > 40);
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  // ---- mobile sidebar
  var drawer = document.querySelector("[data-drawer]");
  var openBtn = document.querySelector("[data-drawer-open]");
  if (drawer && openBtn) {
    var panel = drawer.querySelector(".drawer-panel");
    var lastFocus = null;
    var open = function () {
      lastFocus = document.activeElement;
      root.classList.add("drawer-open");
      drawer.setAttribute("aria-hidden", "false");
      openBtn.setAttribute("aria-expanded", "true");
      setTimeout(function () { var f = drawer.querySelector(".drawer-close"); if (f) f.focus(); }, 60);
    };
    var close = function () {
      root.classList.remove("drawer-open");
      drawer.setAttribute("aria-hidden", "true");
      openBtn.setAttribute("aria-expanded", "false");
      if (lastFocus) lastFocus.focus();
    };
    openBtn.addEventListener("click", open);
    drawer.querySelectorAll("[data-drawer-close]").forEach(function (b) { b.addEventListener("click", close); });
    drawer.querySelectorAll(".drawer-body a").forEach(function (a) { a.addEventListener("click", close); });
    document.addEventListener("keydown", function (e) {
      if (!root.classList.contains("drawer-open")) return;
      if (e.key === "Escape") close();
      if (e.key === "Tab") {                                   // keep focus inside the sidebar
        var items = panel.querySelectorAll("a, button");
        var first = items[0], last = items[items.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    var tx = null;                                            // swipe right to close
    panel.addEventListener("touchstart", function (e) { tx = e.touches[0].clientX; }, { passive: true });
    panel.addEventListener("touchend", function (e) {
      if (tx !== null && e.changedTouches[0].clientX - tx > 70) close();
      tx = null;
    });
  }

  // ---- reveal on scroll
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !still) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  // ---- package page: highlight the current section in the sub-menu, show the mobile booking bar
  var subnav = document.querySelector("[data-subnav]");
  if (subnav && "IntersectionObserver" in window) {
    var links = {};
    subnav.querySelectorAll("a").forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        Object.keys(links).forEach(function (k) { links[k].classList.toggle("is-active", k === en.target.id); });
        var a = links[en.target.id];
        if (a && a.scrollIntoView && subnav.scrollWidth > subnav.clientWidth) a.scrollIntoView({ block: "nearest", inline: "center" });
      });
    }, { rootMargin: "-35% 0px -60% 0px" });
    Object.keys(links).forEach(function (id) { var s = document.getElementById(id); if (s) spy.observe(s); });
  }
  var bar = document.querySelector("[data-book-bar]");
  var book = document.getElementById("book");
  if (bar && book && "IntersectionObserver" in window) {
    var heroGone = false, formVisible = false;
    var update = function () { bar.classList.toggle("is-visible", heroGone && !formVisible); };
    var hero = document.querySelector(".page-hero");
    if (hero) new IntersectionObserver(function (e) { heroGone = !e[0].isIntersecting; update(); }).observe(hero);
    new IntersectionObserver(function (e) { formVisible = e[0].isIntersecting; update(); }, { threshold: 0.15 }).observe(book);
  }
})();

// ---- booking forms -> WhatsApp message
(function () {
  "use strict";
  var money = function (n) { return "$" + Number(n).toLocaleString("en-US"); };
  document.querySelectorAll("[data-book-form]").forEach(function (form) {
    var people = form.querySelector("[name=people]");
    var estimate = form.querySelector("[data-estimate]");
    var tiers = Array.prototype.slice.call(document.querySelectorAll("[data-tier]"));

    function updateEstimate() {
      if (!people || !tiers.length) return;
      var n = parseInt(people.value, 10);
      var match = null;
      tiers.forEach(function (row) {
        var hit = n >= +row.dataset.min && n <= +row.dataset.max;
        row.classList.toggle("is-match", hit);
        if (hit) match = row;
      });
      if (!estimate) return;
      if (!n || n < 1) { estimate.hidden = true; return; }
      estimate.hidden = false;
      if (match) {
        var price = +match.dataset.price;
        estimate.textContent = n === 1
          ? "Estimate: " + money(price) + " (private trip)"
          : "Estimate: " + money(price) + " × " + n + " = " + money(price * n);
      } else {
        estimate.textContent = "We'll confirm the price for " + n + " people on WhatsApp.";
      }
    }
    if (people) { people.addEventListener("input", updateEstimate); updateEstimate(); }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var val = function (name) { var el = form.elements[name]; return el ? el.value.trim() : ""; };
      var trip = form.dataset.package || val("trip");
      var lines = ["Hello Kili Wild Adventure!"];
      lines.push(trip ? "I'd like to book: " + trip : "I'd like to plan a trip.");
      if (val("name")) lines.push("Name: " + val("name"));
      if (val("date")) lines.push("Travel date: " + val("date"));
      if (val("people")) lines.push("Number of people: " + val("people"));
      if (estimate && !estimate.hidden && estimate.textContent) lines.push(estimate.textContent);
      if (val("message")) lines.push("", val("message"));
      if (form.dataset.package) lines.push("", window.location.href);
      var url = "https://wa.me/" + form.dataset.number + "?text=" + encodeURIComponent(lines.join("\n"));
      window.open(url, "_blank", "noopener");
    });
  });
})();

// ---- gallery filters + lightbox
(function () {
  "use strict";
  var gallery = document.querySelector("[data-gallery]");
  if (!gallery) return;
  var figures = Array.prototype.slice.call(gallery.querySelectorAll("figure"));
  var filters = document.querySelector("[data-filters]");
  if (filters) {
    filters.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-filter]");
      if (!btn) return;
      filters.querySelectorAll("button").forEach(function (b) { b.classList.toggle("is-active", b === btn); });
      var kind = btn.dataset.filter;
      figures.forEach(function (f) { f.hidden = kind !== "all" && f.dataset.kind !== kind; });
    });
  }
  var box = document.querySelector("[data-lightbox]");
  if (!box || typeof box.showModal !== "function") return;
  var img = box.querySelector("[data-lb-img]");
  var cap = box.querySelector("[data-lb-cap]");
  var current = 0;
  function visible() { return figures.filter(function (f) { return !f.hidden; }); }
  function show(fig) {
    var pic = fig.querySelector("img");
    img.src = pic.currentSrc || pic.src; img.alt = pic.alt; cap.textContent = pic.alt;
    current = visible().indexOf(fig);
  }
  function step(d) {
    var list = visible(); if (!list.length) return;
    current = (current + d + list.length) % list.length; show(list[current]);
  }
  gallery.addEventListener("click", function (e) {
    var btn = e.target.closest("button[data-open]");
    if (!btn) return;
    show(btn.closest("figure")); box.showModal();
  });
  box.querySelector("[data-lb-close]").addEventListener("click", function () { box.close(); });
  box.querySelector("[data-lb-prev]").addEventListener("click", function () { step(-1); });
  box.querySelector("[data-lb-next]").addEventListener("click", function () { step(1); });
  box.addEventListener("click", function (e) { if (e.target === box) box.close(); });
  box.addEventListener("keydown", function (e) { if (e.key === "ArrowLeft") step(-1); if (e.key === "ArrowRight") step(1); });
  var sx = null;
  box.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
  box.addEventListener("touchend", function (e) {
    if (sx === null) return;
    var dx = e.changedTouches[0].clientX - sx;
    if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1);
    sx = null;
  });
})();

// ---- hero slideshow (crossfade + slow zoom, CSS does the zoom)
(function () {
  "use strict";
  var root = document.querySelector("[data-slider]");
  if (!root) return;
  var slides = root.querySelectorAll("[data-slide]");
  var caps = root.querySelectorAll("[data-caption]");
  var dots = root.querySelectorAll("[data-dot]");
  var MS = 6500, i = 0, timer = null;
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  root.style.setProperty("--slide-ms", MS + "ms");
  function go(n) {
    i = (n + slides.length) % slides.length;
    slides.forEach(function (s, k) { s.classList.toggle("is-active", k === i); });
    caps.forEach(function (c, k) { c.classList.toggle("is-active", k === i); });
    dots.forEach(function (d, k) {
      d.classList.remove("is-active"); d.classList.toggle("is-done", k < i);
      d.setAttribute("aria-selected", k === i ? "true" : "false");
    });
    void root.offsetWidth;
    if (dots[i]) dots[i].classList.add("is-active");
    var next = slides[(i + 1) % slides.length].querySelector("img");
    if (next && next.loading === "lazy") next.loading = "eager";
    schedule();
  }
  function schedule() {
    clearTimeout(timer);
    if (!still && !document.hidden) timer = setTimeout(function () { go(i + 1); }, MS);
  }
  dots.forEach(function (d) { d.addEventListener("click", function () { go(+d.dataset.dot); }); });
  document.addEventListener("visibilitychange", schedule);
  var x0 = null;
  root.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  root.addEventListener("touchend", function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 60) go(i + (dx < 0 ? 1 : -1));
    x0 = null;
  });
  go(0);
})();

// ---- talking map
(function () {
  "use strict";
  var stage = document.querySelector("[data-map]");
  var dataEl = document.getElementById("map-places");
  if (!stage || !dataEl) return;
  var places = JSON.parse(dataEl.textContent);
  var order = JSON.parse(document.getElementById("map-tour").textContent);
  var byKey = {};
  places.forEach(function (p) { byKey[p.key] = p; });

  var svg = stage.querySelector("svg");
  var bubble = stage.querySelector("[data-map-bubble]");
  var bubbleText = stage.querySelector("[data-map-bubble-text]");
  var card = document.querySelector("[data-map-card]");
  var el = function (s) { return card.querySelector(s); };
  var listenBtn = el("[data-mc-listen]"), listenLabel = el("[data-mc-listen-label]");
  var tourBtn = document.querySelector("[data-map-tour]");
  var tourLabel = document.querySelector("[data-map-tour-label]");
  var synth = window.speechSynthesis || null;
  var current = null, typing = null, touring = false, tourIdx = 0, tourTimer = null;

  var ROUTES = { tarangire: "safari", manyara: "safari", ngorongoro: "safari", serengeti: "safari",
                 kilimanjaro: "climb", moshi: "climb", meru: "meru", arusha: "safari" };

  function pickVoice() {
    if (!synth) return null;
    var voices = synth.getVoices();
    return voices.find(function (v) { return /en-(GB|ZA|KE|TZ|NG)/i.test(v.lang); })
        || voices.find(function (v) { return /^en/i.test(v.lang); }) || null;
  }

  function stopSpeaking() {
    if (synth) synth.cancel();
    listenBtn.classList.remove("is-speaking");
    listenLabel.textContent = "Listen";
  }

  function speak(p, onEnd) {
    if (!synth) { if (onEnd) tourTimer = setTimeout(onEnd, 7000); return; }
    stopSpeaking();
    var u = new SpeechSynthesisUtterance(p.say);
    var v = pickVoice(); if (v) u.voice = v;
    u.rate = 0.96; u.pitch = 1;
    u.onend = function () {
      listenBtn.classList.remove("is-speaking"); listenLabel.textContent = "Listen";
      if (onEnd) onEnd();
    };
    u.onerror = u.onend;
    listenBtn.classList.add("is-speaking"); listenLabel.textContent = "Stop";
    synth.speak(u);
  }

  function placeBubble(p) {
    var r = svg.getBoundingClientRect();
    bubble.className = "map-bubble";
    bubble.style.left = (p.x / 960 * 100) + "%";
    bubble.style.top = (p.y / 720 * 100) + "%";
    if (p.y < 260) bubble.classList.add("below");
    if (p.x > 700) bubble.classList.add("flip-left");
    else if (p.x < 260) bubble.classList.add("flip-right");
    bubble.hidden = false;
    // replay the pop-in animation
    bubble.style.animation = "none"; void bubble.offsetWidth; bubble.style.animation = "";
    return r;
  }

  function typeOut(text) {
    clearInterval(typing);
    var parts = text.split(/(?<=[.!?])\s/);
    var first = parts[0].length < 45 && parts[1] ? parts[0] + " " + parts[1] : parts[0];  // a sentence or two
    var n = 0;
    bubbleText.textContent = "";
    typing = setInterval(function () {
      n += 2;
      bubbleText.textContent = first.slice(0, n);
      if (n >= first.length) clearInterval(typing);
    }, 28);
  }

  function select(key, opts) {
    opts = opts || {};
    var p = byKey[key];
    if (!p) return;
    current = p;
    svg.querySelectorAll("[data-pin]").forEach(function (g) { g.classList.toggle("is-active", g.dataset.pin === key); });
    card.querySelectorAll("[data-chip]").forEach(function (c) { c.classList.toggle("is-active", c.dataset.chip === key); });
    svg.querySelectorAll("[data-route]").forEach(function (r) { r.classList.toggle("is-lit", r.dataset.route === ROUTES[key]); });

    card.classList.remove("is-swap"); void card.offsetWidth; card.classList.add("is-swap");
    el("[data-mc-img]").src = p.photo;
    el("[data-mc-img]").alt = p.name;
    el("[data-mc-fact]").textContent = p.fact;
    el("[data-mc-sw]").textContent = p.sw;
    el("[data-mc-name]").textContent = p.name;
    el("[data-mc-say]").textContent = p.say;
    var link = el("[data-mc-link]");
    link.href = p.url;
    link.firstChild.textContent = p.cta + " ";
    var more = el("[data-mc-more]");
    if (more && p.more) { more.href = p.more; more.textContent = "Read the full story of " + p.name + " \u2192"; }

    placeBubble(p);
    typeOut(p.say);
    if (opts.speak) speak(p, opts.onEnd);
  }

  // pins + chips
  svg.querySelectorAll("[data-pin]").forEach(function (g) {
    var go = function () { stopTour(); select(g.dataset.pin, { speak: !!synth }); };
    g.addEventListener("click", go);
    g.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(); } });
  });
  card.querySelectorAll("[data-chip]").forEach(function (c) {
    c.addEventListener("click", function () { stopTour(); select(c.dataset.chip, { speak: !!synth }); });
  });
  listenBtn.addEventListener("click", function () {
    if (listenBtn.classList.contains("is-speaking")) { stopSpeaking(); stopTour(); return; }
    if (!current) { select(order[0], { speak: true }); return; }
    speak(current);
  });

  // guided tour
  function nextStop() {
    if (!touring) return;
    if (tourIdx >= order.length) { stopTour(); return; }
    var key = order[tourIdx++];
    select(key, { speak: true, onEnd: function () { tourTimer = setTimeout(nextStop, 700); } });
  }
  function startTour() {
    touring = true; tourIdx = 0;
    tourLabel.textContent = "Stop the tour";
    tourBtn.classList.add("is-touring");
    stage.scrollIntoView({ behavior: "smooth", block: "center" });
    nextStop();
  }
  function stopTour() {
    if (!touring) return;
    touring = false; clearTimeout(tourTimer); stopSpeaking();
    tourLabel.textContent = "Play the talking tour";
    tourBtn.classList.remove("is-touring");
  }
  tourBtn.addEventListener("click", function () { touring ? stopTour() : startTour(); });
  if (synth && synth.onvoiceschanged !== undefined) synth.onvoiceschanged = function () {};

  // first visit: gently introduce Kilimanjaro when the map scrolls into view (no sound until the user asks)
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting && !current) { select("kilimanjaro"); io.disconnect(); }
    }, { threshold: 0.4 });
    io.observe(stage);
  }
})();

// ---- swipe rail dots (why-us cards on phones)
(function () {
  "use strict";
  document.querySelectorAll("[data-rail]").forEach(function (rail) {
    var dots = rail.parentNode.querySelectorAll("[data-rail-dots] i");
    var cards = rail.querySelectorAll(".why-card");
    if (!dots.length || !cards.length) return;
    var tick = false;
    rail.addEventListener("scroll", function () {
      if (tick) return; tick = true;
      requestAnimationFrame(function () {
        var w = cards[0].offsetWidth + 14;
        var i = Math.min(cards.length - 1, Math.round(rail.scrollLeft / w));
        dots.forEach(function (d, k) { d.classList.toggle("on", k === i); });
        tick = false;
      });
    }, { passive: true });
  });
})();

// ======================================================================
// "Ultra" layer: hero parallax, counters, summit story, wildlife rail,
// big marquee, desktop cursor + 3D tilt + magnetic buttons
// ======================================================================
(function () {
  "use strict";
  var root = document.documentElement;
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var vh = window.innerHeight;
  var visible = {};                                     // which animated sections are on screen
  var watch = function (el, key) {
    if (!el || !("IntersectionObserver" in window)) { visible[key] = !!el; return; }
    new IntersectionObserver(function (e) { visible[key] = e[0].isIntersecting; }, { rootMargin: "100px 0px" }).observe(el);
  };
  var hex = function (h) { h = h.replace("#", ""); return [0, 2, 4].map(function (i) { return parseInt(h.substr(i, 2), 16); }); };
  var mixc = function (a, b, k) { return a.map(function (v, i) { return Math.round(v + (b[i] - v) * k); }); };
  var clamp = function (x) { return Math.max(0, Math.min(1, x)); };

  // ---- counters
  var counters = document.querySelectorAll("[data-count]");
  if (counters.length && "IntersectionObserver" in window && !still) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        cio.unobserve(e.target);
        var el = e.target, end = +el.dataset.count, t0 = performance.now(), dur = end > 100 ? 1700 : 900;
        (function tick(now) {
          var k = Math.min(1, (now - t0) / dur);
          el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))).toLocaleString("en-US");
          if (k < 1) requestAnimationFrame(tick);
        })(t0);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { c.textContent = "0"; cio.observe(c); });
  }

  // ---- hero parallax
  var hero = document.querySelector("[data-hero]");
  var heroSlides = hero && hero.querySelector(".slides");
  var heroContent = document.querySelector("[data-hero-content]");
  watch(hero, "hero");
  function heroUpdate() {
    if (!hero || still || !visible.hero) return;
    var y = window.scrollY, k = y / vh;
    heroSlides.style.transform = "translate3d(0," + (y * 0.38) + "px,0) scale(" + (1 + k * 0.1) + ")";
    heroContent.style.transform = "translate3d(0," + (y * 0.2) + "px,0)";
    heroContent.style.opacity = Math.max(0, 1 - k * 1.15);
  }

  // ---- summit story
  var summit = document.querySelector("[data-summit]");
  var S = null;
  if (summit) {
    var trail = summit.querySelector("[data-trail]");
    var imgs = summit.querySelectorAll("[data-zone-img]");
    S = {
      bg: summit.querySelector("[data-summit-bg]"), alt: summit.querySelector("[data-alt]"),
      bar: summit.querySelector("[data-alt-bar]"), texts: summit.querySelectorAll("[data-zone-text]"),
      steps: summit.querySelectorAll("[data-zone-step]"), imgs: imgs, trail: trail,
      glow: summit.querySelector("[data-trail-glow]"),
      label: summit.querySelector("[data-window-label]"),
      climber: summit.querySelector("[data-climber]"), cta: summit.querySelector("[data-summit-cta]"),
      L: trail.getTotalLength(), cur: -1, lastAlt: -1,
      zones: Array.prototype.map.call(imgs, function (im) {
        return { c: hex(im.dataset.color), low: +im.dataset.low, high: +im.dataset.high };
      })
    };
    trail.style.strokeDasharray = S.L;
    trail.style.strokeDashoffset = S.L;
    S.glow.style.strokeDasharray = S.L;
    S.glow.style.strokeDashoffset = S.L;
    imgs.forEach(function (im) { im.loading = "eager"; });   // all five are needed as you scroll
    watch(summit, "summit");
  }
  function summitUpdate() {
    if (!S || !visible.summit) return;
    var r = summit.getBoundingClientRect();
    var total = summit.offsetHeight - vh;
    var p = clamp(-r.top / total);
    var N = S.zones.length, f = Math.min(p * N, N - 0.0001), i = Math.floor(f), local = f - i;
    var z = S.zones[i], nz = S.zones[Math.min(N - 1, i + 1)];
    var alt = Math.round(z.low + (z.high - z.low) * (p >= 0.999 ? 1 : local));
    if (alt !== S.lastAlt) { S.alt.textContent = alt.toLocaleString("en-US"); S.lastAlt = alt; }
    S.bar.style.width = (p * 100) + "%";
    S.bg.style.backgroundColor = "rgb(" + mixc(z.c, nz.c, clamp((local - 0.65) / 0.35)).join(",") + ")";
    var stars = i === 3 ? clamp(local * 2) : i === 4 ? clamp(1 - local * 1.5) : i === 2 ? clamp((local - 0.7) * 2) : 0;
    summit.style.setProperty("--stars", stars.toFixed(3));
    summit.style.setProperty("--flag", p > 0.96 ? 1 : 0);
    if (i !== S.cur) {
      S.cur = i;
      S.texts.forEach(function (t, k) { t.classList.toggle("is-on", k === i); });
      if (S.label) S.label.textContent = S.texts[i].querySelector("h3").textContent;
      S.imgs.forEach(function (t, k) { t.classList.toggle("is-on", k === i); });
      S.steps.forEach(function (t, k) { t.classList.toggle("is-on", k <= i); t.classList.toggle("is-current", k === i); });
    }
    var len = S.L * p;
    S.trail.style.strokeDashoffset = S.L - len;
    S.glow.style.strokeDashoffset = S.L - len;
    var pt = S.trail.getPointAtLength(len);
    S.climber.setAttribute("transform", "translate(" + pt.x.toFixed(1) + " " + pt.y.toFixed(1) + ")");
    S.cta.classList.toggle("is-on", p > 0.9);
  }

  // ---- wildlife rail: pinned + horizontal on desktop, swipe on phones
  var wild = document.querySelector("[data-wild]");
  var W = wild && { track: wild.querySelector("[data-wild-track]"), rail: wild.querySelector("[data-wild-rail]"),
                    bar: wild.querySelector("[data-wild-bar]"), dist: 0, pinned: false };
  function setupWild() {
    if (!W) return;
    var desk = window.innerWidth > 900 && !still;
    wild.classList.toggle("is-pinned", desk);
    W.pinned = desk;
    if (desk) {
      W.dist = Math.max(0, W.track.scrollWidth - window.innerWidth);
      wild.style.height = (vh + W.dist) + "px";
    } else {
      wild.style.height = ""; W.track.style.transform = ""; W.dist = 0;
    }
  }
  if (W) {
    watch(wild, "wild");
    setupWild();
    W.rail.addEventListener("scroll", function () {
      if (W.pinned) return;
      var m = W.rail.scrollWidth - W.rail.clientWidth;
      W.bar.style.width = (m > 0 ? W.rail.scrollLeft / m * 100 : 0) + "%";
    }, { passive: true });
  }
  function wildUpdate() {
    if (!W || !W.pinned || !visible.wild) return;
    var r = wild.getBoundingClientRect(), total = wild.offsetHeight - vh, p = clamp(-r.top / total);
    W.track.style.transform = "translate3d(" + (-p * W.dist).toFixed(1) + "px,0,0)";
    W.bar.style.width = (p * 100) + "%";
  }

  // ---- big marquee (speeds up while you scroll)
  var bm = document.querySelector("[data-bigmarquee]");
  var rows = bm ? Array.prototype.slice.call(bm.querySelectorAll("[data-bm]")) : [];
  var bmX = 0, lastY = window.scrollY, boost = 0;
  watch(bm, "bm");
  function bmUpdate() {
    var dy = Math.abs(window.scrollY - lastY);
    lastY = window.scrollY;
    boost += (Math.min(dy, 80) * 0.35 - boost) * 0.1;
    if (!bm || still || !visible.bm) return;
    bmX += 0.6 + boost;
    rows.forEach(function (row) {
      var w = row.firstElementChild.offsetWidth || 1, x = bmX % w;
      row.style.transform = "translate3d(" + (row.dataset.bm === "1" ? -x : x - w).toFixed(1) + "px,0,0)";
    });
  }

  // ---- desktop: cursor, 3D tilt, magnetic buttons
  var cur = null;
  if (fine && !still) {
    var dot = document.createElement("div"), ring = document.createElement("div");
    dot.className = "cursor-dot"; ring.className = "cursor-ring";
    document.body.appendChild(dot); document.body.appendChild(ring);
    cur = { mx: -100, my: -100, rx: -100, ry: -100, dot: dot, ring: ring };
    window.addEventListener("pointermove", function (e) {
      cur.mx = e.clientX; cur.my = e.clientY;
      root.classList.add("has-cursor");
      var t = e.target.closest && e.target.closest("a, button, summary, [role=button], input, select, textarea");
      ring.classList.toggle("is-link", !!t);
    }, { passive: true });
    document.addEventListener("mouseleave", function () { root.classList.remove("has-cursor"); });

    document.querySelectorAll(".card, .why-card, .dest, .feature, .wild-card").forEach(function (c) {
      c.classList.add("tilt");
      var g = document.createElement("span"); g.className = "tilt-glare"; c.appendChild(g);
      c.addEventListener("pointermove", function (e) {
        var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        c.style.transform = "perspective(900px) rotateX(" + ((0.5 - y) * 8).toFixed(2) + "deg) rotateY(" + ((x - 0.5) * 10).toFixed(2) + "deg) translateY(-6px)";
        c.style.setProperty("--gx", (x * 100) + "%"); c.style.setProperty("--gy", (y * 100) + "%");
      });
      c.addEventListener("pointerleave", function () { c.style.transform = ""; });
    });
    document.querySelectorAll(".btn, .card-go, .wa-float").forEach(function (b) {
      b.addEventListener("pointermove", function (e) {
        var r = b.getBoundingClientRect();
        b.style.transform = "translate(" + ((e.clientX - r.left - r.width / 2) * 0.2).toFixed(1) + "px," + ((e.clientY - r.top - r.height / 2) * 0.3).toFixed(1) + "px)";
      });
      b.addEventListener("pointerleave", function () { b.style.transform = ""; });
    });
  }
  function cursorUpdate() {
    if (!cur) return;
    cur.rx += (cur.mx - cur.rx) * 0.18; cur.ry += (cur.my - cur.ry) * 0.18;
    cur.dot.style.transform = "translate3d(" + cur.mx + "px," + cur.my + "px,0)";
    cur.ring.style.transform = "translate3d(" + cur.rx.toFixed(1) + "px," + cur.ry.toFixed(1) + "px,0)";
  }

  // ---- one loop for everything
  function loop() {
    heroUpdate(); summitUpdate(); wildUpdate(); bmUpdate(); cursorUpdate();
    requestAnimationFrame(loop);
  }
  window.addEventListener("resize", function () { vh = window.innerHeight; setupWild(); }, { passive: true });
  window.addEventListener("load", setupWild);
  requestAnimationFrame(loop);
})();
