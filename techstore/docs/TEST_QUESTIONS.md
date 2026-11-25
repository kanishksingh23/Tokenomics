# TechStore Test Questions (36 Questions)

**Date Grounding:** 30 September 2026  
**Source File:** `techstore/data/questions_test.jsonl`  
**Purpose:** Grounded benchmark test set to evaluate retrieval, cost routing, answer quality, and guardrails across 9 distinct categories.

---

## Overview & Category Distribution

| # | Category | Target | Expected Tier | Description |
|---|:---|:---:|:---|:---|
| 1 | `simple_faq` | 4 | `economy` | Single-fact questions regarding store policies, shipping charges, and services. |
| 2 | `order_status` | 4 | `economy` | Grounded order tracking, delivery status, and return window lookups. |
| 3 | `product_info` | 3 | `economy` | Single-product specifications, compatibility, and physical features. |
| 4 | `product_comparison` | 4 | `economy_escalation` | Comparing two or more products across specs, use-cases, and budgets. |
| 5 | `troubleshooting` | 3 | `economy` | Step-by-step diagnostic and hardware recovery procedures for accessories/monitors. |
| 6 | `billing_dispute` | 5 | `frontier` | Multi-step financial calculations, duplicate authorization holds, and EMI cancellations. |
| 7 | `technical_api` | 5 | `frontier` | Partner developer integration: cursor pagination, token scopes, deprecation headers, and rate limits. |
| 8 | `policy_edge_case` | 4 | `frontier` | Complex intersection of store policies: transit damage vs hygiene seals, bulk orders, and warranty terms. |
| 9 | `out_of_scope` | 4 | `economy` | Off-topic refusals, unknown admissions, catalog boundary checks, and partial answers. |
| | **Total** | **36** | | |

---

## 1. `simple_faq`

### Question 1 (`t001`)
- **Question:** if i cancel an order before it gets shipped do i get the delivery charges back too
- **Options:**
  - **A)** Yes, cancelled orders are refunded in full including any delivery charge paid, within 5 to 7 business days.
  - **B)** No, delivery fees are strictly non-refundable once an order is placed.
  - **C)** Only 50% of the delivery charge is refunded if cancelled within 24 hours.
  - **D)** Delivery charges are refunded only as non-expiring store credit.
- **Correct Answer:** **A**
- **Context Document:** `pol_cancellation`
- **Expected Tier:** `economy`
- **Key Points:**
  1. Cancelled orders are refunded in full including any delivery charges paid
  2. Refund reaches original payment method in 5 to 7 business days
  3. Cancellation is only possible before order is marked Shipped

### Question 2 (`t002`)
- **Question:** how many days does delivery take to tier-2 cities like jaipur?
- **Options:**
  - **A)** 1 to 2 business days.
  - **B)** 2 to 4 business days (excluding Sundays and national holidays).
  - **C)** 5 to 7 business days.
  - **D)** Same-day delivery if ordered before 2 PM.
- **Correct Answer:** **B**
- **Context Document:** `ship_delivery_times`
- **Expected Tier:** `economy`
- **Key Points:**
  1. Tier-2 cities take 2 to 4 business days
  2. Orders placed after 2 PM are processed the next business day
  3. Delivery estimates exclude Sundays and national holidays

### Question 3 (`t003`)
- **Question:** do you guys provide free demo and installation for laptops or is that only for screens?
- **Options:**
  - **A)** Free demo and installation is offered for all laptops and monitors above ₹30,000.
  - **B)** Free installation and demo is only provided for monitors above 27 inches; laptops do not require installation.
  - **C)** Installation is available for laptops for an additional fee of ₹499.
  - **D)** TechStore does not provide installation or demo for any products.
- **Correct Answer:** **B**
- **Context Document:** `ship_installation`
- **Expected Tier:** `economy`
- **Key Points:**
  1. Free installation and demo is only provided for monitors above 27 inches
  2. Laptops, tablets, headphones, and watches do not require installation
  3. Installation request is raised from Orders and scheduled within 48 hours of delivery

### Question 4 (`t004`)
- **Question:** can i check the package in front of delivery guy before accepting it?
- **Options:**
  - **A)** Yes, open-box delivery is available in 22 cities on orders above ₹20,000, where the courier opens the package for inspection before handover.
  - **B)** No, courier rules strictly prohibit opening packages prior to signing delivery acknowledgment.
  - **C)** Open-box delivery is available nationwide on all orders regardless of price.
  - **D)** You can inspect packages only if you pay an additional inspection fee of ₹199 to the delivery agent.
