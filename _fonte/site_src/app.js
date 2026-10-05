(function () {
  "use strict";
  var norm = function (s) {
    return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  };

  /* ---------- índice: busca + filtros ---------- */
  var q = document.getElementById("q");
  var grid = document.getElementById("grid");
  if (q && grid && window.__INDEX__) {
    var idx = window.__INDEX__.map(function (r) { r.xn = norm(r.x); r.tn = norm(r.t + " " + r.f); return r; });
    var cards = {};
    Array.prototype.forEach.call(grid.querySelectorAll(".card"), function (c) { cards[c.getAttribute("data-num")] = c; });
    var chips = document.querySelectorAll(".chip");
    var empty = document.getElementById("empty");
    var count = document.getElementById("count");
    var cat = "all";

    function apply() {
      var terms = norm(q.value).split(/\s+/).filter(Boolean);
      var shown = 0;
      var scored = idx.map(function (r) {
        var ok = (cat === "all") || r.c.indexOf(cat) >= 0;
        var score = 0;
        if (ok && terms.length) {
          for (var i = 0; i < terms.length; i++) {
            var t = terms[i];
            if (r.tn.indexOf(t) >= 0) score += 10;
            else if (r.xn.indexOf(t) >= 0) score += 1;
            else { ok = false; break; }
          }
        }
        return { r: r, ok: ok, score: score };
      });
      if (terms.length) scored.sort(function (a, b) { return b.score - a.score; });
      scored.forEach(function (s, i) {
        var el = cards[s.r.n];
        if (!el) return;
        el.hidden = !s.ok;
        el.style.order = i;
        if (s.ok) shown++;
      });
      if (empty) empty.hidden = shown > 0;
      if (count) count.textContent = shown;
      try { sessionStorage.setItem("ps_q", q.value); } catch (e) {}
    }
    q.addEventListener("input", apply);
    Array.prototype.forEach.call(chips, function (ch) {
      ch.addEventListener("click", function () {
        Array.prototype.forEach.call(chips, function (o) { o.classList.remove("is-on"); });
        ch.classList.add("is-on");
        cat = ch.getAttribute("data-cat");
        apply();
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && document.activeElement !== q) { e.preventDefault(); q.focus(); q.select(); }
      if (e.key === "Escape" && document.activeElement === q) { q.value = ""; apply(); }
    });
    try { var saved = sessionStorage.getItem("ps_q"); if (saved) { q.value = saved; } } catch (e) {}
    apply();
  }

  /* ---------- página do protocolo: modo resumo / completo ---------- */
  var seg = document.querySelector(".seg");
  if (seg) {
    var tabs = seg.querySelectorAll("button[data-mode]");
    var panels = { resumo: document.getElementById("resumo"), completo: document.getElementById("completo") };
    function setMode(m, push) {
      if (!panels[m]) m = "resumo";
      Array.prototype.forEach.call(tabs, function (t) {
        var on = t.getAttribute("data-mode") === m;
        t.setAttribute("aria-selected", on ? "true" : "false");
      });
      panels.resumo.hidden = m !== "resumo";
      panels.completo.hidden = m !== "completo";
      try { localStorage.setItem("ps_mode", m); } catch (e) {}
      if (push) { history.replaceState(null, "", "#" + m); }
    }
    Array.prototype.forEach.call(tabs, function (t) {
      t.addEventListener("click", function () { setMode(t.getAttribute("data-mode"), true); window.scrollTo({ top: 0, behavior: "smooth" }); });
    });
    var h = (location.hash || "").replace("#", "");
    var initial = "resumo";
    if (h === "completo" || h === "resumo") initial = h;
    else if (h && document.getElementById(h) && panels.completo.contains(document.getElementById(h))) initial = "completo";
    else { try { var pref = localStorage.getItem("ps_mode"); if (pref === "completo") initial = "completo"; } catch (e) {} }
    setMode(initial, false);
    if (h && h !== "resumo" && h !== "completo") {
      var target = document.getElementById(h);
      if (target) setTimeout(function () { target.scrollIntoView(); }, 50);
    }
    var tocD = document.querySelector(".toc-in");
    if (tocD && window.innerWidth < 860) tocD.removeAttribute("open");
    // links do sumário mantêm o modo completo
    var toc = document.querySelector(".toc");
    if (toc) toc.addEventListener("click", function (e) {
      var a = e.target.closest("a"); if (!a) return;
      setMode("completo", false);
    });
    window.addEventListener("hashchange", function () {
      var hh = (location.hash || "").replace("#", "");
      if (hh === "completo" || hh === "resumo") setMode(hh, false);
    });
  }
})();
