# Writing the TechStore Test Questions

A guide for writing the **36 test questions** in `data/questions_test.jsonl`. Read it once fully before starting; after that, the checklists and the appendices are what you will keep coming back to.

**Two tasks, in this order:**
1. The 36 test questions (most of this guide), about 2–2½ hours.
2. After they're done: a small **repeat-traffic set** of 36 variants for testing the answer cache, about 20–30 minutes. See [the repeat-traffic set](#after-the-test-set-the-repeat-traffic-set-for-the-cache).

## Why this set matters

Every fix we made in Phase 0 — document wording, search rules, the prompt — was made after looking at the 50 seed questions, so the system is now fitted to them. On 14 questions written later, keyword search found the right document only 8 times out of 14, while it had looked best on the seeds. **The test set is how we find out how the system does on questions it has never seen.** Every token- and cost-saving technique we build is finally measured on it, so the questions we tuned on (the 64 dev questions) never decide the final result.

That only works if the test set stays independent of everything we tune. Hence the rules below.

## The rules

1. **Write in a customer's words, never the document's.** Lowercase, typos, abbreviations, missing punctuation, "earphones" rather than "earbuds", "it keeps blinking" rather than "flickering". Copying a document's wording makes the search look better than it really is.
2. **Write blind.** Do not run the agent on test questions before the set is frozen. If you try a question, see it fail and reword it, the test stops measuring the real system.
3. **Every question must be answerable from the documents** (except out-of-scope ones). Check the answer is actually there before you write the question. If a fact you need is missing, tell Kanishk so a document can be added **before** freezing — never after.
4. **No copies of dev questions.** `data/questions_dev.jsonl` holds the 64 dev questions. Don't reuse them or reword them; write about different situations. The validator rejects exact copies.
5. **AI may help with phrasing, never with the decisions** (details in [Using AI](#using-ai)). You choose the final wording, the documents and the key points.
6. **Hinglish questions are on hold** for now. Write in English.

The store's date is **30 September 2026**. Every order record and every "is it late?" judgement uses that date, not today's real date.

## The 9 categories

| Category | Test target | Expected tier | In one line |
|:---|---:|:---|:---|
| `simple_faq` | 4 | economy | One fact about a policy, delivery, payment or account |
| `order_status` | 4 | economy | About one specific order, by its order number |
| `product_info` | 3 | economy | One fact about one product |
| `product_comparison` | 4 | economy_escalation | Choosing between products, or "which one is best for…" |
| `troubleshooting` | 3 | economy | Something the customer owns isn't working |
| `billing_dispute` | 5 | frontier | A problem with money: charges, refunds, EMI, invoices |
| `technical_api` | 5 | frontier | A developer using the TechStore Partner API |
| `policy_edge_case` | 4 | frontier | Two rules collide, or a rule meets an unusual situation |
| `out_of_scope` | 4 | economy | The documents can't or shouldn't answer it |
| **Total** | **36** | | |

**Expected tier** is your judgement of which model a well-built router *should* pick:
- `economy` — a cheap model can answer it from one document.
- `economy_escalation` — a cheap model will probably try, but may need the expensive one (comparisons often do).
- `frontier` — needs the expensive model: several documents, arithmetic, code, or careful reasoning.

When unsure, use the table's default for the category.

### 1. `simple_faq` — 4 questions
One fact, one document. Policies (`pol_…`), shipping (`ship_…`), payment (`bill_payment_methods`), account (`acc_…`).

```
"if i order now can it come tomorrow?"
   docs: ship_charges
   key points: express next-day delivery costs ₹149 · metro cities only · order before 2 PM

"is there an extra fee if i pay cash on delivery"
   docs: bill_payment_methods
   key points: ₹49 handling fee · refunded if the order is cancelled before dispatch
```

### 2. `order_status` — 4 questions
About one real order. **Use an order number from [Appendix B](#appendix-b-the-40-orders)** and put it in `order_ids`. Vary the status (processing, shipped, delivered, cancelled, returned), and remember the store's date.

```
"48390 still says processing, when does it ship??"
   orders: 48390 · docs: ship_tracking
   key points: status is Processing · expected 2 October 2026 · tracking link sent by email and SMS once shipped
```

### 3. `product_info` — 3 questions
One fact about one product (`prod_…`). Name the product the way a customer would ("the voltbank", "pulsebook air").

```
"can i take the voltbank on a plane"
   docs: prod_voltbank20k
   key points: capacity is under 100 Wh · check the airline's rules before flying

"how heavy is the pulsebook air"
   docs: prod_pulsebook_air13
   key points: 1.12 kg
```

### 4. `product_comparison` — 4 questions
Choosing between products, or asking for the best one for a purpose. List **every product page needed** in `context_ids` (not `catalogue_summary`). Include some that name a category instead of products ("your cheapest laptop"), and some with a budget.

```
"cheapest laptop you have thats fine for coding?"
   docs: prod_pulsebook_air13, prod_pulsebook14, prod_pulsebook_pro16
   key points: PulseBook Air 13 is the cheapest at ₹44,999 · it has 8 GB RAM

"aurawatch 3 or the pro if i swim a lot"
   docs: prod_aurawatch3, prod_aurawatch_pro
   key points: AuraWatch 3 is rated 5 ATM · AuraWatch Pro is rated 10 ATM
```

### 5. `troubleshooting` — 3 questions
Something the customer owns isn't working. Mostly `tsg_…` documents; add `pol_warranty_terms` when the honest answer is "this is a warranty defect".

```
"my studio buds only play in the left ear"
   docs: tsg_earbuds_one_side
   key points: put both buds in the case for 10 seconds · reset by holding both touch panels for 15 seconds · clean the charging contacts
```

### 6. `billing_dispute` — 5 questions
Money. These need the most care: several documents, often an order record, often arithmetic. Order **48712** has three charges (one payment, two duplicate holds); most other orders have one.

```
"paid half with a gift card and half on UPI, returned it, where does my money go"
   docs: bill_gift_card, pol_refund_timeline
   key points: gift-card portion comes back as store credit · the rest goes back to UPI
```

### 7. `technical_api` — 5 questions
A developer integrating with the Partner API (`api_…`): error codes, webhooks, tokens, retries, pagination. You don't need to understand the code; the documents say what the right answer is. Developers write tersely and paste error messages.

```
"our webhook endpoint stopped getting events, did you turn it off?"
   docs: api_webhook_retries
   key points: failed deliveries retry at 1, 5, 25 and 125 minutes · then the endpoint is marked unhealthy and paused until reactivated

"inventory endpoint says 5 in stock but creating the order fails with 422"
   docs: api_inventory
   key points: stock figures can lag up to 60 seconds · handle 422 out_of_stock on order creation
```

### 8. `policy_edge_case` — 4 questions
Two rules meet, or a rule meets an unusual case. Usually 2–3 documents. The best ones make the customer's situation sound reasonable while the rules point the other way.

```
"preordered the y500 and the date keeps moving, its 3 weeks late now. can i cancel and get all my money back?"
   docs: pol_preorder
   key points: a delay of more than 14 days allows cancelling for a full refund

"need 12 monitors for our office, do we still get 30 days to return them?"
   docs: pol_bulk_orders
   key points: more than 10 units is a business order · business orders have a 15-day return window · a GSTIN is required
```

### 9. `out_of_scope` — 4 questions
Questions the documents can't or shouldn't answer. Each needs an `expected_behavior`:

| `expected_behavior` | Count | Meaning | Example |
|:---|---:|:---|:---|
| `decline_off_topic` | 1 | Nothing to do with TechStore; must decline even if the model knows the answer | *"whats the weather in delhi today"* |
| `admit_unknown` | 1 | About TechStore, but not in the documents; must say so, never invent | *"do you take my old laptop in exchange"* |
| `answer_from_about` | 1 | Answered by the About TechStore document (`about_techstore`) | *"do you sell gaming consoles"* |
| `partial` | 1 | Half answerable, half not | *"what colours does the x200 come in and can you engrave it"* |

For `admit_unknown`, check the knowledge base really doesn't cover it; search for the obvious words in [Appendix A](#appendix-a-the-85-documents-you-can-list). Leave `context_ids` empty except for `answer_from_about` (`about_techstore`) and `partial` (the document for the answerable half).

## Make them varied

Within every category, mix these **question types**:

| Type | Example |
|:---|:---|
| Plain question | "how long does delivery take to pune" |
| Yes / no | "can i pay with a credit card on emi" |
| How do I… | "how do i turn on the noise cancelling" |
| Complaint | "THIRD time asking, where is my refund" |
| Vague | "it's not working" (with just enough detail to answer) |
| Two questions at once | "is the x200 waterproof and how long is the warranty" |
| **Wrong assumption** | "your returns are 45 days right? bought my monitor 40 days ago" — the model must correct the customer, not agree |
| Customer's own context | "my son ordered headphones for me, how do i make them work with my phone" |

And rotate through **personas**:

| Persona | How they write |
|:---|:---|
| Student on a budget | short, price-focused, "cheapest", "under 50k" |
| Frustrated customer | capitals, repetition, blame |
| Older customer | polite, long, unsure of terms, explains the situation |
| Business buyer | quantities, GST, invoices, deadlines |
| Developer | terse, error codes, pasted messages |
| Busy professional | one line, no greeting |

With only 3–5 questions per category, give each question in a category a **different type and persona**.

## Writing key points

Key points are **the 1–3 facts a correct answer must contain**. Graders and the AI judge check every answer against them.

- **Facts, not wording**: *"₹49 handling fee"*, not *"the answer should mention that there might be a fee"*.
- **Include the numbers**: prices, days, hours, limits.
- **Only what matters**: if a correct answer could leave something out and still be correct, it isn't a key point.
- **Take them from the documents**, never from memory or general knowledge.
- **For out-of-scope**, describe the behaviour: *"declines; says it only helps with TechStore orders, products and support"*.

## Using AI

AI can help you find **different ways a customer might phrase** a situation. Three rules:

1. **Use Gemini (or another non-GPT model), not ChatGPT and not Claude.** GPT is the model being tested: if it writes the questions, it writes ones it handles well. Claude wrote the knowledge base: if it wrote the questions, its blind spots would sit on both sides.
2. **Describe the situation in your own words. Never paste in the documents**, or the AI will copy their wording.
3. **You decide everything else**: pick or edit the wording, choose the documents, write the key points. Mark the question `"source": "ai_assisted"`; questions you wrote yourself are `"source": "human"`.

A prompt to adapt:

```
I run support for an online electronics shop in India. Write 6 different
messages a real customer might send about this situation:

  [describe the situation in one or two sentences]

Make them different: one casual with typos, one angry, one very short, one from
an older person who isn't comfortable with technology, one that asks two things
at once, and one from a busy professional. Write in English. Don't make them
formal or polite.
```

## The format

Each question is **one line** in `data/questions_test.jsonl`. Ids run `t001` to `t036`.

```json
{"id": "t001", "category": "simple_faq", "question": "if i order now can it come tomorrow?", "context_ids": ["ship_charges"], "expected_tier": "economy", "key_points": ["Express next-day delivery costs ₹149", "Metro cities only, order before 2 PM"], "source": "human"}
{"id": "t005", "category": "order_status", "question": "48390 still says processing, when does it ship??", "context_ids": ["ship_tracking"], "order_ids": ["48390"], "expected_tier": "economy", "key_points": ["Status is Processing", "Expected 2 October 2026", "Tracking link sent by email and SMS once shipped"], "source": "human"}
{"id": "t033", "category": "out_of_scope", "question": "whats the weather in delhi today", "context_ids": [], "expected_tier": "economy", "expected_behavior": "decline_off_topic", "key_points": ["Declines; says it only helps with TechStore orders, products and support"], "source": "human"}
```

| Field | Required | Notes |
|:---|:---|:---|
| `id` | yes | `t001` … `t036` |
| `category` | yes | One of the 9 above |
| `question` | yes | The customer's message, in their words |
| `context_ids` | yes | Document ids from Appendix A. Empty only for out-of-scope |
| `order_ids` | for order questions | From Appendix B, as text: `["48390"]` |
| `expected_tier` | yes | `economy`, `economy_escalation` or `frontier` |
| `key_points` | yes | 1–3 facts, as a list |
| `expected_behavior` | out-of-scope only | See category 9 |
| `source` | yes | `human` or `ai_assisted` |

The examples in this guide show the format only. **Don't use them as test questions**: they were written by Claude.

## Before each question goes in: checklist

- [ ] Is the answer actually in the documents I listed?
- [ ] Did I list **all** the documents a full answer needs, and no extra ones?
- [ ] Is it worded the way a customer would write it, not the way the document does?
- [ ] Is it clear which product or order it's about? (If not, is the vagueness on purpose?)
- [ ] Are the key points facts, with numbers, taken from the documents?
- [ ] Is it different from every dev question?
- [ ] For order questions: is the order number real, and does the question make sense on 30 September 2026?

## Common mistakes

| Mistake | Why it matters |
|:---|:---|
| Copying a document's phrasing | Hides search failures; the earlier keyword/embedding result came from exactly this |
| An answer that isn't in the documents | Every model fails it, and that tells us nothing about the router |
| Too many documents in `context_ids` | Retrieval looks worse than it is |
| Key points like "explains the policy" | Graders can't check them |
| Using real-world facts (real prices, real laws) | TechStore is fictional; only the documents are true here |
| Thinking in today's real date | The store's date is 30 September 2026 |
| Trying the question on the agent first | Breaks the "write blind" rule |

## Process

**One-time setup** (needed for `validate_data.py`): after `git pull`, run this once from the
repo root (the `Tokenomics` folder, not `techstore`):

```bash
pip install -e ".[gateway,embeddings]"
```

If you skip it, the scripts stop with a message telling you to run exactly this.

1. **Write one category at a time.** Roughly 3–4 minutes per question: about 2–2½ hours for all 36.
2. After each batch, run:
   ```bash
   python validate_data.py
   ```
   It shows progress per category and names any problem: an unknown document or order id, a missing field, a duplicate.
3. **Spot-check**: Kanishk reads 20 random questions against the documents and their key points.
4. **Freeze**, once all 36 are in and validation passes:
   ```bash
   python validate_data.py --freeze
   ```
   This writes `questions_test.sha256`. Commit both files. From then on, any edit to the test set fails validation.

---

## After the test set: the repeat-traffic set (for the cache)

**Do this only after your 36 test questions are finished.** About 20–30 minutes.

### Why

Tokenomics has an **answer cache**: when a customer asks something that was already answered,
even in different words, it reuses the saved answer instead of paying the model again. It saves
money only when customers **repeat** each other, and our question sets have no repeats on
purpose. So this small set measures two things:

1. **Saving:** how often the cache recognises a real repeat and reuses the answer.
2. **Safety:** whether it refuses look-alike questions that need a *different* answer. Reusing an
   answer there would give a customer the wrong information.

It has to be written by you, not by Kanishk or Claude: Claude set how strict the cache is, so it
must not also write the exam.

### What to write

1. **Pick 12 of your 36 test questions** whose answer is the same for every customer: simple FAQs,
   product info, policies, general troubleshooting. **Don't pick `order_status` questions** or
   anything with an order number; those are personal and the cache never stores them.
2. **For each of the 12, write 3 variants:**

| `type` | How many | Rule |
|:---|---:|:---|
| `same` | 2 | **Same meaning and the same correct answer**, in different words, as a different customer would type it. Keep any numbers and product names exactly as in the original. |
| `different` | 1 | **Looks almost the same but needs a different answer.** Change one detail: the product, a number, on ↔ off, with ↔ without, before ↔ after, a payment method... |

That makes **36 lines** (12 × 3).

**Example.** Original test question `t007`: *"can i return headphones after opening them"*

| `type` | Variant | Why it's a good one |
|:---|:---|:---|
| `same` | *"opened my headphones, can they still go back?"* | Same question, different words |
| `same` | *"earphones box is open now, return possible??"* | Same question, casual wording |
| `different` | *"can i return a laptop after opening it"* | Looks the same, but laptops have no hygiene rule, so the answer differs |

**Good `different` variants are the tricky ones**: almost word-for-word the same, with one detail
that changes the answer. A variant about a completely different topic tests nothing.

### Rules

- **Same rules as the test questions:** a customer's own words (lowercase and typos are fine),
  **write blind** (don't try them on the system), and Gemini only for phrasing ideas, never
  ChatGPT or Claude. Mark AI-helped lines `"source": "ai_assisted"`.
- A `same` variant must really have the same correct answer. If you're unsure, it's probably
  a `different`.
- Don't copy any dev or test question, and don't repeat the original word for word.

### Format

One line per variant in **`data/questions_repeat.jsonl`**. Ids run `r001` to `r036`.

```json
{"id": "r001", "repeat_of": "t007", "type": "same", "question": "opened my headphones, can they still go back?", "source": "human"}
{"id": "r002", "repeat_of": "t007", "type": "same", "question": "earphones box is open now, return possible??", "source": "human"}
{"id": "r003", "repeat_of": "t007", "type": "different", "question": "can i return a laptop after opening it", "source": "human"}
```

| Field | Notes |
|:---|:---|
| `id` | `r001` … `r036` |
| `repeat_of` | The id of your test question it's a variant of (`t…`) |
| `type` | `same` or `different` |
| `question` | The customer's message |
| `source` | `human` or `ai_assisted` |

### Check and hand over

```bash
python validate_data.py
```

It checks every line (known `repeat_of`, no order-status originals, no copies, `same` variants
keeping the original's numbers) and shows progress: "repeat set: 36 / 36". When it passes,
commit the file. Don't edit it after the cache has been measured on it.

---

## Appendix A: the 85 documents you can list

Use these ids in `context_ids`. The knowledge base has one more document, `catalogue_summary`, which the system adds automatically to comparison questions; don't list it.


### About (1)

| id | Title |
|:---|:---|
| `about_techstore` | About TechStore |

### Policies (13)

| id | Title |
|:---|:---|
| `pol_return_window` | Return Window |
| `pol_return_exclusions` | Non-Returnable Items |
| `pol_refund_timeline` | Refund Processing Time |
| `pol_exchange` | Exchange Policy |
| `pol_cancellation` | Order Cancellation |
| `pol_price_match` | Price Match Guarantee |
| `pol_warranty_terms` | Standard Warranty Terms |
| `pol_warranty_claim` | How to Raise a Warranty Claim |
| `pol_damaged_in_transit` | Damaged or Wrong Item Delivered |
| `pol_privacy_data` | Customer Data and Privacy |
| `pol_bulk_orders` | Bulk and Business Orders |
| `pol_preorder` | Pre-Orders |
| `pol_replacement_warranty` | Warranty on Replaced Units |

### Shipping and delivery (7)

| id | Title |
|:---|:---|
| `ship_delivery_times` | Delivery Timelines |
| `ship_charges` | Delivery Charges |
| `ship_tracking` | Tracking an Order |
| `ship_international` | International Shipping |
| `ship_failed_delivery` | Failed Delivery Attempts |
| `ship_open_box` | Open-Box Delivery |
| `ship_installation` | Installation and Demo |

### Account (5)

| id | Title |
|:---|:---|
| `acc_create` | Creating and Verifying an Account |
| `acc_password` | Password Reset |
| `acc_address` | Changing a Delivery Address |
| `acc_order_history` | Order History and Invoices |
| `acc_two_factor` | Two-Factor Authentication |

### Billing and payments (12)

| id | Title |
|:---|:---|
| `bill_payment_methods` | Accepted Payment Methods |
| `bill_failed_payment` | Payment Failed but Money Debited |
| `bill_duplicate_charge` | Duplicate or Multiple Charges |
| `bill_emi` | EMI and No-Cost EMI |
| `bill_invoice_gst` | Invoice and GST |
| `bill_refund_partial` | Partial Refunds on Multi-Item Orders |
| `bill_refund_to_closed_card` | Refund to a Closed or Expired Card |
| `bill_cod_refund` | Refunds on Cash-on-Delivery Orders |
| `bill_promo_codes` | Promotional Codes and Stacking |
| `bill_price_drop` | Price Drop After Purchase |
| `bill_gift_card` | Gift Cards and Store Credit |
| `bill_chargeback` | Bank Chargebacks and Disputes |

### Service and repairs (3)

| id | Title |
|:---|:---|
| `svc_centres` | Service Centre Network |
| `svc_out_of_warranty` | Out-of-Warranty Repair |
| `svc_accidental_damage` | Accidental Damage Protection |

### Products (16)

| id | Title | Price |
|:---|:---|---:|
| `prod_x200` | SoundWave X200 Wireless Headphones | ₹12,999 |
| `prod_y500` | SoundWave Y500 Premium Headphones | ₹24,999 |
| `prod_pulsebook14` | PulseBook 14 Laptop | ₹64,999 |
| `prod_pulsebook_pro16` | PulseBook Pro 16 Laptop | ₹134,999 |
| `prod_novatab11` | NovaTab 11 Tablet | ₹29,999 |
| `prod_voltcharge65` | VoltCharge 65W GaN Charger | ₹2,499 |
| `prod_aurawatch3` | AuraWatch 3 Smartwatch | ₹8,999 |
| `prod_clearview27` | ClearView 27 Monitor | ₹22,999 |
| `prod_m100` | SoundWave M100 Wireless Earbuds | ₹3,499 |
| `prod_studiobuds` | SoundWave Studio Buds Pro | ₹6,999 |
| `prod_pulsebook_air13` | PulseBook Air 13 Laptop | ₹44,999 |
| `prod_novatab_mini8` | NovaTab Mini 8 Tablet | ₹17,999 |
| `prod_voltcharge100` | VoltCharge 100W GaN Charger | ₹3,999 |
| `prod_voltbank20k` | VoltBank 20000mAh Power Bank | ₹2,999 |
| `prod_aurawatch_pro` | AuraWatch Pro Smartwatch | ₹15,999 |
| `prod_clearview32` | ClearView 32 Ultra Monitor | ₹39,999 |

### Troubleshooting (14)

| id | Title |
|:---|:---|
| `tsg_headphone_pairing` | Headphones Will Not Pair |
| `tsg_headphone_battery` | Headphone Battery Draining Fast |
| `tsg_laptop_not_charging` | Laptop Not Charging |
| `tsg_watch_sync` | Smartwatch Not Syncing |
| `tsg_monitor_no_signal` | Monitor Shows No Signal |
| `tsg_earbuds_one_side` | Only One Earbud Working |
| `tsg_earbuds_case_charge` | Earbud Case Not Charging |
| `tsg_laptop_slow` | Laptop Running Slowly |
| `tsg_laptop_overheating` | Laptop Overheating |
| `tsg_watch_battery` | Smartwatch Battery Draining Fast |
| `tsg_watch_inaccurate_hr` | Heart Rate Readings Inaccurate |
| `tsg_monitor_flicker` | Monitor Flickering |
| `tsg_monitor_usbc_power` | Monitor Not Charging Laptop over USB-C |
| `tsg_powerbank_not_charging` | Power Bank Not Charging Devices |

### Partner API (developers) (14)

| id | Title |
|:---|:---|
| `api_overview` | TechStore Partner API Overview |
| `api_auth` | API Authentication and 401 Errors |
| `api_webhook_signature` | Webhook Signature Verification and 403 Errors |
| `api_rate_limits` | API Rate Limits and 429 Errors |
| `api_error_codes` | API Error Codes |
| `api_idempotency` | API Idempotency |
| `api_pagination` | API Pagination |
| `api_webhook_retries` | Webhook Delivery and Retries |
| `api_webhook_events` | Webhook Event Types |
| `api_sandbox` | Sandbox Environment |
| `api_versioning` | API Versioning and Deprecation |
| `api_timeouts` | API Timeouts and Retry Safety |
| `api_inventory` | Inventory Endpoint |
| `api_scopes` | Token Scopes and 403 Errors |


## Appendix B: the 40 orders

As of the store's date, 30 September 2026. Use these numbers in `order_ids`.

| Order | Status | Items | Total | Paid by | Dates |
|:---|:---|:---|---:|:---|:---|
| 48213 | Shipped | SoundWave X200 | ₹12,999 | UPI | placed 14 September 2026; expected 30 September 2026 |
| 48217 | Delivered | NovaTab 11 | ₹29,999 | Credit Card | placed 15 September 2026; delivered 18 September 2026 |
| 48390 | Processing | PulseBook 14 | ₹64,999 | No-Cost EMI (6 months) | placed 20 September 2026; expected 2 October 2026 |
| 48455 | Cancelled | VoltCharge 65W GaN Charger | ₹2,499 | UPI | placed 22 September 2026; cancelled 22 September 2026 · refund due 1 October 2026 |
| 48501 | Delivered | SoundWave Y500 Premium | ₹24,999 | Credit Card | placed 23 September 2026; delivered 26 September 2026 |
| 48620 | Delivered | ClearView 27 | ₹22,999 | Net Banking | placed 25 September 2026; delivered 28 September 2026 |
| 48677 | Shipped | AuraWatch 3, VoltCharge 65W GaN Charger | ₹11,498 | UPI | placed 26 September 2026; expected 30 September 2026 |
| 48712 | Processing | SoundWave X200 | ₹12,999 | Credit Card | placed 27 September 2026; expected 1 October 2026 · **3 charges** |
| 48750 | Delivered | PulseBook Pro 16 | ₹134,999 | Credit Card | placed 24 August 2026; delivered 25 August 2026 |
| 48801 | Returned | AuraWatch 3 | ₹8,999 | UPI | placed 28 September 2026; delivered 10 September 2026 · refunded 26 September 2026 · returned: faulty heart-rate sensor |
| 48820 | Processing | PulseBook Air 13 | ₹44,999 | UPI | placed 5 September 2026; expected 1 October 2026 |
| 48821 | Shipped | AuraWatch Pro | ₹15,999 | Cash on Delivery | placed 23 September 2026; expected 3 October 2026 |
| 48822 | Delivered | AuraWatch 3 | ₹8,999 | UPI | placed 19 September 2026; delivered 22 September 2026 |
| 48823 | Delivered | ClearView 27, VoltCharge 65W GaN Charger | ₹25,498 | UPI | placed 24 September 2026; delivered 28 September 2026 |
| 48824 | Shipped | SoundWave X200, PulseBook 14 | ₹77,998 | Credit Card | placed 5 September 2026; expected 1 October 2026 |
| 48825 | Delivered | AuraWatch Pro | ₹15,999 | UPI | placed 2 September 2026; delivered 4 September 2026 |
| 48826 | Delivered | AuraWatch 3, PulseBook 14 | ₹73,998 | Credit Card | placed 10 September 2026; delivered 13 September 2026 |
| 48827 | Processing | NovaTab 11, SoundWave Studio Buds Pro | ₹36,998 | UPI | placed 4 September 2026; expected 6 October 2026 |
| 48828 | Shipped | NovaTab 11, AuraWatch Pro | ₹45,998 | Net Banking | placed 18 September 2026; expected 1 October 2026 |
| 48829 | Processing | SoundWave Y500 Premium | ₹24,999 | Net Banking | placed 17 September 2026; expected 2 October 2026 |
| 48830 | Delivered | ClearView 32 Ultra | ₹39,999 | Net Banking | placed 9 September 2026; delivered 11 September 2026 |
| 48831 | Returned | ClearView 32 Ultra, SoundWave Y500 Premium | ₹64,998 | UPI | placed 25 September 2026; delivered 27 September 2026 · refunded 30 September 2026 · returned: faulty on arrival |
| 48832 | Cancelled | PulseBook 14 | ₹64,999 | No-Cost EMI (6 months) | placed 27 September 2026; cancelled 27 September 2026 · refund due 7 October 2026 |
| 48833 | Delivered | SoundWave Studio Buds Pro | ₹6,999 | Cash on Delivery | placed 5 September 2026; delivered 7 September 2026 |
| 48834 | Cancelled | SoundWave Studio Buds Pro, PulseBook 14 | ₹71,998 | Net Banking | placed 6 September 2026; cancelled 6 September 2026 · refund due 1 October 2026 |
| 48835 | Delivered | NovaTab Mini 8 | ₹17,999 | Credit Card | placed 7 September 2026; delivered 9 September 2026 |
| 48836 | Returned | VoltCharge 65W GaN Charger | ₹2,499 | Net Banking | placed 27 September 2026; delivered 29 September 2026 · refunded 30 September 2026 · returned: wrong variant delivered |
| 48837 | Delivered | ClearView 27 | ₹22,999 | Net Banking | placed 7 September 2026; delivered 8 September 2026 |
| 48838 | Shipped | ClearView 32 Ultra | ₹39,999 | Credit Card | placed 28 September 2026; expected 5 October 2026 |
| 48839 | Delivered | PulseBook Pro 16 | ₹134,999 | UPI | placed 23 September 2026; delivered 26 September 2026 |
| 48840 | Shipped | ClearView 32 Ultra | ₹39,999 | UPI | placed 2 September 2026; expected 1 October 2026 |
| 48841 | Delivered | VoltCharge 65W GaN Charger, VoltCharge 100W GaN Charger | ₹6,498 | UPI | placed 17 September 2026; delivered 21 September 2026 |
| 48842 | Delivered | SoundWave Y500 Premium, PulseBook 14 | ₹89,998 | Credit Card | placed 16 September 2026; delivered 20 September 2026 |
| 48843 | Delivered | AuraWatch Pro, PulseBook Pro 16 | ₹150,998 | No-Cost EMI (6 months) | placed 7 September 2026; delivered 11 September 2026 |
| 48844 | Shipped | NovaTab 11 | ₹29,999 | Net Banking | placed 21 September 2026; expected 1 October 2026 |
| 48845 | Processing | NovaTab 11 | ₹29,999 | Net Banking | placed 15 September 2026; expected 6 October 2026 |
| 48846 | Delivered | VoltBank 20000mAh Power Bank | ₹2,999 | UPI | placed 8 September 2026; delivered 9 September 2026 |
| 48847 | Processing | PulseBook Air 13, VoltCharge 65W GaN Charger | ₹47,498 | Net Banking | placed 8 September 2026; expected 4 October 2026 |
| 48848 | Shipped | SoundWave X200 | ₹12,999 | Net Banking | placed 8 September 2026; expected 3 October 2026 |
| 48849 | Delivered | VoltBank 20000mAh Power Bank | ₹2,999 | UPI | placed 26 September 2026; delivered 29 September 2026 |

---

## Appendix C: 30 Multiple Choice Test Questions

Thirty multiple-choice questions (4 options each) created according to the rules, grounded in the TechStore knowledge base and orders as of 30 September 2026.

### 1. `simple_faq`

#### Q1 (`t001`)
**Question:** if i cancel an order before it gets shipped do i get the delivery charges back too
- A) Yes, cancelled orders are refunded in full including any delivery charge paid, within 5 to 7 business days.
- B) No, delivery fees are strictly non-refundable once an order is placed.
- C) Only 50% of the delivery charge is refunded if cancelled within 24 hours.
- D) Delivery charges are refunded only as non-expiring store credit.
- **Correct Answer:** A
- **Context Document:** `pol_cancellation`
- **Expected Tier:** `economy`
- **Key Points:** Cancelled orders are refunded in full including any delivery charges paid · Refund reaches original payment method in 5 to 7 business days · Cancellation is only possible before order is marked Shipped

#### Q2 (`t002`)
**Question:** how many days does delivery take to tier-2 cities like jaipur?
- A) 1 to 2 business days.
- B) 2 to 4 business days (excluding Sundays and national holidays).
- C) 5 to 7 business days.
- D) Same-day delivery if ordered before 2 PM.
- **Correct Answer:** B
- **Context Document:** `ship_delivery_times`
- **Expected Tier:** `economy`
- **Key Points:** Tier-2 cities take 2 to 4 business days · Orders placed after 2 PM are processed the next business day · Delivery estimates exclude Sundays and national holidays