- **Correct Answer:** **A**
- **Context Document:** `ship_open_box`
- **Expected Tier:** `economy`
- **Key Points:**
  1. Open-box delivery is available in 22 cities on orders above ₹20,000
  2. The courier opens the package in the customer's presence for inspection before handover
  3. Refusal at inspection is free and open-box adds 1 business day to the delivery estimate

---

## 2. `order_status`

### Question 5 (`t005`)
- **Question:** can i get tracking details and estimated arrival for order 48821
- **Options:**
  - **A)** Status is Shipped via Ekart with tracking ID EK4449941868, expected delivery date is 3 October 2026.
  - **B)** It is currently Processing at the warehouse and expected to ship on 5 October 2026.
  - **C)** It was Delivered on 28 September 2026 by BlueDart.
  - **D)** It was Cancelled and refunded to your original payment method.
- **Correct Answer:** **A**
- **Order ID:** `48821`
- **Context Document:** `ship_tracking`
- **Expected Tier:** `economy`
- **Key Points:**
  1. Status is Shipped via Ekart with tracking ID EK4449941868
  2. Expected delivery date is 3 October 2026
  3. Contains AuraWatch Pro Smartwatch with Cash on Delivery total of ₹15,999

### Question 6 (`t006`)
- **Question:** i bought a novatab over two weeks back on 15 sep order 48845 and its still processing?? whats going on
- **Options:**
  - **A)** Order 48845 was lost in transit and a replacement has been dispatched.
  - **B)** Order 48845 for NovaTab 11 is in Processing status with an expected delivery date of 6 October 2026; tracking will update upon dispatch.
  - **C)** Order 48845 was cancelled automatically due to a failed net banking verification.
  - **D)** It was already delivered to your registered address on 20 September 2026.
- **Correct Answer:** **B**
- **Order ID:** `48845`
- **Context Document:** `ship_tracking`
- **Expected Tier:** `economy`
- **Key Points:**
  1. Order 48845 is in Processing status for a NovaTab 11
  2. Estimated delivery date is 6 October 2026
  3. Tracking information is sent via email and SMS once dispatched

### Question 7 (`t007`)
- **Question:** showing order 48849 as delivered yesterday but i was not home, which courier dropped it
- **Options:**
  - **A)** It was delivered by BlueDart under tracking ID BD4471920381.
  - **B)** It was marked Delivered on 29 September 2026 by Delhivery under tracking ID EK4426213146.
  - **C)** It was delivered by Ekart under tracking ID DL8830114772.
  - **D)** The courier marked a failed delivery attempt and will reattempt tomorrow.
- **Correct Answer:** **B**
- **Order ID:** `48849`
- **Context Document:** `ship_tracking`
- **Expected Tier:** `economy`
- **Key Points:**
  1. Marked Delivered on 29 September 2026
  2. Delivered by Delhivery under tracking ID EK4426213146
  3. Item delivered was VoltBank 20000mAh Power Bank

### Question 8 (`t008`)
- **Question:** i received order 48835 on 9th september, do i still have time left to return it if i dont want it?
- **Options:**
  - **A)** Yes, 21 days have passed since delivery, so you have until 9 October 2026 within the 30-day return window.
  - **B)** No, TechStore only offers a 15-day return window for tablets.
  - **C)** No, the return window is 30 days from the order placement date (7 September), which has already closed.
  - **D)** Yes, but a 20% restocking fee applies after 14 days of delivery.
- **Correct Answer:** **A**
- **Order ID:** `48835`
- **Context Document:** `pol_return_window`
- **Expected Tier:** `economy`
- **Key Points:**
  1. Eligible for return: 21 days have passed since delivery on 9 September 2026
  2. TechStore allows returns within 30 days of delivery (until 9 October 2026)
  3. Item must be returned in original packaging with all accessories

---

## 3. `product_info`

### Question 9 (`t009`)
- **Question:** does the novatab mini 8 support a pen or stylus for taking notes in college?
- **Options:**
  - **A)** Yes, it includes an active stylus inside the retail box.
  - **B)** Yes, an active stylus can be purchased separately for ₹4,999.
  - **C)** No, stylus support is not available on the NovaTab Mini 8; it is exclusive to the NovaTab 11.
  - **D)** Yes, it supports any standard Bluetooth capacitive stylus without restriction.
