"""Build the shareable (hosted) version of the grading page.

    python grading_hosted.py runs/2026-10-03_phase0/baseline_50.jsonl --out <file>.html

Same content as grading_view.py, for publishing as a claude.ai Artifact so a
teammate can grade from a link. Differences from the local page:

- Each grader's verdicts are saved to the artifact's store under their own
  private document (`grades/<their id>`): graders cannot see each other's work,
  and the artifact owner (and Claude, acting for the owner) can read them all.
- Exports go through the viewer's download confirmation; where that is
  unavailable the page shows the CSV to copy.
- When online saving is unavailable the page keeps grades in the browser and
  says so.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

import config
from grading_view import build

PAGE = r"""<title>TechStore Grading Desk</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=JetBrains+Mono:wght@400;600&family=Newsreader:opsz,wght@6..72,400;6..72,600&display=swap">
<style>
/* Layout: a marking desk. Sticky tally bar on top; each question is one sheet,
   the model's answer on the left facing the evidence it was given on the right. */
:root {
  --paper: #eef2f5; --sheet: #ffffff; --ink: #18212b; --ink-2: #566472; --rule: #d6dee5;
  --pen: #1f4fa3; --pen-wash: #e3ebf8;
  --ok: #1d6b3a; --ok-wash: #e2f1e7; --warn: #8a5300; --warn-wash: #fbefd9;
  --bad: #a3271f; --bad-wash: #f9e2e0; --miss: #fbeceb;
  --f-read: "Newsreader", Georgia, "Times New Roman", serif;
  --f-ui: "Atkinson Hyperlegible", -apple-system, "Segoe UI", sans-serif;
  --f-mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --paper: #10151b; --sheet: #182029; --ink: #e4e9ee; --ink-2: #9aa8b5; --rule: #2a3440;
  --pen: #8db1ff; --pen-wash: #1c2a44; --ok: #7fd49a; --ok-wash: #16301f; --warn: #f2bd6b; --warn-wash: #36290f;
  --bad: #ff9a91; --bad-wash: #3a1d1b; --miss: #2c1b1c; color-scheme: dark } }
:root[data-theme="dark"] {
  --paper: #10151b; --sheet: #182029; --ink: #e4e9ee; --ink-2: #9aa8b5; --rule: #2a3440;
  --pen: #8db1ff; --pen-wash: #1c2a44; --ok: #7fd49a; --ok-wash: #16301f; --warn: #f2bd6b; --warn-wash: #36290f;
  --bad: #ff9a91; --bad-wash: #3a1d1b; --miss: #2c1b1c; color-scheme: dark }
body { background: var(--paper); color: var(--ink); font: 15px/1.55 var(--f-ui); }
.bar { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: var(--sheet);
  border-bottom: 1px solid var(--rule); padding: 10px 16px; display: flex; flex-wrap: wrap; gap: 8px 16px; align-items: center; }
.bar h1 { font: 600 19px/1.2 var(--f-read); margin: 0; text-wrap: balance; }
.who { color: var(--ink-2); font-size: 13px; }
.tally { font-variant-numeric: tabular-nums; font-size: 13px; color: var(--ink-2); display: flex; gap: 10px; align-items: center; }
.meter { width: 120px; height: 6px; border-radius: 99px; background: var(--rule); overflow: hidden; }
.meter i { display: block; height: 100%; background: var(--pen); width: 0; transition: width .2s; }
.save { font-size: 12px; padding: 2px 8px; border-radius: 99px; background: var(--pen-wash); color: var(--pen); }
.save.local { background: var(--warn-wash); color: var(--warn); }
.spacer { flex: 1 1 auto; }
button, select { font: inherit; font-size: 14px; color: var(--ink); background: var(--sheet); border: 1px solid var(--rule);
  border-radius: 8px; padding: 6px 12px; cursor: pointer; }
button:focus-visible, select:focus-visible, textarea:focus-visible { outline: 2px solid var(--pen); outline-offset: 2px; }
button.go { background: var(--pen); border-color: var(--pen); color: var(--sheet); }
.wrap { max-width: 1200px; margin: 0 auto; padding: 16px; display: flex; flex-direction: column; gap: 18px; }
.brief { background: var(--sheet); border: 1px solid var(--rule); border-radius: 10px; padding: 14px 16px; color: var(--ink-2); }
.brief p { margin: 0 0 6px; max-width: 75ch; } .brief p:last-child { margin: 0; } .brief b { color: var(--ink); }
.scale { display: flex; flex-wrap: wrap; gap: 6px 14px; margin-top: 6px; font-size: 13px; }
.scale span b { font-family: var(--f-mono); font-weight: 600; }
#copybox { background: var(--sheet); border: 1px solid var(--warn); border-radius: 10px; padding: 12px 16px; }
#copybox textarea { width: 100%; height: 160px; font: 12px/1.4 var(--f-mono); background: var(--paper); color: var(--ink);
  border: 1px solid var(--rule); border-radius: 6px; padding: 8px; }
.sheet { background: var(--sheet); border: 1px solid var(--rule); border-radius: 10px; overflow: hidden; }
.sheet.graded { border-color: var(--pen); }
.head { padding: 12px 16px; border-bottom: 1px solid var(--rule); display: flex; flex-wrap: wrap; gap: 6px 10px; align-items: baseline; }
.qid { font: 600 13px var(--f-mono); color: var(--pen); }
.chip { font-size: 12px; padding: 1px 8px; border-radius: 99px; background: var(--paper); color: var(--ink-2); }
.cost { font: 12px var(--f-mono); color: var(--ink-2); margin-left: auto; font-variant-numeric: tabular-nums; }
.q { width: 100%; font: 600 17px/1.4 var(--f-read); margin-top: 2px; text-wrap: pretty; }
.flags { padding: 8px 16px; background: var(--warn-wash); color: var(--warn); font-size: 13px; }
.pair { display: grid; grid-template-columns: 1fr 1fr; }
.pane { padding: 14px 16px; min-width: 0; display: flex; flex-direction: column; gap: 10px; }
.pane + .pane { border-left: 1px solid var(--rule); }
@media (max-width: 860px) { .pair { grid-template-columns: 1fr; } .pane + .pane { border-left: 0; border-top: 1px solid var(--rule); } }
.label { font-size: 11px; letter-spacing: .08em; text-transform: uppercase; color: var(--ink-2); font-weight: 700; }
.answer { font: 16px/1.6 var(--f-read); white-space: pre-wrap; overflow-wrap: anywhere; }
.checks { display: flex; flex-wrap: wrap; gap: 4px; font-size: 13px; }
.mark { padding: 1px 8px; border-radius: 6px; }
.mark.y { background: var(--ok-wash); color: var(--ok); } .mark.n { background: var(--warn-wash); color: var(--warn); }
.doc { border: 1px solid var(--rule); border-radius: 8px; padding: 9px 11px; font: 14.5px/1.55 var(--f-read); }
.doc.missing { border-style: dashed; border-color: var(--bad); background: var(--miss); }
.doc .t { font: 700 14px var(--f-ui); }
.doc .id { font: 11.5px var(--f-mono); color: var(--ink-2); margin-bottom: 3px; overflow-wrap: anywhere; }
.order { font: 13.5px/1.6 var(--f-ui); }
.order code { font: 12px var(--f-mono); color: var(--ink-2); }
.verdict { padding: 12px 16px; border-top: 1px solid var(--rule); display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.verdict button[aria-pressed="true"][data-v="correct"] { background: var(--ok-wash); border-color: var(--ok); color: var(--ok); }
.verdict button[aria-pressed="true"][data-v="partial"] { background: var(--warn-wash); border-color: var(--warn); color: var(--warn); }
.verdict button[aria-pressed="true"][data-v="wrong"],
.verdict button[aria-pressed="true"][data-v="hallucinated"] { background: var(--bad-wash); border-color: var(--bad); color: var(--bad); }
.verdict textarea { flex: 1 1 240px; min-width: 0; font: inherit; font-size: 14px; color: var(--ink); background: var(--paper);
  border: 1px solid var(--rule); border-radius: 8px; padding: 7px 9px; height: 40px; resize: vertical; }
@media (prefers-reduced-motion: reduce) { .meter i { transition: none; } }
</style>

<header class="bar">
  <h1>TechStore Grading Desk</h1>
  <span class="who" id="who">Phase 0 baseline · 50 answers from gpt-6.1-sol</span>
  <span class="spacer"></span>
  <span class="tally"><span class="meter"><i id="meter"></i></span><span id="count">0 / 50 graded</span></span>
  <span class="save local" id="save">Saving on this device</span>
  <select id="filter" aria-label="Show">
    <option value="all">All questions</option><option value="flagged">Flagged only</option><option value="todo">Not yet graded</option>
  </select>
  <button class="go" id="export" type="button">Export CSV</button>
</header>

<main class="wrap">
  <section class="brief">
    <p><b>How to grade.</b> Read the model's answer on the left and check each fact against the evidence on the right. That evidence is <b>exactly</b> what the model was given. A dashed red box is a document it needed but did not get.</p>
    <p>Green marks: the ₹ amount or quoted phrase appears in the evidence. Amber: it does not, so the model either calculated it (check the arithmetic) or invented it.</p>
    <div class="scale">
      <span><b>correct</b> answers fully; every fact matches the evidence</span>
      <span><b>partial</b> right but incomplete, says information is unavailable when the evidence had it, or infers something the evidence does not state</span>
      <span><b>wrong</b> contradicts the evidence, or the arithmetic is wrong</span>
      <span><b>hallucinated</b> states a fact the evidence does not contain that is not a correct calculation</span>
    </div>
    <p style="margin-top:8px">Extra detail the evidence supports is fine. Style and formatting go in the notes and do not change the verdict. If the evidence lacks something and the answer says so, that is correct.</p>
    <p style="margin-top:8px">Grade on your own. Your verdicts are private to you; other graders cannot see them.</p>
  </section>
  <section id="copybox" hidden>
    <p class="label">Your grades as CSV</p>
    <p>This view cannot save files. Copy the text below into a file named <code>review.csv</code>.</p>
    <textarea id="csvtext" readonly aria-label="CSV export"></textarea>
    <p><button id="copy" type="button">Copy</button> <span id="copied" class="who"></span></p>
  </section>
  <div id="sheets"></div>
</main>

<script id="data" type="application/json">__DATA__</script>
<script>
(() => {
  const RUN = "__RUN__";
  const ITEMS = JSON.parse(document.getElementById("data").textContent);
  const LOCAL_KEY = "grading:" + RUN;
  let state = {};
  try { state = JSON.parse(localStorage.getItem(LOCAL_KEY) || "{}") || {}; } catch (e) { state = {}; }

  let db = null, uid = null, online = false, me = null, downloads = null;
  const saveEl = document.getElementById("save");
  function setSave(text, local) { saveEl.textContent = text; saveEl.classList.toggle("local", !!local); }

  function el(tag, cls, text) { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function answerNode(text) {
    const d = el("div", "answer");
    text.split(/(\*\*[^*]+\*\*)/g).forEach(part => {
      if (/^\*\*[^*]+\*\*$/.test(part)) d.appendChild(el("b", null, part.slice(2, -2)));
      else d.appendChild(document.createTextNode(part));
    });
    return d;
  }

  const sheets = new Map();
  function render(it) {
    const s = el("article", "sheet"); s.id = "q-" + it.id;
    const h = el("div", "head");
    h.appendChild(el("span", "qid", it.id)); h.appendChild(el("span", "chip", it.category.replace(/_/g, " ")));
    if (it.expected) h.appendChild(el("span", "chip", "expected: " + it.expected.replace(/_/g, " ")));
    h.appendChild(el("span", "cost", "$" + it.cost.toFixed(4) + " · " + it.tok_in + "+" + it.tok_out + " tok"));
    h.appendChild(el("div", "q", it.question)); s.appendChild(h);
    if (it.flags.length) s.appendChild(el("div", "flags", "Flagged: " + it.flags.join(" · ")));

    const pair = el("div", "pair"), L = el("div", "pane"), R = el("div", "pane");
    L.appendChild(el("div", "label", "Model's answer")); L.appendChild(answerNode(it.answer));
    if (it.rupees.length || it.quotes.length) {
      const c = el("div", "checks");
      it.rupees.forEach(x => c.appendChild(el("span", "mark " + (x.found ? "y" : "n"), (x.found ? "✓ " : "? ") + x.text)));
      it.quotes.forEach(x => c.appendChild(el("span", "mark " + (x.found ? "y" : "n"), (x.found ? "✓ “" : "? “") + x.text + "”")));
      L.appendChild(c);
    }
    R.appendChild(el("div", "label", "Evidence the model was given"));
    if (!it.sources.length && !it.orders.length) R.appendChild(el("div", "doc", "No documents matched this question."));
    it.sources.forEach(d => {
      const b = el("div", "doc"); b.appendChild(el("div", "t", d.title));
      b.appendChild(el("div", "id", d.id + (d.gold ? " · needed for this question" : ""))); b.appendChild(el("div", null, d.text)); R.appendChild(b);
    });
    it.orders.forEach(o => {
      const b = el("div", "doc order"); b.appendChild(el("div", "t", "Order record #" + o.fields.order_id));
      Object.entries(o.fields).forEach(([k, v]) => { const r = el("div"); r.appendChild(el("code", null, k)); r.appendChild(document.createTextNode(" " + v)); b.appendChild(r); });
      o.items.forEach(i => b.appendChild(el("div", null, "Item: " + i)));
      o.charges.forEach(i => b.appendChild(el("div", null, "Charge: " + i))); R.appendChild(b);
    });
    if (it.missing.length) {
      R.appendChild(el("div", "label", "Needed but not retrieved"));
      it.missing.forEach(d => { const b = el("div", "doc missing"); b.appendChild(el("div", "t", d.title)); b.appendChild(el("div", "id", d.id)); b.appendChild(el("div", null, d.text)); R.appendChild(b); });
    }
    pair.appendChild(L); pair.appendChild(R); s.appendChild(pair);

    const v = el("div", "verdict"); const btns = [];
    ["correct", "partial", "wrong", "hallucinated"].forEach(name => {
      const b = el("button", null, name); b.type = "button"; b.dataset.v = name; b.id = "v-" + it.id + "-" + name;
      b.addEventListener("click", () => { mark(it.id, { verdict: name }); }); btns.push(b); v.appendChild(b);
    });
    const n = el("textarea"); n.id = "notes-" + it.id; n.placeholder = "Notes: why, if not correct"; n.setAttribute("aria-label", "Notes for " + it.id);
    n.addEventListener("input", () => mark(it.id, { notes: n.value }, true)); v.appendChild(n);
    s.appendChild(v);
    sheets.set(it.id, { s, btns, n });
    return s;
  }

  function paint(id) {
    const r = sheets.get(id), st = state[id] || {};
    r.btns.forEach(b => b.setAttribute("aria-pressed", String(b.dataset.v === st.verdict)));
    if (document.activeElement !== r.n) r.n.value = st.notes || "";
    r.s.classList.toggle("graded", !!st.verdict);
  }
  function tally() {
    const done = ITEMS.filter(i => (state[i.id] || {}).verdict).length;
    document.getElementById("count").textContent = done + " / " + ITEMS.length + " graded";
    document.getElementById("meter").style.width = (100 * done / ITEMS.length) + "%";
  }
  function filter() {
    const f = document.getElementById("filter").value;
    ITEMS.forEach(it => {
      const graded = !!(state[it.id] || {}).verdict;
      sheets.get(it.id).s.hidden = !(f === "all" || (f === "flagged" && it.flags.length) || (f === "todo" && !graded));
    });
  }

  let timer = null, writing = Promise.resolve(), dirty = false;
  function mark(id, patch, typing) {
    state[id] = Object.assign({}, state[id] || {}, patch);
    try { localStorage.setItem(LOCAL_KEY, JSON.stringify(state)); } catch (e) {}
    paint(id); tally(); if (!typing) filter();
    dirty = true; clearTimeout(timer); timer = setTimeout(flush, typing ? 1200 : 400);
  }
  function flush() {
    if (!online || !dirty) return;
    dirty = false; setSave("Saving…");
    const body = { run: RUN, verdicts: JSON.parse(JSON.stringify(state)), updatedAt: new Date().toISOString() };
    writing = writing.then(() => db.doc("grades/" + uid).set(body)).then(
      () => setSave("Saved online"),
      e => {
        if (e && (e.code === "invalid_argument" || e.code === "not_granted" || e.code === "revoked")) {
          online = false; setSave("Saving on this device only", true);
        } else { dirty = true; setSave("Not saved yet, retrying", true); setTimeout(flush, 3000 + Math.random() * 2000); }
      });
  }

  function csv() {
    const cell = s => { s = String(s == null ? "" : s); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
    const rows = [["id", "category", "expected_behavior", "question", "answer", "verdict", "notes"]];
    ITEMS.forEach(it => { const s = state[it.id] || {}; rows.push([it.id, it.category, it.expected, it.question, it.answer, s.verdict || "", s.notes || ""]); });
    return rows.map(r => r.map(cell).join(",")).join("\n");
  }
  document.getElementById("export").addEventListener("click", async () => {
    const who = (me && me.name ? me.name.split(" ")[0].toLowerCase().replace(/[^a-z0-9]/g, "") : "") || "grader";
    if (downloads) {
      try { await downloads.save({ filename: "review_" + RUN + "_" + who + ".csv", data: "﻿" + csv() }); return; }
      catch (e) { if (e && e.code === "declined") return; }
    }
    const box = document.getElementById("copybox"); box.hidden = false;
    document.getElementById("csvtext").value = csv(); box.scrollIntoView({ block: "start" });
  });
  document.getElementById("copy").addEventListener("click", () => {
    const t = document.getElementById("csvtext"), out = document.getElementById("copied");
    navigator.clipboard.writeText(t.value).then(() => { out.textContent = "Copied."; },
      () => { t.focus(); t.select(); out.textContent = "Press Cmd+C or Ctrl+C to copy the selected text."; });
  });
  document.getElementById("filter").addEventListener("change", filter);

  const host = document.getElementById("sheets");
  ITEMS.forEach(it => host.appendChild(render(it)));
  ITEMS.forEach(it => paint(it.id)); tally(); filter();

  if (window.claude && window.claude.use) {
    window.claude.use("downloads").then(d => { downloads = d; });
    Promise.all([window.claude.use("db"), window.claude.use("user")]).then(async ([d, u]) => {
      if (!d || !u) { setSave("Saving on this device only", true); return; }
      me = await u.me(); uid = me.id;
      if (me.name) document.getElementById("who").textContent = "Grading as " + me.name + " · 50 answers from gpt-6.1-sol";
      if (!uid) { setSave("Saving on this device only", true); return; }
      db = d;
      try {
        const snap = await db.doc("grades/" + uid).get();
        if (snap.exists) {
          const saved = (snap.data() || {}).verdicts || {};
          state = Object.assign({}, state, saved);
          try { localStorage.setItem(LOCAL_KEY, JSON.stringify(state)); } catch (e) {}
          ITEMS.forEach(it => paint(it.id)); tally(); filter();
        }
        online = true; setSave("Saved online");
        if (Object.keys(state).length && !snap.exists) { dirty = true; flush(); }
      } catch (e) { setSave("Saving on this device only", true); }
    });
  }
})();
</script>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("results")
    ap.add_argument("--questions", default=str(config.DEV_QUESTIONS_PATH))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    results = Path(args.results)
    items = build(results, Path(args.questions))
    data = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    page = PAGE.replace("__RUN__", html.escape(results.stem)).replace("__DATA__", data)
    Path(args.out).write_text(page, encoding="utf-8")
    print(f"{len(items)} questions -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