#### Q3 (`t003`)
**Question:** do you guys provide free demo and installation for laptops or is that only for screens?
- A) Free demo and installation is offered for all laptops and monitors above ₹30,000.
- B) Free installation and demo is only provided for monitors above 27 inches; laptops do not require installation.
- C) Installation is available for laptops for an additional fee of ₹499.
- D) TechStore does not provide installation or demo for any products.
- **Correct Answer:** B
- **Context Document:** `ship_installation`
- **Expected Tier:** `economy`
- **Key Points:** Free installation and demo is only provided for monitors above 27 inches · Laptops, tablets, headphones, and watches do not require installation · Installation request is raised from Orders and scheduled within 48 hours of delivery

---

### 2. `order_status`

#### Q4 (`t004`)
**Question:** can i get tracking details and estimated arrival for order 48821
- A) Status is Shipped via Ekart with tracking ID EK4449941868, expected delivery date is 3 October 2026.
- B) It is currently Processing at the warehouse and expected to ship on 5 October 2026.
- C) It was Delivered on 28 September 2026 by BlueDart.
- D) It was Cancelled and refunded to your original payment method.
- **Correct Answer:** A
- **Order ID:** `48821`
- **Context Document:** `ship_tracking`
- **Expected Tier:** `economy`
- **Key Points:** Status is Shipped via Ekart with tracking ID EK4449941868 · Expected delivery date is 3 October 2026 · Contains AuraWatch Pro Smartwatch with Cash on Delivery total of ₹15,999