- **Correct Answer:** **C**
- **Context Document:** `prod_novatab_mini8`
- **Expected Tier:** `economy`
- **Key Points:**
  1. Stylus is not supported on the NovaTab Mini 8
  2. Stylus support is exclusive to the NovaTab 11

### Question 10 (`t010`)
- **Question:** can i wear the m100 earbuds during workouts or when it rains outside?
- **Options:**
  - **A)** No, the M100 has no water or sweat resistance rating and must be kept completely dry.
  - **B)** Yes, the M100 has an IPX4 splash resistance rating, making it safe for workout sweat and light rain.
  - **C)** Yes, it has an IPX8 waterproof rating and can be submerged while swimming.
  - **D)** It is only splash resistant if purchased with the optional silicone protective sleeve.
- **Correct Answer:** **B**
- **Context Document:** `prod_m100`
- **Expected Tier:** `economy`
- **Key Points:**
  1. M100 has IPX4 splash resistance rating
  2. Safe for sweat during workouts and light rain splashes

### Question 11 (`t011`)
- **Question:** how much power delivery does the 32 inch clearview monitor give over usb c?
- **Options:**
  - **A)** 65 W.
  - **B)** 90 W.
  - **C)** 100 W.
  - **D)** Supplies up to 140 W power delivery over USB-C.
- **Correct Answer:** **D**
- **Context Document:** `prod_clearview32`
- **Expected Tier:** `economy`
- **Key Points:**
  1. Supplies up to 140 W power delivery over USB-C
  2. ClearView 32 Ultra Monitor price is ₹39,999

---

## 4. `product_comparison`

### Question 12 (`t012`)
- **Question:** which voltcharge charger should i get to charge my pulsebook pro 16 at max speed?
- **Options:**
  - **A)** VoltCharge 65W (₹2,499), because 65 W provides maximum speed for all PulseBook models.
  - **B)** VoltCharge 100W (₹3,999), because the PulseBook Pro 16 requires 100 W for full-speed charging.
  - **C)** Either charger charges the Pro 16 at the identical maximum speed.
  - **D)** Neither; the PulseBook Pro 16 can only be charged using a proprietary DC barrel adapter.
- **Correct Answer:** **B**
- **Context Documents:** `prod_voltcharge65`, `prod_voltcharge100`, `prod_pulsebook_pro16`
- **Expected Tier:** `economy_escalation`
- **Key Points:**
  1. VoltCharge 100W (₹3,999) is required for full-speed 100 W charging of PulseBook Pro 16
  2. VoltCharge 65W (₹2,499) is not sufficient to charge the Pro 16 at full speed

### Question 13 (`t013`)
- **Question:** deciding between novatab mini 8 and the 11 inch one, what are the main screen and spec differences for the extra money?
- **Options:**
  - **A)** NovaTab 11 (₹29,999) offers an 11-inch 2.5K 120 Hz display, 8 GB RAM, 256 GB storage, and stylus support, whereas Mini 8 (₹17,999) has an 8.4-inch 90 Hz display, 6 GB RAM, 128 GB storage, and no stylus support.
  - **B)** Both have identical screen sizes, but NovaTab 11 includes an OLED display and 5G cellular connectivity.
  - **C)** NovaTab Mini 8 has a higher refresh rate screen (144 Hz) but smaller storage than the NovaTab 11.
  - **D)** The only difference is screen size; internal processor, RAM, and stylus support are identical.
- **Correct Answer:** **A**
- **Context Documents:** `prod_novatab_mini8`, `prod_novatab11`
- **Expected Tier:** `economy_escalation`
- **Key Points:**
  1. NovaTab 11 (₹29,999) has an 11-inch 2.5K 120 Hz screen, 8 GB RAM, 256 GB storage, and stylus support
  2. NovaTab Mini 8 (₹17,999) has an 8.4-inch 90 Hz screen, 6 GB RAM, 128 GB storage, and lacks stylus support

