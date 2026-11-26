# TechStore Repeat-Traffic Variants (36 Questions)

**Source File:** `techstore/data/questions_repeat.jsonl`  
**Original Set:** `techstore/data/questions_test.jsonl` (12 non-`order_status` questions × 3 variants)  
**Purpose:** Evaluate answer-cache **saving** (24 `same` paraphrases that should hit the cache) and **safety** (12 `different` look-alike questions that must *not* reuse the cached answer).

---

## Overview

| Group | Original ID | Category | Variants | `same` | `different` |
|---:|:---|:---|:---|:---:|:---:|
| 1 | `t002` | `simple_faq` | `r001`–`r003` | 2 | 1 |
| 2 | `t003` | `simple_faq` | `r004`–`r006` | 2 | 1 |
| 3 | `t011` | `product_info` | `r007`–`r009` | 2 | 1 |
| 4 | `t012` | `product_comparison` | `r010`–`r012` | 2 | 1 |
| 5 | `t013` | `product_comparison` | `r013`–`r015` | 2 | 1 |
| 6 | `t015` | `product_comparison` | `r016`–`r018` | 2 | 1 |
| 7 | `t018` | `troubleshooting` | `r019`–`r021` | 2 | 1 |
| 8 | `t021` | `billing_dispute` | `r022`–`r024` | 2 | 1 |
| 9 | `t027` | `technical_api` | `r025`–`r027` | 2 | 1 |
| 10 | `t029` | `policy_edge_case` | `r028`–`r030` | 2 | 1 |
| 11 | `t031` | `policy_edge_case` | `r031`–`r033` | 2 | 1 |
| 12 | `t032` | `policy_edge_case` | `r034`–`r036` | 2 | 1 |
| | **Total** | | **36 variants** | **24** | **12** |

---

## 1. `t002` (`simple_faq` · `ship_delivery_times`)

> **Original (`t002`):** how many days does delivery take to tier-2 cities like jaipur?

1. **`r001` (`same`):** whats the shipping timeline for tier-2 towns such as jaipur
2. **`r002` (`same`):** how long will delivery take if i order to a tier 2 city like jaipur
3. **`r003` (`different`):** how many days does delivery take to remote north eastern pin codes  
   *Why different:* Tier-2 cities take 2–4 business days; remote and north-eastern pin codes take 5–7 business days.

---

## 2. `t003` (`simple_faq` · `ship_installation`)

> **Original (`t003`):** do you guys provide free demo and installation for laptops or is that only for screens?

4. **`r004` (`same`):** is free setup and demo available for laptops too or just monitors
5. **`r005` (`same`):** do you send someone for free installation of laptops as well or only displays
6. **`r006` (`different`):** do you guys provide free demo and installation for all monitors including 27 inch ones?  
   *Why different:* Free installation and demo is included only for monitors *above* 27 inches (ClearView 32), not 27-inch monitors.

---

## 3. `t011` (`product_info` · `prod_clearview32`)

> **Original (`t011`):** how much power delivery does the 32 inch clearview monitor give over usb c?

7. **`r007` (`same`):** whats the usb-c charging wattage on the 32 inch clearview display
8. **`r008` (`same`):** how many watts of power output can the 32 inch clearview deliver through usb c
9. **`r009` (`different`):** how much power delivery does the 27 inch clearview monitor give over usb c?  
   *Why different:* ClearView 32 supplies 140 W over USB-C; ClearView 27 supplies 90 W.

---

## 4. `t012` (`product_comparison` · `prod_voltcharge65`, `prod_voltcharge100`, `prod_pulsebook_pro16`)

> **Original (`t012`):** which voltcharge charger should i get to charge my pulsebook pro 16 at max speed?

10. **`r010` (`same`):** which voltcharge adapter do i need for full speed charging on the pulsebook pro 16
11. **`r011` (`same`):** to charge a pulsebook pro 16 at fastest speed which voltcharge model should i buy
12. **`r012` (`different`):** which voltcharge charger should i get to charge my pulsebook 14 at max speed?  
    *Why different:* PulseBook Pro 16 requires the 100 W VoltCharge (₹3,999); PulseBook 14 charges at 65 W, so the VoltCharge 65W (₹2,499) is sufficient.

---

## 5. `t013` (`product_comparison` · `prod_novatab_mini8`, `prod_novatab11`)

> **Original (`t013`):** deciding between novatab mini 8 and the 11 inch one, what are the main screen and spec differences for the extra money?

13. **`r013` (`same`):** comparing novatab mini 8 with the 11 inch model, what extra screen and hardware specs do i get for the higher price
14. **`r014` (`same`):** whats different in display and specs between novatab mini 8 and the 11 inch tablet to justify the cost
15. **`r015` (`different`):** deciding between novatab mini 8 and the 11 inch one, which one comes with a free stylus inside the box?  
    *Why different:* Neither tablet includes a stylus in the box (NovaTab 11 supports a stylus sold separately; NovaTab Mini 8 does not support a stylus).

---

## 6. `t015` (`product_comparison` · `prod_aurawatch3`, `prod_aurawatch_pro`)

> **Original (`t015`):** aurawatch 3 or aurawatch pro, which one is better if i do open water swimming and want longer battery?

