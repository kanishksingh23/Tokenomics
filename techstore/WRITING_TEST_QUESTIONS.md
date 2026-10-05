# Writing the TechStore Test Questions

A guide for writing the **200 test questions** in `data/questions_test.jsonl`. Read it once fully before starting; after that, the checklists and the appendices are what you will keep coming back to.

## Why this set matters

Every fix we made in Phase 0 — document wording, search rules, the prompt — was made after looking at the 50 seed questions, so the system is now fitted to them. On 14 questions written later, keyword search found the right document only 8 times out of 14, while it had looked best on the seeds. **The test set is how we find out how the system does on questions it has never seen.** It is what the router's final cost and quality claims are measured on.

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
| `simple_faq` | 24 | economy | One fact about a policy, delivery, payment or account |
| `order_status` | 24 | economy | About one specific order, by its order number |
| `product_info` | 16 | economy | One fact about one product |
| `product_comparison` | 20 | economy_escalation | Choosing between products, or "which one is best for…" |
| `troubleshooting` | 20 | economy | Something the customer owns isn't working |
| `billing_dispute` | 28 | frontier | A problem with money: charges, refunds, EMI, invoices |
| `technical_api` | 28 | frontier | A developer using the TechStore Partner API |
| `policy_edge_case` | 24 | frontier | Two rules collide, or a rule meets an unusual situation |
| `out_of_scope` | 16 | economy | The documents can't or shouldn't answer it |
| **Total** | **200** | | |

**Expected tier** is your judgement of which model a well-built router *should* pick:
- `economy` — a cheap model can answer it from one document.
- `economy_escalation` — a cheap model will probably try, but may need the expensive one (comparisons often do).
- `frontier` — needs the expensive model: several documents, arithmetic, code, or careful reasoning.

When unsure, use the table's default for the category.

### 1. `simple_faq` — 24 questions
One fact, one document. Policies (`pol_…`), shipping (`ship_…`), payment (`bill_payment_methods`), account (`acc_…`).

```
"if i order now can it come tomorrow?"
   docs: ship_charges
   key points: express next-day delivery costs ₹149 · metro cities only · order before 2 PM

"is there an extra fee if i pay cash on delivery"
   docs: bill_payment_methods
   key points: ₹49 handling fee · refunded if the order is cancelled before dispatch
```