### Question 14 (`t014`)
- **Question:** are the studio buds pro worth the extra price over m100 if i need active noise cancelling and wireless charging?
- **Options:**
  - **A)** No, both models feature identical active noise cancelling and wireless charging cases.
  - **B)** Yes, Studio Buds Pro (₹6,999) includes 30 dB ANC and a wireless charging case, while M100 (₹3,499) lacks ANC and only has a wired USB-C case.
  - **C)** M100 has active noise cancelling, but lacks wireless charging compared to Studio Buds Pro.
  - **D)** Neither model supports wireless charging, but Studio Buds Pro has noise isolation tips.
- **Correct Answer:** **B**
- **Context Documents:** `prod_m100`, `prod_studiobuds`
- **Expected Tier:** `economy_escalation`
- **Key Points:**
  1. Studio Buds Pro (₹6,999) features 30 dB ANC and a wireless charging case
  2. M100 (₹3,499) has no active noise cancellation and only wired USB-C charging
  3. Studio Buds Pro provides 9 hours battery (32 with case) vs 7 hours (28 with case) for M100

### Question 15 (`t015`)
- **Question:** aurawatch 3 or aurawatch pro, which one is better if i do open water swimming and want longer battery?
- **Options:**
  - **A)** AuraWatch Pro (₹15,999), as it offers 10 ATM water resistance and 18-day battery compared to 5 ATM and 14 days on AuraWatch 3 (₹8,999).
  - **B)** AuraWatch 3 is better for open water swimming because 5 ATM allows diving deeper than 10 ATM.
  - **C)** Both watches have identical 5 ATM water resistance and 14-day battery life.
  - **D)** Neither watch is water resistant; both cannot be used in water.
- **Correct Answer:** **A**
- **Context Documents:** `prod_aurawatch3`, `prod_aurawatch_pro`
- **Expected Tier:** `economy_escalation`
- **Key Points:**
  1. AuraWatch Pro has 10 ATM water resistance vs 5 ATM on AuraWatch 3
  2. AuraWatch Pro offers 18-day battery life vs 14 days on AuraWatch 3
  3. AuraWatch Pro costs ₹15,999 while AuraWatch 3 costs ₹8,999

---

## 5. `troubleshooting`

### Question 16 (`t016`)
- **Question:** plugged my earbud case in after not using it for a couple months and the light isnt turning on at all, is it dead?
- **Options:**
  - **A)** If the LED does not turn on within 5 seconds, the battery is permanently depleted and out of warranty.
  - **B)** A case left fully discharged for over a month may need up to 15 minutes before the LED responds; try a 5 V adapter and claim warranty if no LED lights up after 30 minutes on a known-good charger.
  - **C)** You must hold the pairing button for 60 seconds while plugging it in to jump-start the charging circuit.
  - **D)** The case cannot be charged with a USB-C cable once discharged; you must use a wireless charging pad.
- **Correct Answer:** **B**
- **Context Document:** `tsg_earbuds_case_charge`
- **Expected Tier:** `economy`
- **Key Points:**
  1. Cases uncharged for over a month may require up to 15 minutes before the LED responds
  2. Confirm using a working USB-C cable and 5 V adapter
  3. Raise a warranty claim if no LED lights up after 30 minutes on a known-good charger

### Question 17 (`t017`)
- **Question:** my voltbank has 80% charge but when i plug my wireless earbuds into it they wont charge
- **Options:**
  - **A)** The VoltBank 20000 does not support charging accessories like earbuds under any circumstances.
  - **B)** You need to double press the power button to enable low-draw charging mode for earbuds.
  - **C)** Earbuds can only be charged if the power bank is at 100% capacity.
  - **D)** You must connect the power bank to a wall socket while simultaneously charging your earbuds.
- **Correct Answer:** **B**
- **Context Document:** `tsg_powerbank_not_charging`
- **Expected Tier:** `economy`
- **Key Points:**
  1. Double press the power button to enable low-draw charging mode for earbuds
  2. Check that the capacity display shows active charge
  3. Raise a warranty claim if no output occurs across all ports after pressing

### Question 18 (`t018`)
- **Question:** connected my laptop to clearview 27 with type c cable, display works fine but laptop is not charging at all
- **Options:**
  - **A)** The ClearView 27 does not support USB-C charging; you must use your laptop's original power adapter.
  - **B)** Check that USB-C power delivery is enabled in the monitor's on-screen menu (off by default in some firmware) and confirm the cable is rated for power delivery up to 90 W / 100 W.
  - **C)** USB-C power delivery only functions when the monitor is connected via DisplayPort simultaneously.
  - **D)** The monitor only charges laptops when the display resolution is set to 1080p 60 Hz.