#### Q5 (`t005`)
**Question:** i bought a novatab over two weeks back on 15 sep order 48845 and its still processing?? whats going on
- A) Order 48845 was lost in transit and a replacement has been dispatched.
- B) Order 48845 for NovaTab 11 is in Processing status with an expected delivery date of 6 October 2026; tracking will update upon dispatch.
- C) Order 48845 was cancelled automatically due to a failed net banking verification.
- D) It was already delivered to your registered address on 20 September 2026.
- **Correct Answer:** B
- **Order ID:** `48845`
- **Context Document:** `ship_tracking`
- **Expected Tier:** `economy`
- **Key Points:** Order 48845 is in Processing status for a NovaTab 11 · Estimated delivery date is 6 October 2026 · Tracking information is sent via email and SMS once dispatched

#### Q6 (`t006`)
**Question:** showing order 48849 as delivered yesterday but i was not home, which courier dropped it
- A) It was delivered by BlueDart under tracking ID BD4471920381.
- B) It was marked Delivered on 29 September 2026 by Delhivery under tracking ID EK4426213146.
- C) It was delivered by Ekart under tracking ID DL8830114772.
- D) The courier marked a failed delivery attempt and will reattempt tomorrow.
- **Correct Answer:** B
- **Order ID:** `48849`
- **Context Document:** `ship_tracking`
- **Expected Tier:** `economy`
- **Key Points:** Marked Delivered on 29 September 2026 · Delivered by Delhivery under tracking ID EK4426213146 · Item delivered was VoltBank 20000mAh Power Bank

