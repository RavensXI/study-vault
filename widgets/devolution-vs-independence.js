/* devolution-vs-independence -- who holds the legal power to decide? */
(function () {
  "use strict";

  var BODY = {
    wm: { name: "UK Parliament (Westminster)", short: "Westminster", tier: "res", nation: "the whole UK" },
    sp: { name: "Scottish Parliament", short: "the Scottish Parliament", tier: "dev", nation: "Scotland" },
    sc: { name: "Senedd Cymru (Welsh Parliament)", short: "the Senedd", tier: "dev", nation: "Wales" },
    ni: { name: "Northern Ireland Assembly", short: "the NI Assembly", tier: "dev", nation: "Northern Ireland" }
  };

  var ROUNDS = [
    /* ---- plainly devolved ---- */
    {
      cat: "dev", place: "Scotland", ans: "sp",
      area: "The subjects taught in state schools, and the qualifications pupils sit.",
      right: "Education is <strong>devolved</strong>. Scotland sets its own curriculum and its own qualifications, so Westminster has no say in what a Glasgow school teaches.",
      alt: "Education was transferred in 1999 and is <strong>devolved</strong>. Westminster does not set the curriculum in Scotland, which is why Scottish pupils sit different exams."
    },
    {
      cat: "dev", place: "Wales", ans: "sc",
      area: "Running the NHS in Wales — its hospitals, staff and waiting lists.",
      right: "Health is <strong>devolved</strong>. NHS Wales answers to the Senedd, not to Westminster, which is why waiting lists and prescription charges can differ from England’s.",
      alt: "Health is <strong>devolved</strong>. NHS Wales is directed from Cardiff and answers to the Senedd; Westminster does not run Welsh hospitals."
    },
    {
      cat: "dev", place: "Wales", ans: "sc",
      area: "Requiring road signs to show Welsh as well as English.",
      right: "The Welsh language is <strong>devolved</strong>. Welsh language duties are set by law made in Cardiff, so a bilingual sign is a Senedd matter, not a Westminster one.",
      alt: "The Welsh language is <strong>devolved</strong>. Bilingual signs come from Welsh law; Westminster does not decide what a road sign in Wales says."
    },
    {
      cat: "dev", place: "Northern Ireland", ans: "ni",
      area: "Running schools and hospitals in Northern Ireland.",
      right: "Health and education are <strong>devolved</strong> to the Assembly. Northern Ireland runs its own integrated health and social care system, decided at Stormont.",
      alt: "Health and education were transferred to the Assembly. Westminster does not run Northern Ireland’s schools or hospitals while the Assembly is sitting."
    },
    {
      cat: "dev", place: "Scotland", ans: "sp",
      area: "How the courts work and the sentences judges can pass.",
      right: "Justice is <strong>devolved</strong>, and Scotland kept its own legal system in 1707. Its courts, prosecutors and sentencing rules are all set in Edinburgh.",
      alt: "Justice is <strong>devolved</strong> in Scotland, which has had a separate legal system since 1707. Westminster does not set Scottish sentencing."
    },

    /* ---- plainly reserved ---- */
    {
      cat: "res", place: "Scotland", ans: "wm",
      area: "Deciding who may come from abroad to live and work in Scotland.",
      right: "Immigration is <strong>reserved</strong>. It was never transferred, so who may enter the UK is decided at Westminster for the whole country, Scotland included.",
      alt: "Immigration is <strong>reserved</strong> — it was never on the transferred list. Devolution hands over a named set of powers, not everything inside a nation’s borders."
    },
    {
      cat: "res", place: "Wales", ans: "wm",
      area: "Agreeing a trade deal with another country.",
      right: "Foreign affairs and trade are <strong>reserved</strong>. Treaties are made by the UK government for the whole UK; no devolved body signs its own.",
      alt: "Foreign affairs are <strong>reserved</strong>. Signing your own treaties is what an independent state does; the Senedd holds transferred domestic powers only."
    },
    {
      cat: "res", place: "The whole UK", ans: "wm",
      area: "The size of the armed forces and where they are sent.",
      right: "Defence is <strong>reserved</strong>. The armed forces are UK-wide and answer to the UK government; no devolved body has a say in a deployment.",
      alt: "Defence is <strong>reserved</strong> and was never transferred. A devolved nation has no army of its own — one of the clearest lines between devolution and independence."
    },
    {
      cat: "res", place: "The whole UK", ans: "wm",
      area: "Which currency the UK uses.",
      right: "Currency is <strong>reserved</strong>. The pound is a UK-wide matter settled at Westminster, so no devolved body can create money of its own.",
      alt: "Currency is <strong>reserved</strong>. Devolution transferred domestic services, not the money supply; running your own currency is a mark of independence."
    },
    {
      cat: "res", place: "Northern Ireland", ans: "wm",
      area: "Issuing passports and deciding who counts as a British citizen.",
      right: "Nationality is <strong>reserved</strong>. Citizenship and passports are settled at Westminster for everyone in the UK, not at Stormont.",
      alt: "Nationality is <strong>reserved</strong>. The Assembly runs Northern Ireland’s public services; it does not decide who is a citizen or issue passports."
    },

    /* ---- the lists are not the same (asymmetry) ---- */
    {
      cat: "asym", place: "Wales", ans: "wm",
      area: "Running the police service and deciding how policing is organised.",
      right: "Policing is <strong>reserved</strong> in Wales. The three lists are not the same: Scotland and Northern Ireland run their own policing, and Wales does not.",
      alt: "Policing is <strong>reserved</strong> in Wales — the one most people get wrong. Scotland and Northern Ireland run their own; the three lists are not identical."
    },
    {
      cat: "asym", place: "Scotland", ans: "sp",
      area: "Setting the rates and bands of income tax on people’s earnings.",
      right: "Rates and bands are <strong>devolved</strong> to Scotland, so a Scottish taxpayer can pay a different rate. The Senedd may vary rates only; the Assembly has no income tax power at all.",
      alt: "Rates and bands of income tax on earnings were transferred to Scotland in 2017. Wales got a narrower version and Northern Ireland got none, so the three lists differ."
    },
    {
      cat: "asym", place: "Northern Ireland", ans: "wm",
      area: "Setting the rates and bands of income tax on people’s earnings.",
      right: "Income tax is <strong>reserved</strong> in Northern Ireland; the Assembly has no power over it. Scotland’s Parliament does set its own rates and bands, so the lists are not the same.",
      alt: "The Assembly has no income tax power — it is <strong>reserved</strong> here. Scotland’s Parliament does set its own rates and bands, so you cannot assume all three match."
    },

    /* ---- Westminster stays sovereign ---- */
    {
      cat: "sov", place: "The whole UK", ans: "wm",
      area: "Changing what powers the Senedd holds — adding to them or removing them.",
      right: "Devolution was created by Acts of the <strong>UK Parliament</strong>, and only it can change them. The powers are granted, not owned, which is why devolution is not independence.",
      alt: "The Senedd cannot rewrite its own powers. Devolution came from Acts of the <strong>UK Parliament</strong>, so only Westminster can add to the list or take from it."
    },
    {
      cat: "sov", place: "Scotland", ans: "wm",
      area: "Passing a law on a devolved matter when the Scottish Parliament has refused its consent.",
      right: "Legally Westminster still can. Under the <strong>Sewel convention</strong> it does not normally legislate on devolved matters without consent, but a convention is an agreed habit, not a law.",
      alt: "The Scottish Parliament cannot block it. Sewel is a <strong>convention</strong> — an agreed habit, not a law — so the legal power to legislate stays with the UK Parliament."
    },
    {
      cat: "sov", place: "Scotland", ans: "wm",
      area: "Holding a legally binding referendum on whether Scotland stays in the UK.",
      right: "The constitution and the Union are <strong>reserved</strong>. In 2022 the Supreme Court confirmed the Scottish Parliament cannot arrange one alone; the 2014 vote needed Westminster’s agreement.",
      alt: "This was never transferred: the Union and the constitution are <strong>reserved</strong>. The 2014 vote went ahead only because the UK Parliament granted the power for it."
    }
  ];

  var MASTERY = "Powers come as a named list that differs by nation. Everything else — defence, foreign affairs, immigration, currency — stays with Westminster, which can still change it.";

  var OPENER = "Devolution transferred a named list of powers. Anything not on the list stayed with the UK Parliament.";

  var CSS =
  ".svw-dvi{font-family:Inter,system-ui,-apple-system,'Segoe UI',sans-serif;color:#2d2a26;line-height:1.45;}" +
  ".svw-dvi *{box-sizing:border-box;}" +
  ".svw-dvi .dvi-kicker{margin:0 0 .12rem;font-size:.66rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase;color:var(--dvi-accent);}" +
  ".svw-dvi .dvi-title{margin:0 0 .22rem;font-family:'Source Serif 4',Georgia,serif;font-weight:600;font-size:1.22rem;line-height:1.2;}" +
  ".svw-dvi .dvi-frame{margin:0 0 .48rem;font-size:.85rem;color:#5b564e;}" +
  ".svw-dvi .dvi-stage{background:#faf8f5;border:1px solid #e8e2d9;border-radius:12px;padding:.55rem .6rem .6rem;}" +
  ".svw-dvi .dvi-case{background:#fff;border:1px solid #e0d9cd;border-radius:10px;padding:.4rem .55rem .45rem;margin-bottom:.48rem;}" +
  ".svw-dvi .dvi-badges{display:flex;flex-wrap:wrap;gap:.3rem;margin-bottom:.18rem;}" +
  ".svw-dvi .dvi-badge{font-size:.62rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;border-radius:999px;padding:.13rem .45rem;color:var(--dvi-accent);background:var(--dvi-tint);}" +
  ".svw-dvi .dvi-badge--tier{color:#4f7d63;background:#eef3ef;}" +
  ".svw-dvi .dvi-area{display:block;font-size:.88rem;font-weight:600;line-height:1.3;}" +
  ".svw-dvi .dvi-band{margin:.38rem 0 .2rem;font-size:.63rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:#8d8880;}" +
  ".svw-dvi .dvi-band--first{margin-top:0;}" +
  ".svw-dvi .dvi-row{display:flex;align-items:center;gap:.4rem;width:100%;text-align:left;font-family:inherit;font-size:.82rem;font-weight:600;background:#fff;border:1px solid #ddd7cd;border-radius:10px;padding:.36rem .55rem;margin:0 0 .26rem;color:#2d2a26;cursor:pointer;}" +
  ".svw-dvi .dvi-row:last-child{margin-bottom:0;}" +
  ".svw-dvi .dvi-nm{flex:1 1 auto;}" +
  ".svw-dvi .dvi-tag{flex:0 0 auto;font-size:.62rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#8d8880;white-space:nowrap;}" +
  ".svw-dvi .dvi-row[aria-pressed='true']{background:#2d2a26;border-color:#2d2a26;color:#fff;}" +
  ".svw-dvi .dvi-row.is-right{background:#eef3ef;border-color:#4f7d63;}" +
  ".svw-dvi .dvi-row.is-right .dvi-tag{color:#4f7d63;}" +
  ".svw-dvi .dvi-row.is-picked{border-style:dashed;border-color:#b6ada0;color:#5b564e;}" +
  ".svw-dvi .dvi-row[disabled]{cursor:default;}" +
  ".svw-dvi .dvi-streak{min-height:.98rem;margin:.42rem 0 0;font-size:.77rem;font-weight:600;color:#8d8880;}" +
  ".svw-dvi .dvi-actions{margin:.28rem 0 .4rem;}" +
  ".svw-dvi .dvi-check{font-family:inherit;font-size:.82rem;font-weight:600;padding:.46rem .95rem;border-radius:10px;border:1px solid #ddd7cd;background:#faf8f5;color:#2d2a26;cursor:pointer;}" +
  ".svw-dvi .dvi-check.is-armed{background:#2d2a26;border-color:#2d2a26;color:#fff;}" +
  ".svw-dvi .dvi-caption{margin:0;font-size:.84rem;line-height:1.5;color:#3d3931;min-height:4.1rem;}" +
  ".svw-dvi .dvi-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;}" +
  ".svw-dvi .dvi-row:focus-visible,.svw-dvi .dvi-check:focus-visible{outline:2px solid var(--dvi-accent);outline-offset:2px;}" +
  ".svw-dvi.dvi-motion .dvi-row,.svw-dvi.dvi-motion .dvi-check{transition:background-color .16s ease,border-color .16s ease,color .16s ease;}";

  var KEYS = ["wm", "sp", "sc", "ni"];

  function shuffle(list) {
    var out = list.slice(), i, j, t;
    for (i = out.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1));
      t = out[i]; out[i] = out[j]; out[j] = t;
    }
    return out;
  }

  window.SVWidget = {
    meta: {
      id: "devolution-vs-independence",
      title: "Devolution: who decides?",
      teaches: "Devolution transfers a named, unequal list of powers to the Scottish Parliament, the Senedd and the Northern Ireland Assembly; reserved matters and legal sovereignty stay with the UK Parliament."
    },

    mount: function (root, ctx) {
      ctx = ctx || {};
      var accent = ctx.accent ||
        (getComputedStyle(root).getPropertyValue("--accent") || "").trim() || "#8a6d3b";
      var reduced = !!ctx.reducedMotion;

      root.className = (root.className ? root.className + " " : "") + "svw-dvi" + (reduced ? "" : " dvi-motion");
      root.style.setProperty("--dvi-accent", accent);
      root.style.setProperty("--dvi-tint", accent + "1f");

      var style = document.createElement("style");
      style.textContent = CSS;
      root.appendChild(style);

      /* ---------- build the DOM once ---------- */
      var html =
        '<p class="dvi-kicker">Devolution</p>' +
        '<h3 class="dvi-title">Who decides?</h3>' +
        '<p class="dvi-frame">For each decision below, say which body holds the legal power to make it.</p>' +
        '<div class="dvi-stage">' +
          '<div class="dvi-case">' +
            '<span class="dvi-badges"><span class="dvi-badge" data-el="place"></span>' +
            '<span class="dvi-badge dvi-badge--tier" data-el="tier" hidden></span></span>' +
            '<span class="dvi-area" data-el="area"></span>' +
          '</div>' +
          '<p class="dvi-band dvi-band--first">Reserved — kept by the UK Parliament</p>' +
          '<div data-el="resrows"></div>' +
          '<p class="dvi-band">Devolved — transferred to a nation’s own body</p>' +
          '<div data-el="devrows"></div>' +
        '</div>' +
        '<p class="dvi-streak" data-el="streak"></p>' +
        '<div class="dvi-actions"><button type="button" class="dvi-check" data-el="check">Check</button></div>' +
        '<p class="dvi-caption" data-el="caption" role="status" aria-live="polite"></p>' +
        '<p class="dvi-sr" data-el="sr" aria-live="polite"></p>';
      var holder = document.createElement("div");
      holder.innerHTML = html;
      while (holder.firstChild) root.appendChild(holder.firstChild);

      var el = {};
      Array.prototype.forEach.call(root.querySelectorAll("[data-el]"), function (n) {
        el[n.getAttribute("data-el")] = n;
      });

      var rowFor = {};
      KEYS.forEach(function (key) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "dvi-row";
        b.setAttribute("aria-pressed", "false");
        b.setAttribute("data-body", key);
        b.innerHTML = '<span class="dvi-nm"></span><span class="dvi-tag"></span>';
        b.querySelector(".dvi-nm").textContent = BODY[key].name;
        (key === "wm" ? el.resrows : el.devrows).appendChild(b);
        rowFor[key] = b;
        b.addEventListener("click", function () { pickBody(key); });
      });

      /* ---------- round queue: devolved, reserved, asymmetry, sovereignty ---------- */
      var buckets = { dev: [], res: [], asym: [], sov: [] };
      ROUNDS.forEach(function (r) { buckets[r.cat].push(r); });
      var pools = {
        dev: shuffle(buckets.dev), res: shuffle(buckets.res),
        asym: shuffle(buckets.asym), sov: shuffle(buckets.sov)
      };
      var cycle = ["dev", "res", "asym", "sov"];
      var cursor = 0;

      function drawRound() {
        var cat = cycle[cursor % cycle.length];
        cursor++;
        if (!pools[cat].length) pools[cat] = shuffle(buckets[cat]);
        return pools[cat].shift();
      }

      /* ---------- state ---------- */
      var round = null, pick = null, phase = "ask";
      var streak = 0, attempted = 0, mastered = false, lastCorrect = null;

      function publish() {
        root.dataset.svState = JSON.stringify({
          streak: streak, mastered: mastered, attempted: attempted,
          lastCorrect: lastCorrect, picked: pick
        });
      }

      function clearRows() {
        KEYS.forEach(function (k) {
          var b = rowFor[k];
          b.classList.remove("is-right");
          b.classList.remove("is-picked");
          b.setAttribute("aria-pressed", "false");
          b.disabled = false;
          b.querySelector(".dvi-tag").textContent = "";
        });
      }

      function armCheck() {
        el.check.textContent = phase === "shown"
          ? (mastered ? "Another anyway" : "Next decision")
          : "Check";
        var armed = phase === "shown" || pick !== null;
        if (armed) el.check.classList.add("is-armed");
        else el.check.classList.remove("is-armed");
      }

      function setStreakLine() {
        var t = "";
        if (mastered) t = "You have it — keep going if you like.";
        else if (streak === 1) t = "1 right in a row — two more and you have it.";
        else if (streak === 2) t = "2 right in a row — one more and you have it.";
        else if (attempted > 0) t = "Back to nought — three in a row finishes it.";
        el.streak.textContent = t;
      }

      function newRound() {
        round = drawRound();
        pick = null;
        phase = "ask";
        clearRows();
        el.place.textContent = round.place;
        el.tier.hidden = true;
        el.area.textContent = round.area;
        armCheck();
        setStreakLine();
        el.sr.textContent = "New decision, " + round.place + ". " + round.area;
      }

      function pickBody(key) {
        if (phase === "shown") return;
        pick = key;
        KEYS.forEach(function (k) {
          rowFor[k].setAttribute("aria-pressed", k === key ? "true" : "false");
        });
        armCheck();
        publish();
        el.sr.textContent = BODY[key].name + " chosen. Not checked yet.";
      }

      function explain(correct, pickKey, ansKey) {
        if (correct) {
          return mastered
            ? "Three in a row — you have it. " + MASTERY
            : round.right;
        }
        if (BODY[pickKey].tier === "dev" && BODY[ansKey].tier === "dev") {
          return "You had the right level — this is <strong>devolved</strong> — but the decision is being made in " +
                 BODY[ansKey].nation + ", and each body decides only for its own nation.";
        }
        return round.alt;
      }

      function commit() {
        if (phase === "shown") {
          newRound();
          el.caption.innerHTML = OPENER;
          el.check.focus();
          return;
        }
        if (pick === null) {
          el.caption.innerHTML = "Nothing is committed yet — choose the body you think holds the power.";
          el.sr.textContent = "No body chosen yet.";
          return;
        }

        var correct = pick === round.ans;
        attempted++;
        lastCorrect = correct;
        if (correct) {
          streak++;
          if (streak >= 3) mastered = true;
        } else {
          streak = 0;
        }

        phase = "shown";
        KEYS.forEach(function (k) {
          rowFor[k].setAttribute("aria-pressed", "false");
          rowFor[k].disabled = true;
        });
        rowFor[round.ans].classList.add("is-right");
        rowFor[round.ans].querySelector(".dvi-tag").textContent = correct ? "your answer" : "decides this";
        if (!correct) {
          rowFor[pick].classList.add("is-picked");
          rowFor[pick].querySelector(".dvi-tag").textContent = "you chose";
        }

        el.tier.hidden = false;
        el.tier.textContent = BODY[round.ans].tier === "res" ? "Reserved" : "Devolved";

        var lead = correct
          ? (mastered
              ? "<strong>Right</strong> — you said " + BODY[pick].short + ". "
              : "<strong>Right</strong> — you said " + BODY[pick].short + ", and it does decide this. ")
          : "<strong>Not quite</strong> — you said " + BODY[pick].short + ", but " + BODY[round.ans].short + " decides this. ";
        el.caption.innerHTML = lead + explain(correct, pick, round.ans);
        el.sr.textContent = (correct ? "Correct. " : "Wrong. ") + BODY[round.ans].name + " decides this.";

        setStreakLine();
        armCheck();
        publish();
      }

      el.check.addEventListener("click", commit);

      newRound();
      el.caption.innerHTML = OPENER;
      publish();
    }
  };
})();