16. **`r016` (`same`):** for open water swimming and better battery life should i pick aurawatch 3 or the pro
17. **`r017` (`same`):** between aurawatch 3 and aurawatch pro which handles open water swims and lasts longer on a charge
18. **`r018` (`different`):** aurawatch 3 or aurawatch pro, which one works with an iphone running ios 14?  
    *Why different:* AuraWatch 3 is compatible with iOS 14 and above, whereas AuraWatch Pro requires iOS 15 and above.

---

## 7. `t018` (`troubleshooting` · `tsg_monitor_usbc_power`)

> **Original (`t018`):** connected my laptop to clearview 27 with type c cable, display works fine but laptop is not charging at all

19. **`r019` (`same`):** plugged my laptop into the clearview 27 over usb-c, video shows up fine but there is no charging
20. **`r020` (`same`):** my laptop screen mirrors onto clearview 27 via type-c cable, why isnt it getting power
21. **`r021` (`different`):** connected my laptop to clearview 27 with hdmi cable, display works fine but laptop is not charging at all  
    *Why different:* HDMI does not deliver USB-C power; charging from ClearView 27 requires a power-delivery-rated USB-C cable with USB-C PD enabled.

---

## 8. `t021` (`billing_dispute` · `bill_price_drop`)

> **Original (`t021`):** bought a pulsebook 14 five days ago on techstore and today you dropped the site price by 3000 rs. will you refund me the difference?

22. **`r022` (`same`):** ordered a pulsebook 14 on your site five days back and now its listed 3000 rupees cheaper, can i claim the difference
23. **`r023` (`same`):** purchased the pulsebook 14 five days ago and today the techstore price went down by rs 3000, do i get a refund for the drop
24. **`r024` (`different`):** bought a pulsebook 14 ten days ago on techstore and today you dropped the site price by 3000 rs. will you refund me the difference?  
    *Why different:* Price-drop refunds only apply within 7 days of purchase, so 10 days is outside the window.

---

## 9. `t027` (`technical_api` · `api_timeouts`, `api_idempotency`)

> **Original (`t027`):** our POST /v1/shipments calls occasionally hit a 30s timeout. is it safe to immediately retry the call?

25. **`r025` (`same`):** getting sporadic 30s timeouts on POST /v1/shipments, can our client retry right away without risk
26. **`r026` (`same`):** some POST /v1/shipments requests time out after 30s, is an immediate retry safe to do
27. **`r027` (`different`):** our GET /v1/shipments calls occasionally hit a 30s timeout. is it safe to retry without an idempotency key?  
    *Why different:* `POST` requires the same `Idempotency-Key` header on retry to avoid duplicate resources; `GET` is idempotent by design and does not need an idempotency key.

---

## 10. `t029` (`policy_edge_case` · `pol_preorder`, `pol_return_window`)

> **Original (`t029`):** i preordered my headphones 45 days ago and was charged immediately, but package arrived only 10 days back. has my 30 day return window expired?

28. **`r028` (`same`):** pre-ordered headphones 45 days back and got billed right away, delivered just 10 days ago — is the 30 day return period over
29. **`r029` (`same`):** my preorder was placed and charged 45 days ago but reached me 10 days ago, am i already past the 30 day return limit
30. **`r030` (`different`):** i preordered my headphones 45 days ago and was charged immediately, package arrived 35 days back. has my 30 day return window expired?  
    *Why different:* The 30-day return window starts at delivery—10 days is eligible (if unopened), whereas 35 days after delivery is expired.

---

## 11. `t031` (`policy_edge_case` · `pol_bulk_orders`, `pol_return_window`)

> **Original (`t031`):** our company bought 15 novatab tablets 20 days ago for staff. we want to return 5 of them that are unused in box, can we do that under the 30 day policy?

31. **`r031` (`same`):** we ordered 15 novatab units for our office 20 days back and need to return 5 unopened ones, does the 30 day return rule cover us
32. **`r032` (`same`):** bought 15 novatabs for company staff 20 days ago, can we send back 5 sealed boxes using the 30 day return window
33. **`r033` (`different`):** our company bought 8 novatab tablets 20 days ago for staff. we want to return 5 of them that are unused in box, can we do that under the 30 day policy?  
    *Why different:* Orders above 10 units of a single SKU are business orders with a 15-day return window (ineligible at 20 days); an 8-unit order gets the standard 30-day return window.

---

## 12. `t032` (`policy_edge_case` · `pol_replacement_warranty`, `pol_warranty_terms`)

> **Original (`t032`):** techstore just replaced my smartwatch under warranty when only 2 weeks were left on my 1 year warranty. does my replacement unit get a brand new 1 year warranty?

34. **`r034` (`same`):** got a warranty replacement smartwatch with just 2 weeks remaining on the original 1 year cover, does the new unit restart a full 1 year warranty
35. **`r035` (`same`):** my watch was replaced under warranty when 2 weeks were left out of 1 year — will the replacement have a fresh 1 year warranty
36. **`r036` (`different`):** techstore just replaced my smartwatch under warranty when 6 months were left on my 1 year warranty. does my replacement unit get a 90-day warranty or 6 months?  
    *Why different:* With 2 weeks (<90 days) remaining, the replacement gets the 90-day floor; with 6 months (>90 days) remaining, it inherits the remaining 6 months.