#### Q7 (`t007`)
**Question:** i received order 48835 on 9th september, do i still have time left to return it if i dont want it?
- A) Yes, 21 days have passed since delivery, so you have until 9 October 2026 within the 30-day return window.
- B) No, TechStore only offers a 15-day return window for tablets.
- C) No, the return window is 30 days from the order placement date (7 September), which has already closed.
- D) Yes, but a 20% restocking fee applies after 14 days of delivery.
- **Correct Answer:** A
- **Order ID:** `48835`
- **Context Document:** `pol_return_window`
- **Expected Tier:** `economy`
- **Key Points:** Eligible for return: 21 days have passed since delivery on 9 September 2026 · TechStore allows returns within 30 days of delivery (until 9 October 2026) · Item must be returned in original packaging with all accessories

---

### 3. `product_info`

#### Q8 (`t008`)
**Question:** does the novatab mini 8 support a pen or stylus for taking notes in college?
- A) Yes, it includes an active stylus inside the retail box.
- B) Yes, an active stylus can be purchased separately for ₹4,999.
- C) No, stylus support is not available on the NovaTab Mini 8; it is exclusive to the NovaTab 11.
- D) Yes, it supports any standard Bluetooth capacitive stylus without restriction.
- **Correct Answer:** C
- **Context Document:** `prod_novatab_mini8`
- **Expected Tier:** `economy`
- **Key Points:** Stylus is not supported on the NovaTab Mini 8 · Stylus support is exclusive to the NovaTab 11