### 2. `order_status` — 24 questions
About one real order. **Use an order number from [Appendix B](#appendix-b-the-40-orders)** and put it in `order_ids`. Vary the status (processing, shipped, delivered, cancelled, returned), and remember the store's date.

```
"48390 still says processing, when does it ship??"
   orders: 48390 · docs: ship_tracking
   key points: status is Processing · expected 2 October 2026 · tracking link sent by email and SMS once shipped
```

### 3. `product_info` — 16 questions
One fact about one product (`prod_…`). Name the product the way a customer would ("the voltbank", "pulsebook air").

```
"can i take the voltbank on a plane"
   docs: prod_voltbank20k
   key points: capacity is under 100 Wh · check the airline's rules before flying

"how heavy is the pulsebook air"
   docs: prod_pulsebook_air13
   key points: 1.12 kg
```

### 4. `product_comparison` — 20 questions
Choosing between products, or asking for the best one for a purpose. List **every product page needed** in `context_ids` (not `catalogue_summary`). Include some that name a category instead of products ("your cheapest laptop"), and some with a budget.

```
"cheapest laptop you have thats fine for coding?"
   docs: prod_pulsebook_air13, prod_pulsebook14, prod_pulsebook_pro16
   key points: PulseBook Air 13 is the cheapest at ₹44,999 · it has 8 GB RAM

"aurawatch 3 or the pro if i swim a lot"
   docs: prod_aurawatch3, prod_aurawatch_pro
   key points: AuraWatch 3 is rated 5 ATM · AuraWatch Pro is rated 10 ATM
```

### 5. `troubleshooting` — 20 questions
Something the customer owns isn't working. Mostly `tsg_…` documents; add `pol_warranty_terms` when the honest answer is "this is a warranty defect".

```
"my studio buds only play in the left ear"
   docs: tsg_earbuds_one_side
   key points: put both buds in the case for 10 seconds · reset by holding both touch panels for 15 seconds · clean the charging contacts
```

### 6. `billing_dispute` — 28 questions
Money. These need the most care: several documents, often an order record, often arithmetic. Order **48712** has three charges (one payment, two duplicate holds); most other orders have one.

```
"paid half with a gift card and half on UPI, returned it, where does my money go"
   docs: bill_gift_card, pol_refund_timeline
   key points: gift-card portion comes back as store credit · the rest goes back to UPI
```

### 7. `technical_api` — 28 questions
A developer integrating with the Partner API (`api_…`): error codes, webhooks, tokens, retries, pagination. You don't need to understand the code; the documents say what the right answer is. Developers write tersely and paste error messages.

```
"our webhook endpoint stopped getting events, did you turn it off?"
   docs: api_webhook_retries
   key points: failed deliveries retry at 1, 5, 25 and 125 minutes · then the endpoint is marked unhealthy and paused until reactivated

"inventory endpoint says 5 in stock but creating the order fails with 422"
   docs: api_inventory
   key points: stock figures can lag up to 60 seconds · handle 422 out_of_stock on order creation
```

### 8. `policy_edge_case` — 24 questions
Two rules meet, or a rule meets an unusual case. Usually 2–3 documents. The best ones make the customer's situation sound reasonable while the rules point the other way.

```
"preordered the y500 and the date keeps moving, its 3 weeks late now. can i cancel and get all my money back?"
   docs: pol_preorder
   key points: a delay of more than 14 days allows cancelling for a full refund

"need 12 monitors for our office, do we still get 30 days to return them?"
   docs: pol_bulk_orders
   key points: more than 10 units is a business order · business orders have a 15-day return window · a GSTIN is required
```

### 9. `out_of_scope` — 16 questions
Questions the documents can't or shouldn't answer. Each needs an `expected_behavior`:

| `expected_behavior` | Count | Meaning | Example |
|:---|---:|:---|:---|
| `decline_off_topic` | 4 | Nothing to do with TechStore; must decline even if the model knows the answer | *"whats the weather in delhi today"* |
| `admit_unknown` | 6 | About TechStore, but not in the documents; must say so, never invent | *"do you take my old laptop in exchange"* |
| `answer_from_about` | 3 | Answered by the About TechStore document (`about_techstore`) | *"do you sell gaming consoles"* |
| `partial` | 3 | Half answerable, half not | *"what colours does the x200 come in and can you engrave it"* |

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

Aim for no persona or type above about a third of any category.

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

Each question is **one line** in `data/questions_test.jsonl`. Ids run `t001` to `t200`.

```json
{"id": "t001", "category": "simple_faq", "question": "if i order now can it come tomorrow?", "context_ids": ["ship_charges"], "expected_tier": "economy", "key_points": ["Express next-day delivery costs ₹149", "Metro cities only, order before 2 PM"], "source": "human"}
{"id": "t025", "category": "order_status", "question": "48390 still says processing, when does it ship??", "context_ids": ["ship_tracking"], "order_ids": ["48390"], "expected_tier": "economy", "key_points": ["Status is Processing", "Expected 2 October 2026", "Tracking link sent by email and SMS once shipped"], "source": "human"}
{"id": "t185", "category": "out_of_scope", "question": "whats the weather in delhi today", "context_ids": [], "expected_tier": "economy", "expected_behavior": "decline_off_topic", "key_points": ["Declines; says it only helps with TechStore orders, products and support"], "source": "human"}
```

| Field | Required | Notes |
|:---|:---|:---|
| `id` | yes | `t001` … `t200` |
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

1. **Write in batches, one category at a time**, about 20 questions per sitting. Roughly 3–4 minutes each: about 12 hours for all 200, or 6 each if Kanishk writes half.
2. After each batch, run:
   ```bash
   python validate_data.py
   ```
   It shows progress per category and names any problem: an unknown document or order id, a missing field, a duplicate.
3. **Spot-check**: Kanishk reads 20 random questions against the documents and their key points.
4. **Freeze**, once all 200 are in and validation passes:
   ```bash
   python validate_data.py --freeze
   ```
   This writes `questions_test.sha256`. Commit both files. From then on, any edit to the test set fails validation.

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
