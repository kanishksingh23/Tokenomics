"""Build a self-contained HTML page for grading a batch run by hand.

    python grading_view.py runs/2026-10-03_phase0/baseline_50.jsonl
    open runs/2026-10-03_phase0/baseline_50.grading.html

Each question shows the model's answer beside the full text of every document
and order record it was given, plus any needed document retrieval missed.
Rupee amounts and quoted phrases in the answer are checked against those
sources automatically. Verdicts save in the browser as you go and export to CSV.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

import config
from review_results import RUPEES, _amount, behavior_problem, load_jsonl

QUOTE = re.compile(r"[“\"]([^”\"]{8,}?)[”\"]")


def _norm(text: str) -> str:
    text = text.replace("’", "'").replace("‘", "'").replace("—", "-").replace("–", "-")
    return " ".join(text.lower().split())


def _quote_found(quote: str, source_norm: str) -> bool:
    """A quote counts as verified when every piece of it appears in the sources.
    Models bold text inside quotes and shorten them with an ellipsis; both are fine."""
    text = quote.replace("**", "").replace("\u2026", "...")
    pieces = [_norm(p).strip(" .,;:") for p in text.split("...")]
    pieces = [p for p in pieces if len(p) >= 4]
    return bool(pieces) and all(p in source_norm for p in pieces)


def _order_view(o: dict) -> dict:
    keep = ("order_id", "status", "placed_at", "delivered_at", "cancelled_at", "eta",
            "payment_method", "courier", "tracking_id", "total", "return_reason")
    return {"fields": {k: o[k] for k in keep if o.get(k) not in (None, "")},
            "items": [f"{i['qty']} × {i['name']} @ ₹{i['unit_price']:,}" for i in o["items"]],
            "charges": [", ".join(f"{k}: {v}" for k, v in c.items()) for c in o["charges"]]}


def build(results_path: Path, questions_path: Path) -> list[dict]:
    docs = {d["id"]: d for d in load_jsonl(config.KB_PATH)}
    orders = {o["order_id"]: o for o in load_jsonl(config.ORDERS_PATH)}
    qs = load_jsonl(questions_path)
    by_id = {q["id"]: q for q in qs}
    by_text = {q["question"]: q for q in qs}

    items = []
    for r in load_jsonl(results_path):
        q = by_id.get(r.get("id")) or by_text.get(r["question"]) or {}
        gold = q.get("context_ids", [])
        retrieved = r.get("retrieved", [])
        missing = [g for g in gold if g not in retrieved]
        used_orders = [orders[o] for o in r.get("orders_used", []) if o in orders]

        # Titles and the customer's own words are legitimate things to quote.
        source_text = " ".join(f'{docs[d]["title"]}. {docs[d]["text"]}' for d in retrieved if d in docs)
        source_text += " " + r["question"]
        source_text += " " + " ".join(json.dumps(o, ensure_ascii=False) for o in used_orders)
        source_norm = _norm(source_text)
        source_amounts = {_amount(m) for m in RUPEES.findall(source_text)}
        for d in retrieved:
            if docs.get(d, {}).get("price"):
                source_amounts.add(float(docs[d]["price"]))
        for o in used_orders:
            source_amounts.add(float(o["total"]))
            source_amounts.update(float(i["unit_price"]) for i in o["items"])
            source_amounts.update(float(c["amount"]) for c in o["charges"])

        answer = r.get("error") or r.get("answer") or ""
        rupees = [{"text": "₹" + m, "found": _amount(m) in source_amounts} for m in RUPEES.findall(answer)]
        quotes = [{"text": m.replace("**", "").strip(), "found": _quote_found(m, source_norm)}
                  for m in QUOTE.findall(answer)]

        flags = []
        if r.get("error"):
            flags.append("error")
        if r.get("finish_reason") == "length":
            flags.append("cut off at the output limit")
        if missing:
            flags.append("retrieval missed a needed document")
        behaviour = None if r.get("error") else behavior_problem(
            q.get("expected_behavior"), answer, missing_gold=bool(missing))
        if behaviour:
            flags.append(behaviour)
        if any(not x["found"] for x in rupees):
            flags.append("an amount is not in the sources (computed, or invented)")
        if any(not x["found"] for x in quotes):
            flags.append("a quoted phrase is not word-for-word in the sources")

        items.append({
            "id": r.get("id") or q.get("id", "?"),
            "category": r.get("category") or q.get("category", ""),
            "expected": q.get("expected_behavior", ""),
            "question": r["question"],
            "answer": answer,
            "cost": r.get("cost_usd", 0), "tok_in": r.get("prompt_tokens", 0),
            "tok_out": r.get("completion_tokens", 0),
            "flags": flags, "rupees": rupees, "quotes": quotes,
            "sources": [{"id": d, "title": docs[d]["title"], "text": docs[d]["text"],
                         "gold": d in gold} for d in retrieved if d in docs],
            "missing": [{"id": d, "title": docs[d]["title"], "text": docs[d]["text"]}
                        for d in missing if d in docs],
            "orders": [_order_view(o) for o in used_orders],
        })
    return items


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Grading: __RUN__</title>
<style>
:root{--bg:#f6f7f9;--card:#fff;--ink:#1d2330;--muted:#5f6b7a;--line:#e1e5ea;--ok:#127a3d;--okbg:#e6f4ea;
--warn:#a45a00;--warnbg:#fff1dc;--bad:#b3261e;--badbg:#fde7e6;--acc:#2f5bd3;--accbg:#e8eefc}
@media (prefers-color-scheme:dark){:root{--bg:#14171c;--card:#1d2128;--ink:#e6e9ee;--muted:#9aa4b2;--line:#2e343e;
--ok:#6fd08f;--okbg:#18311f;--warn:#f0b35a;--warnbg:#382a14;--bad:#ff8a80;--badbg:#3a1c1b;--acc:#8fb0ff;--accbg:#1f2a44}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--card);border-bottom:1px solid var(--line);padding:12px 16px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
header h1{font-size:17px;margin:0 12px 0 0}.prog{font-variant-numeric:tabular-nums;color:var(--muted)}
button,select{font:inherit;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;padding:6px 12px;cursor:pointer}
button.primary{background:var(--acc);border-color:var(--acc);color:#fff}
main{max-width:1180px;margin:0 auto;padding:16px}
.help{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin-bottom:16px;color:var(--muted)}
.help b{color:var(--ink)}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;margin-bottom:18px;overflow:hidden}
.card.done{border-color:var(--ok)}
.top{padding:12px 16px;border-bottom:1px solid var(--line);display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.qid{font-weight:700}.tag{font-size:12px;padding:2px 8px;border-radius:99px;background:var(--accbg);color:var(--acc)}
.q{font-size:16px;font-weight:600;width:100%;margin-top:4px}
.flags{padding:8px 16px;background:var(--warnbg);color:var(--warn);font-size:13px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:0}@media (max-width:860px){.grid{grid-template-columns:1fr}}
.pane{padding:12px 16px;min-width:0}.pane+.pane{border-left:1px solid var(--line)}@media (max-width:860px){.pane+.pane{border-left:0;border-top:1px solid var(--line)}}
h3{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:4px 0 8px}
.answer{white-space:pre-wrap;word-wrap:break-word}
.checks{margin-top:10px;font-size:13px}.chip{display:inline-block;margin:2px 4px 2px 0;padding:1px 8px;border-radius:6px}
.chip.y{background:var(--okbg);color:var(--ok)}.chip.n{background:var(--warnbg);color:var(--warn)}
.src{border:1px solid var(--line);border-radius:8px;padding:8px 10px;margin-bottom:8px;font-size:14px}
.src.miss{border-style:dashed;background:var(--badbg)}.src .t{font-weight:600}.src .id{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--muted)}
.order{font-size:13px}.order code{font-size:12px}
.grade{padding:12px 16px;border-top:1px solid var(--line);display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.grade button.sel[data-v=correct]{background:var(--okbg);border-color:var(--ok);color:var(--ok)}
.grade button.sel[data-v=partial]{background:var(--warnbg);border-color:var(--warn);color:var(--warn)}
.grade button.sel[data-v=wrong],.grade button.sel[data-v=hallucinated]{background:var(--badbg);border-color:var(--bad);color:var(--bad)}
.grade textarea{flex:1;min-width:220px;font:inherit;border:1px solid var(--line);border-radius:8px;padding:6px 8px;background:var(--bg);color:var(--ink);height:38px}
</style></head><body>
<header><h1>Grading · __RUN__</h1><span class="prog" id="prog"></span>
<select id="filter"><option value="all">All questions</option><option value="flagged">Flagged only</option><option value="todo">Not yet graded</option></select>
<button class="primary" id="dl">Download review CSV</button></header>
<main>
<div class="help"><b>How to grade:</b> read the answer on the left and check every fact against the sources on the right —
those are <b>exactly</b> what the model was given. A dashed red box is a document it <b>needed but did not get</b>.
Green chips: amount or quote found in the sources. Orange: not found — either computed (check the arithmetic) or invented.<br>
<b>correct</b> fully answers; every fact matches the sources ·
<b>partial</b> right but incomplete, <i>or</i> says information is unavailable when the sources had it, <i>or</i> infers something the sources do not state ·
<b>wrong</b> contradicts the sources, or the arithmetic is wrong ·
<b>hallucinated</b> states a fact the sources do not contain that is not a correct calculation.<br>
<b>Also:</b> extra detail the sources support is fine · style and formatting go in notes and do not change the verdict ·
if the sources lack something and the answer says so, that is correct. Your grades save in this browser automatically.</div>
<div id="list"></div></main>
<script id="data" type="application/json">__DATA__</script>
<script>
const ITEMS = JSON.parse(document.getElementById('data').textContent);
const KEY = 'grading:__RUN__';
let state = {}; try { state = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) {}
function save(){ try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} progress(); }
function el(tag, cls, text){ const e=document.createElement(tag); if(cls) e.className=cls; if(text!=null) e.textContent=text; return e; }
function answerNode(text){
  const d=el('div','answer');
  text.split(/(\*\*[^*]+\*\*)/g).forEach(part=>{
    if(/^\*\*[^*]+\*\*$/.test(part)){ d.appendChild(el('b',null,part.slice(2,-2))); } else { d.appendChild(document.createTextNode(part)); }
  });
  return d;
}
function card(it){
  const c=el('div','card'); c.id='card-'+it.id;
  const top=el('div','top'); top.appendChild(el('span','qid',it.id)); top.appendChild(el('span','tag',it.category));
  if(it.expected) top.appendChild(el('span','tag','expected: '+it.expected));
  top.appendChild(el('span','prog','$'+it.cost.toFixed(4)+' · '+it.tok_in+'+'+it.tok_out+' tokens'));
  top.appendChild(el('div','q',it.question)); c.appendChild(top);
  if(it.flags.length) c.appendChild(el('div','flags','⚑ '+it.flags.join(' · ')));
  const g=el('div','grid'); const L=el('div','pane'); const R=el('div','pane');
  L.appendChild(el('h3',null,"Model's answer")); L.appendChild(answerNode(it.answer));
  if(it.rupees.length||it.quotes.length){
    const ch=el('div','checks'); ch.appendChild(el('div',null,'Automatic checks against the sources:'));
    it.rupees.forEach(x=>ch.appendChild(el('span','chip '+(x.found?'y':'n'),(x.found?'✓ ':'? ')+x.text)));
    it.quotes.forEach(x=>ch.appendChild(el('span','chip '+(x.found?'y':'n'),(x.found?'✓ “':'? “')+x.text+'”')));
    L.appendChild(ch);
  }
  R.appendChild(el('h3',null,'Sources the model was given'));
  if(!it.sources.length && !it.orders.length) R.appendChild(el('div','src','(no documents matched this question)'));
  it.sources.forEach(s=>{ const b=el('div','src'); b.appendChild(el('div','t',(s.gold?'✓ ':'')+s.title));
    b.appendChild(el('div','id',s.id+(s.gold?' · needed for this question':''))); b.appendChild(el('div',null,s.text)); R.appendChild(b); });
  it.orders.forEach(o=>{ const b=el('div','src order'); b.appendChild(el('div','t','Order record #'+o.fields.order_id));
    Object.entries(o.fields).forEach(([k,v])=>{ const r=el('div'); r.appendChild(el('code',null,k)); r.appendChild(document.createTextNode(': '+v)); b.appendChild(r); });
    o.items.forEach(i=>b.appendChild(el('div',null,'• '+i))); o.charges.forEach(i=>b.appendChild(el('div',null,'charge — '+i))); R.appendChild(b); });
  if(it.missing.length){ R.appendChild(el('h3',null,'Needed but NOT retrieved'));
    it.missing.forEach(s=>{ const b=el('div','src miss'); b.appendChild(el('div','t',s.title)); b.appendChild(el('div','id',s.id)); b.appendChild(el('div',null,s.text)); R.appendChild(b); }); }
  g.appendChild(L); g.appendChild(R); c.appendChild(g);
  const gr=el('div','grade'); const st=state[it.id]||{};
  ['correct','partial','wrong','hallucinated'].forEach(v=>{ const b=el('button',st.verdict===v?'sel':'',v); b.dataset.v=v;
    b.onclick=()=>{ state[it.id]=Object.assign(state[it.id]||{},{verdict:v}); save(); gr.querySelectorAll('button').forEach(x=>x.classList.toggle('sel',x.dataset.v===v)); c.classList.add('done'); applyFilter(); };
    gr.appendChild(b); });
  const n=el('textarea'); n.placeholder='notes — why, if not correct'; n.value=st.notes||'';
  n.oninput=()=>{ state[it.id]=Object.assign(state[it.id]||{},{notes:n.value}); save(); }; gr.appendChild(n);
  if(st.verdict) c.classList.add('done');
  c.appendChild(gr); return c;
}
function progress(){ const n=ITEMS.filter(i=>(state[i.id]||{}).verdict).length; document.getElementById('prog').textContent=n+' / '+ITEMS.length+' graded'; }
function applyFilter(){ const f=document.getElementById('filter').value;
  ITEMS.forEach(it=>{ const c=document.getElementById('card-'+it.id); const graded=!!(state[it.id]||{}).verdict;
    c.style.display=(f==='all'||(f==='flagged'&&it.flags.length)||(f==='todo'&&!graded))?'':'none'; }); }
function csvCell(s){ s=String(s==null?'':s); return /[",\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s; }
document.getElementById('dl').onclick=()=>{
  const rows=[['id','category','expected_behavior','question','answer','verdict','notes']];
  ITEMS.forEach(it=>{ const s=state[it.id]||{}; rows.push([it.id,it.category,it.expected,it.question,it.answer,s.verdict||'',s.notes||'']); });
  const blob=new Blob(['﻿'+rows.map(r=>r.map(csvCell).join(',')).join('\n')],{type:'text/csv;charset=utf-8'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='review___RUN__.csv'; a.click();
};
document.getElementById('filter').onchange=applyFilter;
const list=document.getElementById('list'); ITEMS.forEach(it=>list.appendChild(card(it))); progress(); applyFilter();
</script></body></html>"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("results")
    ap.add_argument("--questions", default=str(config.DATA_DIR / "questions_seed.jsonl"))
    ap.add_argument("--out")
    args = ap.parse_args()
    results = Path(args.results)
    items = build(results, Path(args.questions))
    run = results.stem
    data = json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    page = PAGE.replace("__RUN__", html.escape(run)).replace("__DATA__", data)
    out = Path(args.out) if args.out else results.with_suffix(".grading.html")
    out.write_text(page, encoding="utf-8")
    flagged = sum(bool(i["flags"]) for i in items)
    print(f"{len(items)} questions ({flagged} flagged) -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