#### Q9 (`t009`)
**Question:** can i wear the m100 earbuds during workouts or when it rains outside?
- A) No, the M100 has no water or sweat resistance rating and must be kept completely dry.
- B) Yes, the M100 has an IPX4 splash resistance rating, making it safe for workout sweat and light rain.
- C) Yes, it has an IPX8 waterproof rating and can be submerged while swimming.
- D) It is only splash resistant if purchased with the optional silicone protective sleeve.
- **Correct Answer:** B
- **Context Document:** `prod_m100`
- **Expected Tier:** `economy`
- **Key Points:** M100 has IPX4 splash resistance rating · Safe for sweat during workouts and light rain splashes

#### Q10 (`t010`)
**Question:** how much power delivery does the 32 inch clearview monitor give over usb c?
- A) 65 W.
- B) 90 W.
- C) 100 W.
- D) Supplies up to 140 W power delivery over USB-C.
- **Correct Answer:** D
- **Context Document:** `prod_clearview32`
- **Expected Tier:** `economy`
- **Key Points:** Supplies up to 140 W power delivery over USB-C · ClearView 32 Ultra Monitor price is ₹39,999

---

### 4. `product_comparison`

#### Q11 (`t011`)
**Question:** which voltcharge charger should i get to charge my pulsebook pro 16 at max speed?
- A) VoltCharge 65W (₹2,499), because 65 W provides maximum speed for all PulseBook models.
- B) VoltCharge 100W (₹3,999), because the PulseBook Pro 16 requires 100 W for full-speed charging.
- C) Either charger charges the Pro 16 at the identical maximum speed.
- D) Neither; the PulseBook Pro 16 can only be charged using a proprietary DC barrel adapter.
- **Correct Answer:** B
- **Context Documents:** `prod_voltcharge65`, `prod_voltcharge100`, `prod_pulsebook_pro16`
- **Expected Tier:** `economy_escalation`
- **Key Points:** VoltCharge 100W (₹3,999) is required for full-speed 100 W charging of PulseBook Pro 16 · VoltCharge 65W (₹2,499) is not sufficient to charge the Pro 16 at full speed