- **Correct Answer:** **B**
- **Context Document:** `tsg_monitor_usbc_power`
- **Expected Tier:** `economy`
- **Key Points:**
  1. Check that USB-C power delivery is enabled in the monitor's on-screen menu (off by default in some firmware)
  2. Confirm the USB-C cable supports power delivery up to 90 W / 100 W and not video only
  3. ClearView 27 provides up to 90 W over USB-C

---

## 6. `billing_dispute`

### Question 19 (`t019`)
- **Question:** i cancelled my pulsebook order 48832 three days ago which was on no-cost emi, why havent i received the refund and why is the emi still showing on my card?
- **Options:**
  - **A)** Refund of ₹64,999 takes 5 to 7 business days (due by 7 October 2026); TechStore absorbs the interest discount upfront, but the customer must contact the bank to cancel the EMI plan.
  - **B)** TechStore automatically cancels the bank EMI plan within 24 hours of order cancellation without requiring bank contact.
  - **C)** Orders placed on No-Cost EMI cannot be cancelled once placed.
  - **D)** The full amount was forfeited because No-Cost EMI orders incur a 100% cancellation penalty.
- **Correct Answer:** **A**
- **Order ID:** `48832`
- **Context Documents:** `bill_emi`, `pol_cancellation`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. Refund of ₹64,999 is initiated and scheduled to complete by 7 October 2026 (5 to 7 business days)
  2. TechStore absorbs the interest discount upfront, but the customer must contact the bank to cancel the EMI plan
  3. The bank may still levy interest already accrued prior to cancellation

### Question 20 (`t020`)
- **Question:** my credit card that i used to pay was closed by my bank last week. can you please send my return refund to my new bank account instead?
- **Options:**
  - **A)** Yes, support can immediately update the destination bank account in the system upon receiving your request.
  - **B)** Refunds must always be initiated to the original payment method; the issuing bank usually routes the credit to your linked account, and if rejected and returned to TechStore, support can arrange a verified bank transfer.
  - **C)** TechStore never processes refunds for closed cards; the funds are automatically converted into non-refundable store credits.
  - **D)** You must reopen your closed credit card with your bank to receive the refund.
- **Correct Answer:** **B**
- **Context Documents:** `bill_refund_to_closed_card`, `pol_refund_timeline`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. Refunds must always be initiated to the original payment method and cannot be redirected directly
  2. The issuing bank usually routes the credit to the customer's linked underlying account
  3. If the bank rejects the credit, funds return to TechStore within 10 business days and support can arrange a bank transfer after ID verification

### Question 21 (`t021`)
- **Question:** bought a pulsebook 14 five days ago on techstore and today you dropped the site price by 3000 rs. will you refund me the difference?
- **Options:**
  - **A)** No, TechStore policies strictly prohibit any refunds for post-purchase price changes.
  - **B)** Yes, TechStore refunds the price difference if the site price drops within 7 days of purchase upon request (does not apply during flash sales, festive events, or clearance).
  - **C)** TechStore only matches competitor prices, not its own site price drops.
  - **D)** You must return the laptop and place a brand new order at the lower price.
- **Correct Answer:** **B**
- **Context Document:** `bill_price_drop`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. TechStore refunds the price difference if the site price drops within 7 days of purchase
  2. Applies once per order line upon request
  3. Does not apply during flash sales, festive events, or clearance sales

### Question 22 (`t022`)
- **Question:** returned my cash on delivery order last week, why havent you refunded to my upi yet? you have my phone number
- **Options:**
  - **A)** TechStore automatically initiates refunds to whichever UPI ID is linked to the registered phone number.
  - **B)** COD orders cannot be refunded to UPI automatically; you must submit bank account number and IFSC via support's secure link for a bank transfer taking 5 to 7 business days.
  - **C)** COD orders are only refunded in physical cash via courier visit.
  - **D)** Refunds for COD orders are retained permanently as store coupons.
- **Correct Answer:** **B**
- **Context Document:** `bill_cod_refund`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. COD orders cannot be refunded to UPI automatically because no payment method was used at checkout
  2. Refund is executed via bank transfer after the customer enters account number and IFSC via support's secure link
  3. Transfers take 5 to 7 business days from verification (the ₹49 COD fee is non-refundable after dispatch)

