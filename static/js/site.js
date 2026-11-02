(function () {
  "use strict";

  // ---- mobile menu
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-nav]");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  // ---- booking forms -> WhatsApp message
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

  // ---- gallery filters + lightbox
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
    img.src = pic.currentSrc || pic.src;
    img.alt = pic.alt;
    cap.textContent = pic.alt;
    current = visible().indexOf(fig);
  }
  function step(d) {
    var list = visible();
    if (!list.length) return;
    current = (current + d + list.length) % list.length;
    show(list[current]);
  }

  gallery.addEventListener("click", function (e) {
    var btn = e.target.closest("button[data-open]");
    if (!btn) return;
    show(btn.closest("figure"));
    box.showModal();
  });
  box.querySelector("[data-lb-close]").addEventListener("click", function () { box.close(); });
  box.querySelector("[data-lb-prev]").addEventListener("click", function () { step(-1); });
  box.querySelector("[data-lb-next]").addEventListener("click", function () { step(1); });
  box.addEventListener("click", function (e) { if (e.target === box) box.close(); });
  box.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") step(-1);
    if (e.key === "ArrowRight") step(1);
  });
  var startX = null;
  box.addEventListener("touchstart", function (e) { startX = e.touches[0].clientX; }, { passive: true });
  box.addEventListener("touchend", function (e) {
    if (startX === null) return;
    var dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1);
    startX = null;
  });
})();