#### Q12 (`t012`)
**Question:** deciding between novatab mini 8 and the 11 inch one, what are the main screen and spec differences for the extra money?
- A) NovaTab 11 (₹29,999) offers an 11-inch 2.5K 120 Hz display, 8 GB RAM, 256 GB storage, and stylus support, whereas Mini 8 (₹17,999) has an 8.4-inch 90 Hz display, 6 GB RAM, 128 GB storage, and no stylus support.
- B) Both have identical screen sizes, but NovaTab 11 includes an OLED display and 5G cellular connectivity.
- C) NovaTab Mini 8 has a higher refresh rate screen (144 Hz) but smaller storage than the NovaTab 11.
- D) The only difference is screen size; internal processor, RAM, and stylus support are identical.
- **Correct Answer:** A
- **Context Documents:** `prod_novatab_mini8`, `prod_novatab11`
- **Expected Tier:** `economy_escalation`
- **Key Points:** NovaTab 11 (₹29,999) has an 11-inch 2.5K 120 Hz screen, 8 GB RAM, 256 GB storage, and stylus support · NovaTab Mini 8 (₹17,999) has an 8.4-inch 90 Hz screen, 6 GB RAM, 128 GB storage, and lacks stylus support

#### Q13 (`t013`)
**Question:** are the studio buds pro worth the extra price over m100 if i need active noise cancelling and wireless charging?
- A) No, both models feature identical active noise cancelling and wireless charging cases.
- B) Yes, Studio Buds Pro (₹6,999) includes 30 dB ANC and a wireless charging case, while M100 (₹3,499) lacks ANC and only has a wired USB-C case.
- C) M100 has active noise cancelling, but lacks wireless charging compared to Studio Buds Pro.
- D) Neither model supports wireless charging, but Studio Buds Pro has noise isolation tips.
- **Correct Answer:** B
- **Context Documents:** `prod_m100`, `prod_studiobuds`
- **Expected Tier:** `economy_escalation`
- **Key Points:** Studio Buds Pro (₹6,999) features 30 dB ANC and a wireless charging case · M100 (₹3,499) has no active noise cancellation and only wired USB-C charging · Studio Buds Pro provides 9 hours battery (32 with case) vs 7 hours (28 with case) for M100

---

### 5. `troubleshooting`

#### Q14 (`t014`)
**Question:** plugged my earbud case in after not using it for a couple months and the light isnt turning on at all, is it dead?
- A) If the LED does not turn on within 5 seconds, the battery is permanently depleted and out of warranty.
- B) A case left fully discharged for over a month may need up to 15 minutes before the LED responds; try a 5 V adapter and claim warranty if no LED lights up after 30 minutes on a known-good charger.
- C) You must hold the pairing button for 60 seconds while plugging it in to jump-start the charging circuit.
- D) The case cannot be charged with a USB-C cable once discharged; you must use a wireless charging pad.
- **Correct Answer:** B
- **Context Document:** `tsg_earbuds_case_charge`
- **Expected Tier:** `economy`
- **Key Points:** Cases uncharged for over a month may require up to 15 minutes before the LED responds · Confirm using a working USB-C cable and 5 V adapter · Raise a warranty claim if no LED lights up after 30 minutes on a known-good charger