### Question 23 (`t023`)
- **Question:** i checked my credit card statement for order 48712 and you charged me 12999 three times!! why are there 3 charges and when do i get my money back?
- **Options:**
  - **A)** TechStore created three separate orders for headphones and you must return two of them.
  - **B)** Only one charge of ₹12,999 is settled for order 48712; the other two are duplicate authorizations where one was already released on 29 September and the third will reverse automatically by 4 October 2026.
  - **C)** All three charges are permanent and duplicate charges cannot be reversed on credit cards.
  - **D)** You must file a chargeback with your issuing bank immediately because TechStore cannot release duplicate holds.
- **Correct Answer:** **B**
- **Order ID:** `48712`
- **Context Document:** `bill_duplicate_charge`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. Only one charge of ₹12,999 is settled for the actual order
  2. One duplicate authorization was already released on 29 September 2026
  3. The third hold is pending reversal and reverses automatically by 4 October 2026

---

## 7. `technical_api`

### Question 24 (`t024`)
- **Question:** trying to fetch all orders via GET /v1/orders?offset=100&limit=50 but page 2 still gives the first 50 results. how do we paginate?
- **Options:**
  - **A)** You need to pass `page=2` rather than `offset=100`.
  - **B)** Offset-based pagination is not supported; use cursor-based pagination by passing the `next_cursor` value as `?cursor=<cursor>` on subsequent requests (max 100 records/page, expires in 30 minutes).
  - **C)** Increase `limit` to 500, as pagination is disabled by default on production endpoints.
  - **D)** Pass the `X-Pagination-Offset` HTTP header with each request.
- **Correct Answer:** **B**
- **Context Document:** `api_pagination`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. Offset-based pagination is not supported
  2. List endpoints return up to 100 records and a cursor in next_cursor
  3. Pass the opaque cursor value as ?cursor= parameter; cursors expire after 30 minutes

### Question 25 (`t025`)
- **Question:** POST /v1/orders is throwing 403 with error body {"code": "insufficient_scope"}. Can I update permissions on my existing bearer token?
- **Options:**
  - **A)** Yes, send a PATCH request to `/v1/tokens` with the new scopes required.
  - **B)** No, token scopes cannot be widened or modified once a token is created; a new bearer token must be generated in the partner dashboard with `orders:write` scope.
  - **C)** A 403 insufficient_scope error indicates invalid webhook signature, not missing permissions.
  - **D)** Wait 24 hours for the partner dashboard to automatically synchronize elevated scopes.
- **Correct Answer:** **B**
- **Context Document:** `api_scopes`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. Token scopes cannot be widened or modified once a token is created
  2. A new bearer token must be generated in the partner dashboard with 'orders:write' scope
  3. 403 insufficient_scope indicates authentication succeeded but permissions are lacking

### Question 26 (`t026`)
- **Question:** we are seeing a Sunset header in api responses for v1, what does that mean and how long do we have before our integration breaks?
- **Options:**
  - **A)** It indicates the endpoint is rate-limited and will recover after midnight IST.
  - **B)** Sunset header indicates the current API version is deprecated; deprecated versions are supported for 12 months after the successor version is announced.
  - **C)** The API token will expire within 30 minutes unless rotated immediately.
  - **D)** The API sandbox is undergoing scheduled nightly maintenance.
- **Correct Answer:** **B**
- **Context Document:** `api_versioning`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. Sunset header indicates the current API version is deprecated
  2. Deprecated versions are supported for 12 months after the successor version is announced
  3. Breaking changes are released under a new URL path version

### Question 27 (`t027`)
- **Question:** our POST /v1/shipments calls occasionally hit a 30s timeout. is it safe to immediately retry the call?
- **Options:**
  - **A)** Yes, retry immediately in a while-loop without modifying headers.
  - **B)** Server-side timeout occurs at 30 seconds and operation status is uncertain; retry using exponential backoff with jitter and include the identical `Idempotency-Key` header to prevent duplicate operations.
  - **C)** Timeouts guarantee the operation failed completely, so you can safely create a new UUID idempotency key on each retry.
  - **D)** You must cancel the API token and generate a new one before retrying any timed-out request.
