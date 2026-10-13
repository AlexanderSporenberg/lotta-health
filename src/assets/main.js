// Lotta Health: small progressive enhancements. Nothing here sends data anywhere.
(function () {
  if (/[?&]review/.test(location.search)) document.documentElement.classList.add("review");
  "use strict";

  // Mobile navigation
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("hauptnav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("open", !open);
    });
  }

  // Reveal on scroll
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -60px 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  // Demo checkout: preselect the plan from the hash, mirror it in the summary, fake the payment.
  var co = document.querySelector("[data-checkout]");
  if (co) {
    var form = co.querySelector("form");
    var sync = function () {
      var r = form.querySelector("input[name=plan]:checked");
      co.querySelector("[data-sum-name]").textContent = r.dataset.name;
      co.querySelector("[data-sum-price]").textContent = r.dataset.price;
      co.querySelector("[data-sum-note]").textContent = r.dataset.note;
    };
    var pre = form.querySelector('input[value="' + location.hash.slice(1) + '"]');
    if (pre) pre.checked = true;
    sync();
    form.addEventListener("change", sync);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var btn = form.querySelector(".checkout-btn");
      btn.disabled = true;
      btn.textContent = "Wird verarbeitet …";
      setTimeout(function () {
        form.hidden = true;
        co.querySelector(".checkout-summary").hidden = true;
        var done = co.querySelector(".checkout-done");
        done.hidden = false;
        done.querySelector("h2").setAttribute("tabindex", "-1");
        done.querySelector("h2").focus();
      }, 900);
    });
  }

  // Demo shop: filter chips and an in-memory cart. Nothing is stored or sent.
  var shop = document.querySelector("[data-shop]");
  if (shop) {
    var cart = {};
    var euro = function (n) { return n.toFixed(2).replace(".", ",").replace(",00", "") + " €"; };
    var render = function () {
      var list = shop.querySelector("[data-cart-list]");
      var ids = Object.keys(cart);
      var sum = 0;
      list.innerHTML = ids.map(function (id) {
        var it = cart[id]; sum += it.price * it.qty;
        return '<li><span>' + it.qty + " × " + it.name + '</span><span>' + euro(it.price * it.qty) +
          '</span><button type="button" class="cart-x" data-remove="' + id + '" aria-label="' + it.name + ' entfernen">×</button></li>';
      }).join("");
      var ship = sum > 0 && sum < 50 ? 4.9 : 0;
      shop.querySelector("[data-cart-empty]").hidden = ids.length > 0;
      shop.querySelector("[data-cart-total]").hidden = !ids.length;
      shop.querySelector("[data-cart-ship]").hidden = !ids.length;
      shop.querySelector("[data-cart-sum]").textContent = euro(sum + ship) + (ship ? " inkl. Versand" : "");
      shop.querySelector("[data-cart-checkout]").disabled = !ids.length;
    };
    shop.addEventListener("click", function (e) {
      var add = e.target.closest("[data-add]");
      var rem = e.target.closest("[data-remove]");
      var f = e.target.closest("[data-filter]");
      if (add) {
        var id = add.dataset.add;
        cart[id] = cart[id] || { name: add.dataset.name, price: parseFloat(add.dataset.price), qty: 0 };
        cart[id].qty += 1;
        shop.querySelector("[data-cart-done]").hidden = true;
        add.textContent = "Hinzugefügt";
        setTimeout(function () { add.textContent = "In den Warenkorb"; }, 1200);
        render();
      } else if (rem) {
        delete cart[rem.dataset.remove];
        render();
      } else if (f) {
        shop.querySelectorAll("[data-filter]").forEach(function (b) { b.classList.toggle("on", b === f); b.setAttribute("aria-pressed", b === f); });
        shop.querySelectorAll(".product").forEach(function (p) { p.hidden = f.dataset.filter !== "alle" && p.dataset.cat !== f.dataset.filter; });
      } else if (e.target.closest("[data-cart-checkout]")) {
        cart = {};
        render();
        shop.querySelector("[data-cart-done]").hidden = false;
      }
    });
  }

  // Waitlist forms. TODO: connect to the newsletter tool once chosen.
  document.querySelectorAll("form[data-waitlist]").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var msg = form.querySelector(".form-msg");
      if (!form.checkValidity()) { form.reportValidity(); return; }
      form.querySelectorAll("input, button").forEach(function (el) { el.disabled = true; });
      if (msg) { msg.hidden = false; msg.textContent = "Danke. Wir melden uns bei dir, sobald Termine frei sind."; }
    });
  });

  // Symptom check ("Frag Lotte")
  var root = document.getElementById("check");
  if (root) symptomCheck(root);

  function symptomCheck(root) {
    var SCALE = [
      { v: 0, t: "Gar nicht" },
      { v: 1, t: "Ein bisschen" },
      { v: 2, t: "Deutlich" },
      { v: 3, t: "Sehr stark" },
    ];
    var AREAS = {
      koerper: "Körper",
      seele: "Stimmung und Kopf",
      intim: "Intimbereich und Blase",
    };
    var QUESTIONS = [
      { id: "zyklus", text: "Wie sieht dein Zyklus im Moment aus?", options: [
        { v: "regel", t: "Regelmäßig wie immer" },
        { v: "unregel", t: "Unregelmäßiger als früher" },
        { v: "pause", t: "Seit über 12 Monaten keine Periode mehr" },
        { v: "unklar", t: "Weiß ich nicht (z. B. wegen Spirale oder Pille)" },
      ] },
      { id: "hitze", area: "koerper", text: "Wie sehr belasten dich Hitzewellen oder nächtliches Schwitzen?" },
      { id: "schlaf", area: "koerper", text: "Wie sehr belastet dich schlechter oder unruhiger Schlaf?" },
      { id: "gelenke", area: "koerper", text: "Wie sehr belasten dich Gelenk- oder Muskelschmerzen?" },
      { id: "herz", area: "koerper", text: "Wie sehr belastet dich Herzklopfen oder Herzrasen ohne klaren Grund?" },
      { id: "stimmung", area: "seele", text: "Wie sehr belasten dich Stimmungstiefs oder Niedergeschlagenheit?" },
      { id: "gereizt", area: "seele", text: "Wie sehr belasten dich Gereiztheit oder innere Unruhe?" },
      { id: "kopf", area: "seele", text: "Wie sehr belasten dich Vergesslichkeit oder Konzentrationsprobleme?" },
      { id: "trocken", area: "intim", text: "Wie sehr belastet dich Trockenheit im Intimbereich?" },
      { id: "blase", area: "intim", text: "Wie sehr belasten dich häufiger Harndrang oder eine empfindliche Blase?" },
      { id: "lust", area: "intim", text: "Wie sehr belastet dich eine veränderte Lust auf Sex?" },
    ];

    var step = 0;
    var answers = {};
    var bar = root.querySelector(".progress span");
    var stage = root.querySelector("[data-stage]");

    render();

    function render() {
      if (step >= QUESTIONS.length) return renderResult();
      var q = QUESTIONS[step];
      var opts = q.options || SCALE;
      bar.style.width = Math.round((step / QUESTIONS.length) * 100) + "%";
      stage.innerHTML =
        '<p class="q-count">Frage ' + (step + 1) + " von " + QUESTIONS.length + "</p>" +
        '<h2 id="q-title" tabindex="-1">' + q.text + "</h2>" +
        '<div class="options" role="radiogroup" aria-labelledby="q-title">' +
        opts.map(function (o) {
          var checked = answers[q.id] === o.v ? " checked" : "";
          return '<label class="option"><input type="radio" name="' + q.id + '" value="' + o.v + '"' + checked + "> " + o.t + "</label>";
        }).join("") +
        "</div>" +
        '<div class="check-nav">' +
        '<button type="button" class="btn btn-ghost" data-back' + (step === 0 ? " disabled" : "") + ">Zurück</button>" +
        '<button type="button" class="btn" data-next' + (answers[q.id] === undefined ? " disabled" : "") + ">" +
        (step === QUESTIONS.length - 1 ? "Auswertung ansehen" : "Weiter") + "</button>" +
        "</div>";

      stage.querySelectorAll("input").forEach(function (input) {
        input.addEventListener("change", function () {
          answers[q.id] = q.options ? input.value : Number(input.value);
          stage.querySelector("[data-next]").disabled = false;
        });
      });
      stage.querySelector("[data-back]").addEventListener("click", function () { step--; render(); });
      stage.querySelector("[data-next]").addEventListener("click", function () { step++; render(); });
      var title = stage.querySelector("#q-title");
      if (step > 0) title.focus();
    }

    function renderResult() {
      bar.style.width = "100%";
      var sums = {}, max = {};
      QUESTIONS.forEach(function (q) {
        if (!q.area) return;
        sums[q.area] = (sums[q.area] || 0) + answers[q.id];
        max[q.area] = (max[q.area] || 0) + 3;
      });
      var total = 0, totalMax = 0;
      var bars = Object.keys(AREAS).map(function (a) {
        total += sums[a]; totalMax += max[a];
        var pct = Math.round((sums[a] / max[a]) * 100);
        var cls = pct >= 60 ? "high" : pct >= 30 ? "mid" : "";
        var word = pct >= 60 ? "stark" : pct >= 30 ? "spürbar" : "gering";
        return '<div class="result-bar"><label><span>' + AREAS[a] + "</span><span>" + word + "</span></label>" +
          '<div class="track"><div class="fill ' + cls + '" style="width:' + Math.max(pct, 4) + '%"></div></div></div>';
      }).join("");

      var share = total / totalMax;
      var headline, text;
      if (share >= 0.5) {
        headline = "Deine Beschwerden belasten dich deutlich.";
        text = "Das musst du nicht aushalten. Lass deine Beschwerden ärztlich einordnen, bei deiner Gynäkologin oder in einer Lotta Navigation Session. Speichere dir diese Auswertung und nimm sie mit.";
      } else if (share >= 0.2) {
        headline = "Du spürst einige typische Veränderungen.";
        text = "Viele Frauen erleben genau das. Mit guter ärztlicher Einordnung, Schlaf, Training und den passenden Routinen lässt sich oft viel bewegen. In der Navigation Session finden wir heraus, wo du ansetzt.";
      } else {
        headline = "Im Moment belastet dich wenig.";
        text = "Schön. Wenn sich etwas verändert, mach den Check einfach noch einmal. Wissen vorab hilft, Veränderungen früh einzuordnen.";
      }
      var cycleNote = {
        regel: "Auch mit regelmäßigem Zyklus können erste Veränderungen der Perimenopause auftreten.",
        unregel: "Ein unregelmäßiger Zyklus ist oft eines der ersten Zeichen der Perimenopause.",
        pause: "Nach 12 Monaten ohne Periode spricht man von der Postmenopause. Beschwerden können trotzdem weiter bestehen.",
        unklar: "Wenn Verhütung deinen Zyklus überdeckt, hilft ein Gespräch in der Praxis bei der Einordnung.",
      }[answers.zyklus];

      root.querySelector("[data-stage]").innerHTML =
        '<p class="eyebrow">Deine Auswertung</p>' +
        '<h2 id="q-title" tabindex="-1">' + headline + "</h2>" +
        "<p>" + text + "</p>" +
        '<div class="result-bars">' + bars + "</div>" +
        "<p>" + cycleNote + "</p>" +
        (sums.seele / max.seele >= 0.6 ? '<p><strong>Wenn du Gedanken hast, nicht mehr leben zu wollen:</strong> Bitte hol dir sofort Hilfe, über die 112 oder die Telefonseelsorge 0800 111 0 111 (kostenfrei, rund um die Uhr).</p>' : "") +
        '<p class="muted">Stand: ' + new Date().toLocaleDateString("de-DE") + "</p>" +
        '<p class="note">Dieser Check ist eine Orientierung und keine Diagnose. Deine Antworten bleiben in deinem Browser und werden nicht gespeichert oder übertragen. Bei starken, neuen oder ungewöhnlichen Beschwerden (zum Beispiel Blutungen nach der Menopause) geh bitte zeitnah in eine Praxis.</p>' +
        '<div class="btn-row"><a class="btn" href="checkout.html#navigation">Navigation Session buchen</a><a class="btn btn-ghost" href="ablauf.html#navigation-session">So geht es weiter</a>' +
        '<button type="button" class="btn btn-ghost" data-print>Drucken oder als PDF speichern</button>' +
        '<button type="button" class="btn btn-ghost" data-restart>Check neu starten</button></div>';
      root.scrollIntoView({ block: "start" });
      root.querySelector("#q-title").focus({ preventScroll: true });
      root.querySelector("[data-print]").addEventListener("click", function () { window.print(); });
      root.querySelector("[data-restart]").addEventListener("click", function () {
        step = 0; answers = {}; render();
      });
    }
  }
})();

// App section: feature tabs switch the phone screen, with a gentle auto-rotate.
(function () {
  var list = document.querySelector("[data-app-tabs]");
  if (!list) return;
  var btns = list.querySelectorAll(".feat");
  var screens = document.querySelectorAll(".app-stage .screen");
  var current = 0, timer = null;
  function show(i) {
    current = i;
    btns.forEach(function (b, j) { b.classList.toggle("on", j === i); b.setAttribute("aria-pressed", j === i ? "true" : "false"); });
    screens.forEach(function (s, j) { s.classList.toggle("on", j === i); });
  }
  btns.forEach(function (b, i) { b.addEventListener("click", function () { clearInterval(timer); show(i); }); });
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    timer = setInterval(function () { show((current + 1) % btns.length); }, 4500);
  }
})();