#### Q15 (`t015`)
**Question:** my voltbank has 80% charge but when i plug my wireless earbuds into it they wont charge
- A) The VoltBank 20000 does not support charging accessories like earbuds under any circumstances.
- B) You need to double press the power button to enable low-draw charging mode for earbuds.
- C) Earbuds can only be charged if the power bank is at 100% capacity.
- D) You must connect the power bank to a wall socket while simultaneously charging your earbuds.
- **Correct Answer:** B
- **Context Document:** `tsg_powerbank_not_charging`
- **Expected Tier:** `economy`
- **Key Points:** Double press the power button to enable low-draw charging mode for earbuds · Check that the capacity display shows active charge · Raise a warranty claim if no output occurs across all ports after pressing

#### Q16 (`t016`)
**Question:** connected my laptop to clearview 27 with type c cable, display works fine but laptop is not charging at all
- A) The ClearView 27 does not support USB-C charging; you must use your laptop's original power adapter.
- B) Check that USB-C power delivery is enabled in the monitor's on-screen menu (off by default in some firmware) and confirm the cable is rated for power delivery up to 90 W / 100 W.
- C) USB-C power delivery only functions when the monitor is connected via DisplayPort simultaneously.
- D) The monitor only charges laptops when the display resolution is set to 1080p 60 Hz.
- **Correct Answer:** B
- **Context Document:** `tsg_monitor_usbc_power`
- **Expected Tier:** `economy`
- **Key Points:** Check that USB-C power delivery is enabled in the monitor's on-screen menu (off by default in some firmware) · Confirm the USB-C cable supports power delivery up to 90 W / 100 W and not video only · ClearView 27 provides up to 90 W over USB-C

---

### 6. `billing_dispute`

#### Q17 (`t017`)
**Question:** i cancelled my pulsebook order 48832 three days ago which was on no-cost emi, why havent i received the refund and why is the emi still showing on my card?
- A) Refund of ₹64,999 takes 5 to 7 business days (due by 7 October 2026); TechStore absorbs the interest discount upfront, but the customer must contact the bank to cancel the EMI plan.
- B) TechStore automatically cancels the bank EMI plan within 24 hours of order cancellation without requiring bank contact.
- C) Orders placed on No-Cost EMI cannot be cancelled once placed.
- D) The full amount was forfeited because No-Cost EMI orders incur a 100% cancellation penalty.
- **Correct Answer:** A
- **Order ID:** `48832`
- **Context Documents:** `bill_emi`, `pol_cancellation`
- **Expected Tier:** `frontier`
- **Key Points:** Refund of ₹64,999 is initiated and scheduled to complete by 7 October 2026 (5 to 7 business days) · TechStore absorbs the interest discount upfront, but the customer must contact the bank to cancel the EMI plan · The bank may still levy interest already accrued prior to cancellation

#### Q18 (`t018`)
**Question:** my credit card that i used to pay was closed by my bank last week. can you please send my return refund to my new bank account instead?
- A) Yes, support can immediately update the destination bank account in the system upon receiving your request.
- B) Refunds must always be initiated to the original payment method; the issuing bank usually routes the credit to your linked account, and if rejected and returned to TechStore, support can arrange a verified bank transfer.
- C) TechStore never processes refunds for closed cards; the funds are automatically converted into non-refundable store credits.
- D) You must reopen your closed credit card with your bank to receive the refund.
- **Correct Answer:** B
- **Context Documents:** `bill_refund_to_closed_card`, `pol_refund_timeline`
- **Expected Tier:** `frontier`
- **Key Points:** Refunds must always be initiated to the original payment method and cannot be redirected directly · The issuing bank usually routes the credit to the customer's linked underlying account · If the bank rejects the credit, funds return to TechStore within 10 business days and support can arrange a bank transfer after ID verification

#### Q19 (`t019`)
**Question:** bought a pulsebook 14 five days ago on techstore and today you dropped the site price by 3000 rs. will you refund me the difference?
- A) No, TechStore policies strictly prohibit any refunds for post-purchase price changes.
- B) Yes, TechStore refunds the price difference if the site price drops within 7 days of purchase upon request (does not apply during flash sales, festive events, or clearance).
- C) TechStore only matches competitor prices, not its own site price drops.
- D) You must return the laptop and place a brand new order at the lower price.
- **Correct Answer:** B
- **Context Document:** `bill_price_drop`
- **Expected Tier:** `frontier`
- **Key Points:** TechStore refunds the price difference if the site price drops within 7 days of purchase · Applies once per order line upon request · Does not apply during flash sales, festive events, or clearance sales

#### Q20 (`t020`)
**Question:** returned my cash on delivery order last week, why havent you refunded to my upi yet? you have my phone number
- A) TechStore automatically initiates refunds to whichever UPI ID is linked to the registered phone number.
- B) COD orders cannot be refunded to UPI automatically; you must submit bank account number and IFSC via support's secure link for a bank transfer taking 5 to 7 business days.
- C) COD orders are only refunded in physical cash via courier visit.
- D) Refunds for COD orders are retained permanently as store coupons.
- **Correct Answer:** B
- **Context Document:** `bill_cod_refund`
- **Expected Tier:** `frontier`
- **Key Points:** COD orders cannot be refunded to UPI automatically because no payment method was used at checkout · Refund is executed via bank transfer after the customer enters account number and IFSC via support's secure link · Transfers take 5 to 7 business days from verification (the ₹49 COD fee is non-refundable after dispatch)

---

### 7. `technical_api`

#### Q21 (`t021`)
**Question:** trying to fetch all orders via GET /v1/orders?offset=100&limit=50 but page 2 still gives the first 50 results. how do we paginate?
- A) You need to pass `page=2` rather than `offset=100`.
- B) Offset-based pagination is not supported; use cursor-based pagination by passing the `next_cursor` value as `?cursor=<cursor>` on subsequent requests (max 100 records/page, expires in 30 minutes).
- C) Increase `limit` to 500, as pagination is disabled by default on production endpoints.
- D) Pass the `X-Pagination-Offset` HTTP header with each request.
- **Correct Answer:** B
- **Context Document:** `api_pagination`
- **Expected Tier:** `frontier`
- **Key Points:** Offset-based pagination is not supported · List endpoints return up to 100 records and a cursor in next_cursor · Pass the opaque cursor value as ?cursor= parameter; cursors expire after 30 minutes

#### Q22 (`t022`)
**Question:** POST /v1/orders is throwing 403 with error body {"code": "insufficient_scope"}. Can I update permissions on my existing bearer token?
- A) Yes, send a PATCH request to `/v1/tokens` with the new scopes required.
- B) No, token scopes cannot be widened or modified once a token is created; a new bearer token must be generated in the partner dashboard with `orders:write` scope.
- C) A 403 insufficient_scope error indicates invalid webhook signature, not missing permissions.
- D) Wait 24 hours for the partner dashboard to automatically synchronize elevated scopes.
- **Correct Answer:** B
- **Context Document:** `api_scopes`
- **Expected Tier:** `frontier`
- **Key Points:** Token scopes cannot be widened or modified once a token is created · A new bearer token must be generated in the partner dashboard with 'orders:write' scope · 403 insufficient_scope indicates authentication succeeded but permissions are lacking