- **Correct Answer:** **B**
- **Context Documents:** `api_timeouts`, `api_idempotency`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. Server-side timeout occurs at 30 seconds and does not indicate whether execution completed
  2. POST retries must use the identical Idempotency-Key header to prevent duplicate operations
  3. Retries must implement exponential backoff with jitter instead of immediate loops

### Question 28 (`t028`)
- **Question:** hitting 429 Too Many Requests on bulk export endpoint after 70 calls in a minute. what are the rate limits and what happens if we keep hitting it?
- **Options:**
  - **A)** Rate limit is 10,000 requests per day across all endpoints; hitting it revokes your API token.
  - **B)** Bulk export endpoints allow 60 requests per minute per token (standard endpoints allow 600/min); exceeding returns 429 with Retry-After header, and sustained violations over 15 minutes trigger a 1-hour block.
  - **C)** Bulk export endpoints have no rate limit in production; 429 indicates invalid authentication credentials.
  - **D)** You must create a new API token for each 50 bulk export calls to bypass rate limiting.
- **Correct Answer:** **B**
- **Context Document:** `api_rate_limits`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. Bulk export limit is 60 requests per minute per token (vs 600/min for standard endpoints)
  2. 429 responses return a Retry-After header in seconds
  3. Sustained violations exceeding 15 minutes trigger a temporary 1-hour block

---

## 8. `policy_edge_case`

### Question 29 (`t029`)
- **Question:** i preordered my headphones 45 days ago and was charged immediately, but package arrived only 10 days back. has my 30 day return window expired?
- **Options:**
  - **A)** Yes, the 30-day return window is calculated from the date the payment is captured, so it expired 15 days ago.
  - **B)** No, the 30-day return window starts on the delivery date, not the preorder or charge date; you are eligible since only 10 days have elapsed since delivery (provided hygiene seal is intact).
  - **C)** Pre-ordered items cannot be returned under any circumstances once delivered.
  - **D)** Pre-orders carry a special 60-day return window calculated from the original dispatch estimate.
- **Correct Answer:** **B**
- **Context Documents:** `pol_preorder`, `pol_return_window`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. The 30-day return window starts on the delivery date, not the preorder or charge date
  2. Eligible for return since only 10 days have elapsed since delivery
  3. Item must be returned in original packaging with unbroken seal under hygiene policy

### Question 30 (`t030`)
- **Question:** my soundwave earbuds arrived with the box crushed and the earbud casing cracked inside. i opened the plastic seal before seeing the crack, am i denied a replacement because hygiene rules say opened earphones cant be returned?
- **Options:**
  - **A)** Yes, breaking the hygiene seal voids all return, replacement, and warranty rights permanently.
  - **B)** No, hygiene return exclusions do not apply to damaged or defective items delivered; report transit damage within 48 hours of delivery with photos for free pickup and immediate replacement.
  - **C)** You must pay a ₹499 inspection fee before TechStore can replace unsealed earbuds.
  - **D)** You can only get store credit equivalent to 50% of the purchase value.
- **Correct Answer:** **B**
- **Context Documents:** `pol_damaged_in_transit`, `pol_return_exclusions`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. Hygiene return exclusions do not apply to damaged or defective items delivered
  2. Report transit damage within 48 hours of delivery with photos of package and product
  3. TechStore arranges a free pickup and immediately dispatches a replacement

### Question 31 (`t031`)
- **Question:** our company bought 15 novatab tablets 20 days ago for staff. we want to return 5 of them that are unused in box, can we do that under the 30 day policy?
- **Options:**
  - **A)** Yes, all unused products carry a standard 30-day return window regardless of quantity.
  - **B)** No, orders of more than 10 units of a single SKU are treated as business/bulk orders with a 15-day return window, so the request is ineligible after 20 days.
  - **C)** Yes, but business order returns can only be swapped for laptop SKUs.
  - **D)** Business orders cannot be returned under any timeframe once accepted.
- **Correct Answer:** **B**
- **Context Documents:** `pol_bulk_orders`, `pol_return_window`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. Orders of more than 10 units of a single SKU are treated as business/bulk orders
  2. Business orders have a 15-day return window rather than the standard 30-day window
  3. The return request is ineligible because 20 days have passed since delivery

### Question 32 (`t032`)
- **Question:** techstore just replaced my smartwatch under warranty when only 2 weeks were left on my 1 year warranty. does my replacement unit get a brand new 1 year warranty?
- **Options:**
  - **A)** Yes, all replacement units receive a brand new full 1-year manufacturer warranty from delivery date.
  - **B)** No, replacements inherit the remaining original warranty, but because fewer than 90 days remained, the replacement gets a 90-day warranty from the replacement date.
  - **C)** No, once a warranty replacement is issued, warranty coverage terminates immediately with 0 days remaining.
  - **D)** Replacements carry a 30-day return window instead of warranty coverage.
- **Correct Answer:** **B**
- **Context Documents:** `pol_replacement_warranty`, `pol_warranty_terms`
- **Expected Tier:** `frontier`
- **Key Points:**
  1. Replacements inherit the remaining warranty of the original unit rather than starting a fresh 1-year term
  2. If fewer than 90 days remain, the replacement receives a 90-day warranty from replacement date
  3. Replacement units may be factory refurbished and functionally equivalent

---

## 9. `out_of_scope`

### Question 33 (`t033`)
- **Question:** what is the speed of light in kilometers per second
- **Options:**
  - **A)** Approximately 299,792 kilometers per second.
  - **B)** Declines; states that it can only help with TechStore orders, products, and support.
  - **C)** The speed of light varies depending on whether you measure it in Bangalore or Delhi.
  - **D)** TechStore does not sell scientific measurement tools.
- **Correct Answer:** **B**
- **Context Documents:** `[]`
- **Expected Tier:** `economy`
- **Expected Behavior:** `decline_off_topic`
- **Key Points:**
  1. Declines; states that it can only help with TechStore orders, products, and support

### Question 34 (`t034`)
- **Question:** can i get gift wrapping on my order with a custom birthday card included?
- **Options:**
  - **A)** Yes, gift wrapping costs ₹49 and custom greeting cards cost ₹29 at checkout.
  - **B)** Admits unknown; states it does not have information regarding gift wrapping or personalized cards, and offers to connect the customer with a human support agent.
  - **C)** TechStore offers free gift wrapping exclusively for products priced above ₹10,000.
  - **D)** Gift wrapping is available for all orders shipped via BlueDart.
- **Correct Answer:** **B**
- **Context Documents:** `[]`
- **Expected Tier:** `economy`
- **Expected Behavior:** `admit_unknown`
- **Key Points:**
  1. Admits unknown; states it does not have information regarding gift wrapping or personalized cards
  2. Offers to connect the customer with a human support agent

### Question 35 (`t035`)
- **Question:** do you sell refrigerators or microwave ovens?
- **Options:**
  - **A)** Yes, TechStore stocks select compact refrigerators and microwave ovens online.
  - **B)** States that TechStore does not sell home appliances such as refrigerators, washing machines, or microwaves, and lists that TechStore exclusively sells headphones, laptops, tablets, smartwatches, monitors, and chargers/power banks.
  - **C)** Home appliances are only available at TechStore physical retail showrooms.
  - **D)** Refrigerator orders must be placed through the Partner API only.
- **Correct Answer:** **B**
- **Context Document:** `about_techstore`
- **Expected Tier:** `economy`
- **Expected Behavior:** `answer_from_about`
- **Key Points:**
  1. States that TechStore does not sell home appliances such as refrigerators, washing machines, or microwaves
  2. Lists that TechStore exclusively sells headphones, laptops, tablets, smartwatches, monitors, and chargers/power banks

### Question 36 (`t036`)
- **Question:** what colors are available for the soundwave x200 and can i get custom name engraving on the headband?
- **Options:**
  - **A)** SoundWave X200 is available in Midnight Black and Arctic White (₹12,999); custom engraving is not mentioned in documentation, so support must admit unknown regarding custom engraving and connect to an agent.
  - **B)** X200 comes only in Space Gray; laser engraving is available for ₹499.
  - **C)** X200 comes in six colors and includes free custom engraving on all preorders.
  - **D)** Custom engraving is only offered on the Y500 headphones.
- **Correct Answer:** **A**
- **Context Document:** `prod_x200`
- **Expected Tier:** `economy`
- **Expected Behavior:** `partial`
- **Key Points:**
  1. Answers that SoundWave X200 is available in Midnight Black and Arctic White
  2. Admits unknown or offers support contact regarding custom name engraving