#### Q23 (`t023`)
**Question:** we are seeing a Sunset header in api responses for v1, what does that mean and how long do we have before our integration breaks?
- A) It indicates the endpoint is rate-limited and will recover after midnight IST.
- B) Sunset header indicates the current API version is deprecated; deprecated versions are supported for 12 months after the successor version is announced.
- C) The API token will expire within 30 minutes unless rotated immediately.
- D) The API sandbox is undergoing scheduled nightly maintenance.
- **Correct Answer:** B
- **Context Document:** `api_versioning`
- **Expected Tier:** `frontier`
- **Key Points:** Sunset header indicates the current API version is deprecated · Deprecated versions are supported for 12 months after the successor version is announced · Breaking changes are released under a new URL path version

#### Q24 (`t024`)
**Question:** our POST /v1/shipments calls occasionally hit a 30s timeout. is it safe to immediately retry the call?
- A) Yes, retry immediately in a while-loop without modifying headers.
- B) Server-side timeout occurs at 30 seconds and operation status is uncertain; retry using exponential backoff with jitter and include the identical `Idempotency-Key` header to prevent duplicate operations.
- C) Timeouts guarantee the operation failed completely, so you can safely create a new UUID idempotency key on each retry.
- D) You must cancel the API token and generate a new one before retrying any timed-out request.
- **Correct Answer:** B
- **Context Documents:** `api_timeouts`, `api_idempotency`
- **Expected Tier:** `frontier`
- **Key Points:** Server-side timeout occurs at 30 seconds and does not indicate whether execution completed · POST retries must use the identical Idempotency-Key header to prevent duplicate operations · Retries must implement exponential backoff with jitter instead of immediate loops

---

### 8. `policy_edge_case`

#### Q25 (`t025`)
**Question:** i preordered my headphones 45 days ago and was charged immediately, but package arrived only 10 days back. has my 30 day return window expired?
- A) Yes, the 30-day return window is calculated from the date the payment is captured, so it expired 15 days ago.
- B) No, the 30-day return window starts on the delivery date, not the preorder or charge date; you are eligible since only 10 days have elapsed since delivery (provided hygiene seal is intact).
- C) Pre-ordered items cannot be returned under any circumstances once delivered.
- D) Pre-orders carry a special 60-day return window calculated from the original dispatch estimate.
- **Correct Answer:** B
- **Context Documents:** `pol_preorder`, `pol_return_window`
- **Expected Tier:** `frontier`
- **Key Points:** The 30-day return window starts on the delivery date, not the preorder or charge date · Eligible for return since only 10 days have elapsed since delivery · Item must be returned in original packaging with unbroken seal under hygiene policy

#### Q26 (`t026`)
**Question:** my soundwave earbuds arrived with the box crushed and the earbud casing cracked inside. i opened the plastic seal before seeing the crack, am i denied a replacement because hygiene rules say opened earphones cant be returned?
- A) Yes, breaking the hygiene seal voids all return, replacement, and warranty rights permanently.
- B) No, hygiene return exclusions do not apply to damaged or defective items delivered; report transit damage within 48 hours of delivery with photos for free pickup and immediate replacement.
- C) You must pay a ₹499 inspection fee before TechStore can replace unsealed earbuds.
- D) You can only get store credit equivalent to 50% of the purchase value.
- **Correct Answer:** B
- **Context Documents:** `pol_damaged_in_transit`, `pol_return_exclusions`
- **Expected Tier:** `frontier`
- **Key Points:** Hygiene return exclusions do not apply to damaged or defective items delivered · Report transit damage within 48 hours of delivery with photos of package and product · TechStore arranges a free pickup and immediately dispatches a replacement

#### Q27 (`t027`)
**Question:** our company bought 15 novatab tablets 20 days ago for staff. we want to return 5 of them that are unused in box, can we do that under the 30 day policy?
- A) Yes, all unused products carry a standard 30-day return window regardless of quantity.
- B) No, orders of more than 10 units of a single SKU are treated as business/bulk orders with a 15-day return window, so the request is ineligible after 20 days.
- C) Yes, but business order returns can only be swapped for laptop SKUs.
- D) Business orders cannot be returned under any timeframe once accepted.
- **Correct Answer:** B
- **Context Documents:** `pol_bulk_orders`, `pol_return_window`
- **Expected Tier:** `frontier`
- **Key Points:** Orders of more than 10 units of a single SKU are treated as business/bulk orders · Business orders have a 15-day return window rather than the standard 30-day window · The return request is ineligible because 20 days have passed since delivery

---

### 9. `out_of_scope`

#### Q28 (`t028`)
**Question:** what is the speed of light in kilometers per second
- A) Approximately 299,792 kilometers per second.
- B) Declines; states that it can only help with TechStore orders, products, and support.
- C) The speed of light varies depending on whether you measure it in Bangalore or Delhi.
- D) TechStore does not sell scientific measurement tools.
- **Correct Answer:** B
- **Expected Behavior:** `decline_off_topic`
- **Context Documents:** `[]`
- **Expected Tier:** `economy`
- **Key Points:** Declines; states that it can only help with TechStore orders, products, and support

#### Q29 (`t029`)
**Question:** can i get gift wrapping on my order with a custom birthday card included?
- A) Yes, gift wrapping costs ₹49 and custom greeting cards cost ₹29 at checkout.
- B) Admits unknown; states it does not have information regarding gift wrapping or personalized cards, and offers to connect the customer with a human support agent.
- C) TechStore offers free gift wrapping exclusively for products priced above ₹10,000.
- D) Gift wrapping is available for all orders shipped via BlueDart.
- **Correct Answer:** B
- **Expected Behavior:** `admit_unknown`
- **Context Documents:** `[]`
- **Expected Tier:** `economy`
- **Key Points:** Admits unknown; states it does not have information regarding gift wrapping or personalized cards · Offers to connect the customer with a human support agent

#### Q30 (`t030`)
**Question:** do you sell refrigerators or microwave ovens?
- A) Yes, TechStore stocks select compact refrigerators and microwave ovens online.
- B) States that TechStore does not sell home appliances such as refrigerators, washing machines, or microwaves, and lists that TechStore exclusively sells headphones, laptops, tablets, smartwatches, monitors, and chargers/power banks.
- C) Home appliances are only available at TechStore physical retail showrooms.
- D) Refrigerator orders must be placed through the Partner API only.
- **Correct Answer:** B
- **Expected Behavior:** `answer_from_about`
- **Context Document:** `about_techstore`
- **Expected Tier:** `economy`
- **Key Points:** States that TechStore does not sell home appliances such as refrigerators, washing machines, or microwaves · Lists that TechStore exclusively sells headphones, laptops, tablets, smartwatches, monitors, and chargers/power banks

