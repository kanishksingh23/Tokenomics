# Answers to grade

Grade each answer ONLY against the evidence shown with it. Store date: 30 September 2026.
Verdicts: correct / partial / wrong / hallucinated (rubric: Tokenomics.md §7, Grading Rubric).


========== q001 [simple_faq] ==========
QUESTION: How long do I have to return something?
NEEDED DOCS: ['pol_return_window']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
You have **30 days from the delivery date shown on tracking**, not the order date, to return an item under the “30-day return window.” Returns raised on day 31 or later are automatically rejected.

Include the original packaging and all accessories, manuals, and free gifts.

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_return_window] Return Window
TechStore accepts returns within 30 days of delivery. The 30 days are counted from the delivery date shown on the tracking record, not the order date. Items must be returned in their original packaging with all accessories, manuals and free gifts included. A return raised on day 31 or later is rejected automatically by the returns system.
--- [pol_refund_timeline] Refund Processing Time
Once a returned item is received and inspected at our warehouse, refunds are initiated within 2 business days. The money reaches the original payment method in 5 to 7 business days for cards and UPI, and up to 10 business days for net banking. Refunds are always issued to the original payment method; we cannot redirect a refund to a different card or account.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [ship_failed_delivery] Failed Delivery Attempts
The courier makes three delivery attempts on consecutive business days. After the third failed attempt the parcel is returned to our warehouse and the order is refunded in full, including any delivery charge paid, within 7 business days of the parcel being received back. A customer can reschedule delivery once through the tracking link.

========== q002 [simple_faq] ==========
QUESTION: Is delivery free?
NEEDED DOCS: ['ship_charges']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Delivery is free on “all orders above ₹999.” Below ₹999, a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149.

EVIDENCE THE MODEL WAS GIVEN:
--- [ship_charges] Delivery Charges
Delivery is free on all orders above ₹999. Below that a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149 and is available in metro cities only for orders placed before 2 PM. Delivery charges are refunded if the order is cancelled before shipping or if the item arrives damaged.
--- [ship_open_box] Open-Box Delivery
Open-box delivery is available in 22 cities on orders above ₹20,000. The courier opens the package in the customer's presence for inspection before handover. Refusal at open-box inspection is free and refunds process within 5 to 7 business days. Open-box delivery adds 1 business day to the estimate.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.

========== q006 [order_status] ==========
QUESTION: Where is my order #48213?
NEEDED DOCS: ['ship_tracking']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Your order #48213 is **Shipped** via BlueDart and is due today, **30 September 2026**.

- **Item:** SoundWave X200 Wireless Headphones
- **Tracking ID:** BD4471920381

You can check tracking under **Orders** in your account or through the link sent by email and SMS.

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [ship_tracking] Tracking an Order
A tracking link is emailed and sent by SMS when the order is marked Shipped. Tracking can also be seen under Orders in the account. Tracking information can take up to 12 hours after dispatch to become active with the courier. If tracking has not updated for more than 48 hours, contact support so a courier trace can be raised.
--- [pol_bulk_orders] Bulk and Business Orders
Orders above 10 units of a single SKU are treated as business orders and require a GSTIN. Bulk pricing is quoted by the business desk and is not available at checkout. Business orders ship in 5 to 10 business days and carry a 15-day return window rather than 30 days.
--- [svc_centres] Service Centre Network
TechStore operates authorised service centres in 48 Indian cities. The nearest centre can be found by pin code on the Support page. Walk-in service is available for laptops and monitors; headphones, watches and tablets are handled by courier pickup only. Carry the invoice or order ID for any walk-in visit.
--- ORDER 48213
{"order_id": "48213", "customer_id": "cust_1042", "email": "anita.r@example.com", "placed_at": "2026-09-14", "status": "Shipped", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "UPI", "delivery_pin": "560034", "courier": "BlueDart", "tracking_id": "BD4471920381", "eta": "2026-09-30", "charges": [{"date": "2026-09-14", "amount": 12999, "type": "capture", "status": "settled"}]}

========== q008 [order_status] ==========
QUESTION: When will order 48677 arrive?
NEEDED DOCS: ['ship_delivery_times']   MISSING FROM WHAT THE MODEL SAW: ['ship_delivery_times']

ANSWER:
Your order #48677 is due today, 30 September 2026. It has shipped via BlueDart; tracking ID: BD4473001199.

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [ship_tracking] Tracking an Order
A tracking link is emailed and sent by SMS when the order is marked Shipped. Tracking can also be seen under Orders in the account. Tracking information can take up to 12 hours after dispatch to become active with the courier. If tracking has not updated for more than 48 hours, contact support so a courier trace can be raised.
--- [pol_preorder] Pre-Orders
Pre-ordered items are charged at the time of order, not at dispatch. The estimated dispatch date on the product page is indicative; if it slips by more than 14 days the customer may cancel for a full refund. The 30-day return window begins at delivery, not at the order date.
--- [pol_bulk_orders] Bulk and Business Orders
Orders above 10 units of a single SKU are treated as business orders and require a GSTIN. Bulk pricing is quoted by the business desk and is not available at checkout. Business orders ship in 5 to 10 business days and carry a 15-day return window rather than 30 days.
--- ORDER 48677
{"order_id": "48677", "customer_id": "cust_6001", "email": "sameer.j@example.com", "placed_at": "2026-09-26", "status": "Shipped", "items": [{"sku": "prod_aurawatch3", "name": "AuraWatch 3 Smartwatch", "qty": 1, "unit_price": 8999}, {"sku": "prod_voltcharge65", "name": "VoltCharge 65W GaN Charger", "qty": 1, "unit_price": 2499}], "total": 11498, "payment_method": "UPI", "delivery_pin": "411014", "courier": "BlueDart", "tracking_id": "BD4473001199", "eta": "2026-09-30", "charges": [{"date": "2026-09-26", "amount": 11498, "type": "capture", "status": "settled"}]}

========== q009 [order_status] ==========
QUESTION: I cancelled order 48455, when do I get my refund?
NEEDED DOCS: ['pol_refund_timeline']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Your ₹2,499 refund for order #48455 has been initiated and is expected in your original UPI payment method by **1 October 2026**.

Cancelled orders are refunded within “5 to 7 business days.”

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_cancellation] Order Cancellation
An order can be cancelled free of charge at any time before it is marked Shipped. Once shipped, cancellation is not possible; the customer should refuse delivery or raise a return after delivery. Cancelled orders are refunded in full, including any delivery charge paid, within 5 to 7 business days.
--- [bill_cod_refund] Refunds on Cash-on-Delivery Orders
Cash-on-delivery orders cannot be refunded to a payment method because none was used. Refunds are made by bank transfer after the customer submits account number and IFSC through the secure link sent by support. Transfers complete within 5 to 7 business days of verification. The ₹49 COD handling fee is refunded only if the order is cancelled before dispatch.
--- [pol_refund_timeline] Refund Processing Time
Once a returned item is received and inspected at our warehouse, refunds are initiated within 2 business days. The money reaches the original payment method in 5 to 7 business days for cards and UPI, and up to 10 business days for net banking. Refunds are always issued to the original payment method; we cannot redirect a refund to a different card or account.
--- [ship_failed_delivery] Failed Delivery Attempts
The courier makes three delivery attempts on consecutive business days. After the third failed attempt the parcel is returned to our warehouse and the order is refunded in full, including any delivery charge paid, within 7 business days of the parcel being received back. A customer can reschedule delivery once through the tracking link.
--- ORDER 48455
{"order_id": "48455", "customer_id": "cust_1042", "email": "anita.r@example.com", "placed_at": "2026-09-22", "status": "Cancelled", "items": [{"sku": "prod_voltcharge65", "name": "VoltCharge 65W GaN Charger", "qty": 1, "unit_price": 2499}], "total": 2499, "payment_method": "UPI", "delivery_pin": "560034", "courier": null, "tracking_id": null, "cancelled_at": "2026-09-22", "charges": [{"date": "2026-09-22", "amount": 2499, "type": "capture", "status": "refund_initiated", "refund_eta": "2026-10-01"}]}

========== q010 [order_status] ==========
QUESTION: What did I order in 48501?
NEEDED DOCS: []   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
You ordered 1 SoundWave Y500 Premium Headphones for ₹24,999 in order #48501.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_clearview32] ClearView 32 Ultra Monitor
32-inch monitor. Price ₹39,999. 4K UHD IPS Black panel, 165 Hz refresh, 1 ms response, 99 percent DCI-P3, HDR600, USB-C with 140 W power delivery, built-in KVM switch, height and pivot adjustable stand, VESA 100. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.
--- [prod_clearview27] ClearView 27 Monitor
27-inch monitor. Price ₹22,999. 4K UHD IPS panel, 144 Hz refresh, 1 ms response, 95 percent DCI-P3 colour coverage, USB-C with 90 W power delivery, height and pivot adjustable stand, VESA 100 mount. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- ORDER 48501
{"order_id": "48501", "customer_id": "cust_4420", "email": "rahul.k@example.com", "placed_at": "2026-09-23", "status": "Delivered", "items": [{"sku": "prod_y500", "name": "SoundWave Y500 Premium Headphones", "qty": 1, "unit_price": 24999}], "total": 24999, "payment_method": "Credit Card", "delivery_pin": "500081", "courier": "BlueDart", "tracking_id": "BD4472881003", "delivered_at": "2026-09-26", "charges": [{"date": "2026-09-23", "amount": 24999, "type": "capture", "status": "settled"}]}

========== q014 [product_info] ==========
QUESTION: Does the ClearView 27 support USB-C?
NEEDED DOCS: ['prod_clearview27']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Yes, the ClearView 27 supports USB-C with 90 W power delivery.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_clearview27] ClearView 27 Monitor
27-inch monitor. Price ₹22,999. 4K UHD IPS panel, 144 Hz refresh, 1 ms response, 95 percent DCI-P3 colour coverage, USB-C with 90 W power delivery, height and pivot adjustable stand, VESA 100 mount. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.
--- [tsg_monitor_usbc_power] Monitor Not Charging Laptop over USB-C
The ClearView 27 supplies 90 W and the ClearView 32 Ultra supplies 140 W over USB-C. A PulseBook Pro 16 drawing 100 W will charge slowly from a ClearView 27 under sustained load. Confirm the cable is rated for both video and 100 W power delivery; many are not. Verify USB-C power delivery is enabled in the monitor menu, as it is off by default on some firmware.
--- [tsg_monitor_no_signal] Monitor Shows No Signal
If ClearView 27 reports no signal: 1) Confirm the input source matches the cable used, selectable in the on-screen menu. 2) For USB-C, confirm the laptop port supports DisplayPort Alt Mode; the PulseBook USB-A port does not. 3) Try a different cable, as many USB-C cables carry power but not video. 4) At 4K 144 Hz use DisplayPort 1.4 or HDMI 2.1; older cables cap the refresh rate. 5) Reset the monitor to factory defaults from the menu.
--- [prod_clearview32] ClearView 32 Ultra Monitor
32-inch monitor. Price ₹39,999. 4K UHD IPS Black panel, 165 Hz refresh, 1 ms response, 99 percent DCI-P3, HDR600, USB-C with 140 W power delivery, built-in KVM switch, height and pivot adjustable stand, VESA 100. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.

========== q016 [product_comparison] ==========
QUESTION: X200 or Y500 for a noisy open-plan office?
NEEDED DOCS: ['prod_x200', 'prod_y500']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
For a noisy open-plan office, choose the **SoundWave Y500 (₹24,999)**. It’s specifically recommended for this setting, with **45 dB adaptive active noise cancellation**, versus the X200’s 35 dB hybrid ANC.

The **X200 (₹12,999)** is the lower-cost option. The Y500 also offers longer battery life—60 hours versus 40—and memory-foam earcups.

Both have a **“2-year manufacturer warranty”** and are **“Non-returnable once the seal is opened”** under the hygiene policy.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [prod_y500] SoundWave Y500 Premium Headphones
Flagship over-ear wireless headphones. Price ₹24,999. 60-hour battery life, Bluetooth 5.4, adaptive active noise cancellation rated at 45 dB with transparency mode, LDAC and aptX Lossless support, USB-C and wireless charging, multipoint pairing with three devices, 268 g, memory-foam earcups. Available in Graphite and Sand. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy. Recommended over the X200 for noisy environments such as open-plan offices and flights.
--- [prod_m100] SoundWave M100 Wireless Earbuds
Entry-level true wireless earbuds. Price ₹3,499. 7 hours playback per charge and 28 hours with the case, Bluetooth 5.2, IPX4 splash resistance, touch controls, USB-C charging. No active noise cancellation. Available in Black and Ivory. 1-year manufacturer warranty. Worn in the ear, therefore non-returnable once the seal is opened, under the hygiene policy.
--- [prod_studiobuds] SoundWave Studio Buds Pro
Premium true wireless earbuds. Price ₹6,999. 9 hours playback and 32 hours with the case, Bluetooth 5.4, active noise cancellation rated 30 dB, IPX5, wireless charging case, multipoint pairing with two devices, in-ear detection. 1-year manufacturer warranty. Non-returnable once opened, under the hygiene policy.

========== q017 [product_comparison] ==========
QUESTION: Is the PulseBook Pro 16 worth twice the price of the PulseBook 14 for video editing?
NEEDED DOCS: ['prod_pulsebook14', 'prod_pulsebook_pro16']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
For demanding video editing, **the PulseBook Pro 16 is the stronger choice**:

| | PulseBook 14 | PulseBook Pro 16 |
|---|---|---|
| Price | ₹64,999 | ₹1,34,999 |
| Processor | Intel Core Ultra 5 | Intel Core Ultra 9 |
| RAM / SSD | 16 GB / 512 GB | 32 GB / 1 TB |
| Graphics | Not specified | Discrete RTX 4060 |
| Display | 14-inch 2.8K OLED, 90 Hz | 16-inch 3.2K OLED, 120 Hz |
| Weight | 1.29 kg | 1.95 kg |

**My take:** the Pro’s extra memory, storage, discrete graphics, and larger display make its ₹70,000 premium more compelling for demanding editing than for occasional projects. Both include a “2-year manufacturer warranty including one year of accidental damage protection.”

I don't have information about video-editing benchmarks or performance in your editing software, so I can’t confirm whether it delivers twice the performance.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_pulsebook14] PulseBook 14 Laptop
14-inch ultrabook. Price ₹64,999. Intel Core Ultra 5, 16 GB LPDDR5 RAM, 512 GB NVMe SSD, 14-inch 2.8K OLED display at 90 Hz, 65 W USB-C charging, 1.29 kg, 12-hour rated battery. Ports: two USB-C Thunderbolt, one USB-A, HDMI 2.1, headphone jack. 2-year manufacturer warranty including one year of accidental damage protection.
--- [prod_pulsebook_pro16] PulseBook Pro 16 Laptop
16-inch creator laptop. Price ₹1,34,999. Intel Core Ultra 9, 32 GB RAM, 1 TB NVMe SSD, discrete RTX 4060 graphics, 16-inch 3.2K OLED at 120 Hz, 100 W USB-C charging, 1.95 kg. 2-year manufacturer warranty including one year of accidental damage protection.
--- [prod_pulsebook_air13] PulseBook Air 13 Laptop
13-inch entry ultrabook. Price ₹44,999. Intel Core Ultra 3, 8 GB LPDDR5 RAM, 256 GB NVMe SSD, 13.3-inch 1920x1200 IPS display at 60 Hz, 45 W USB-C charging, 1.12 kg, 10-hour rated battery. Ports: two USB-C, one USB-A, headphone jack. No HDMI port. 2-year manufacturer warranty. Accidental damage protection is not included on the Air 13; it is included only on the PulseBook 14 and Pro 16.
--- [svc_accidental_damage] Accidental Damage Protection
PulseBook 14 and PulseBook Pro 16 include one year of accidental damage protection from the delivery date, covering drops and liquid spills. One claim is permitted in the coverage year, with a customer contribution of 10 percent of the product price. Accidental damage protection does not cover theft, loss, or cosmetic damage that does not affect function.

========== q019 [product_comparison] ==========
QUESTION: Which of your headphones is lighter and does it matter for long flights?
NEEDED DOCS: ['prod_x200', 'prod_y500']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
The **SoundWave X200** is lighter at **250 g**, versus **268 g** for the Y500—an 18 g difference.

Lower weight may matter for comfort over a long flight, but the **Y500 is recommended for flights**: it has stronger noise cancellation (45 dB versus 35 dB), memory-foam earcups, and 60-hour rated battery life versus 40 hours.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_y500] SoundWave Y500 Premium Headphones
Flagship over-ear wireless headphones. Price ₹24,999. 60-hour battery life, Bluetooth 5.4, adaptive active noise cancellation rated at 45 dB with transparency mode, LDAC and aptX Lossless support, USB-C and wireless charging, multipoint pairing with three devices, 268 g, memory-foam earcups. Available in Graphite and Sand. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy. Recommended over the X200 for noisy environments such as open-plan offices and flights.
--- [tsg_headphone_battery] Headphone Battery Draining Fast
Rapid battery drain on SoundWave headphones is usually caused by active noise cancellation combined with high volume. ANC reduces rated battery life by roughly 30 percent. Check for firmware updates in the SoundWave app, disable multipoint if two devices are not needed, and confirm the unit powers off rather than idling when removed. If runtime is below 50 percent of the rated figure with ANC off, the battery is considered defective and covered under warranty.
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [prod_m100] SoundWave M100 Wireless Earbuds
Entry-level true wireless earbuds. Price ₹3,499. 7 hours playback per charge and 28 hours with the case, Bluetooth 5.2, IPX4 splash resistance, touch controls, USB-C charging. No active noise cancellation. Available in Black and Ivory. 1-year manufacturer warranty. Worn in the ear, therefore non-returnable once the seal is opened, under the hygiene policy.
--- [catalogue_summary] TechStore Product Catalogue
TechStore sells 16 products, one per line as name | type | price | key specs. Each product's own page has its full details.
SoundWave X200 Wireless Headphones | headphones, over-ear | ₹12,999 | 40 h battery · 35 dB ANC · 250 g
SoundWave Y500 Premium Headphones | headphones, over-ear | ₹24,999 | 60 h battery · 45 dB adaptive ANC · 268 g
SoundWave M100 Wireless Earbuds | earbuds | ₹3,499 | 7 h battery (28 h with case) · no ANC · IPX4
SoundWave Studio Buds Pro | earbuds | ₹6,999 | 9 h battery (32 h with case) · 30 dB ANC · IPX5
PulseBook Air 13 Laptop | laptop, 13.3-inch | ₹44,999 | Core Ultra 3 · 8 GB RAM · 256 GB SSD · 1.12 kg
PulseBook 14 Laptop | laptop, 14-inch | ₹64,999 | Core Ultra 5 · 16 GB RAM · 512 GB SSD · 1.29 kg
PulseBook Pro 16 Laptop | laptop, 16-inch | ₹1,34,999 | Core Ultra 9 · 32 GB RAM · 1 TB SSD · RTX 4060 · 1.95 kg
NovaTab Mini 8 Tablet | tablet, 8.4-inch | ₹17,999 | 6 GB RAM · 128 GB storage · stylus not supported
NovaTab 11 Tablet | tablet, 11-inch | ₹29,999 | 8 GB RAM · 256 GB storage · stylus supported, sold separately at ₹4,999
AuraWatch 3 Smartwatch | smartwatch | ₹8,999 | 14-day battery · GPS · 5 ATM
AuraWatch Pro Smartwatch | smartwatch | ₹15,999 | 18-day battery · ECG · dual-band GPS · 10 ATM
ClearView 27 Monitor | monitor, 27-inch | ₹22,999 | 4K · 144 Hz · USB-C with 90 W power delivery
ClearView 32 Ultra Monitor | monitor, 32-inch | ₹39,999 | 4K · 165 Hz · USB-C with 140 W power delivery · KVM switch
VoltCharge 65W GaN Charger | charger | ₹2,499 | 65 W · not sufficient to charge the PulseBook Pro 16 at full speed
VoltCharge 100W GaN Charger | charger | ₹3,999 | 100 W · required for full-speed charging of the PulseBook Pro 16
VoltBank 20000mAh Power Bank | power bank | ₹2,999 | 20000 mAh · 65 W USB-C output · 389 g

========== q020 [product_comparison] ==========
QUESTION: I want a tablet for reading and a laptop for college. What should I buy under 1 lakh total?
NEEDED DOCS: ['prod_novatab11', 'prod_pulsebook14']   MISSING FROM WHAT THE MODEL SAW: ['prod_pulsebook14']

ANSWER:
I’d recommend this combination for reading and college:

| Product | Why it fits | Price |
|---|---|---:|
| **NovaTab Mini 8** | Compact 8.4-inch display for reading, 128 GB expandable storage, 5500 mAh battery | ₹17,999 |
| **PulseBook 14** | Core Ultra 5, 16 GB RAM and 512 GB SSD; portable at 1.29 kg | ₹64,999 |
| **Total** | | **₹82,998** |

**Note:** The Mini 8 does not support a stylus. If handwritten notes matter, choose the **NovaTab 11 + PulseBook 14** for **₹94,998**, or **₹99,997 including the separately sold stylus**.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_novatab11] NovaTab 11 Tablet
11-inch Android tablet. Price ₹29,999. Snapdragon 7 Gen 3, 8 GB RAM, 256 GB storage expandable by microSD, 11-inch 2.5K LCD at 120 Hz, 8000 mAh battery, stylus supported and sold separately at ₹4,999. 1-year manufacturer warranty.
--- [prod_novatab_mini8] NovaTab Mini 8 Tablet
8-inch compact Android tablet. Price ₹17,999. Snapdragon 6 Gen 1, 6 GB RAM, 128 GB storage expandable by microSD, 8.4-inch 1920x1200 LCD at 90 Hz, 5500 mAh battery. Stylus is not supported on the Mini 8; stylus support is exclusive to the NovaTab 11. 1-year manufacturer warranty.
--- [prod_pulsebook_pro16] PulseBook Pro 16 Laptop
16-inch creator laptop. Price ₹1,34,999. Intel Core Ultra 9, 32 GB RAM, 1 TB NVMe SSD, discrete RTX 4060 graphics, 16-inch 3.2K OLED at 120 Hz, 100 W USB-C charging, 1.95 kg. 2-year manufacturer warranty including one year of accidental damage protection.
--- [prod_pulsebook_air13] PulseBook Air 13 Laptop
13-inch entry ultrabook. Price ₹44,999. Intel Core Ultra 3, 8 GB LPDDR5 RAM, 256 GB NVMe SSD, 13.3-inch 1920x1200 IPS display at 60 Hz, 45 W USB-C charging, 1.12 kg, 10-hour rated battery. Ports: two USB-C, one USB-A, headphone jack. No HDMI port. 2-year manufacturer warranty. Accidental damage protection is not included on the Air 13; it is included only on the PulseBook 14 and Pro 16.
--- [catalogue_summary] TechStore Product Catalogue
TechStore sells 16 products, one per line as name | type | price | key specs. Each product's own page has its full details.
SoundWave X200 Wireless Headphones | headphones, over-ear | ₹12,999 | 40 h battery · 35 dB ANC · 250 g
SoundWave Y500 Premium Headphones | headphones, over-ear | ₹24,999 | 60 h battery · 45 dB adaptive ANC · 268 g
SoundWave M100 Wireless Earbuds | earbuds | ₹3,499 | 7 h battery (28 h with case) · no ANC · IPX4
SoundWave Studio Buds Pro | earbuds | ₹6,999 | 9 h battery (32 h with case) · 30 dB ANC · IPX5
PulseBook Air 13 Laptop | laptop, 13.3-inch | ₹44,999 | Core Ultra 3 · 8 GB RAM · 256 GB SSD · 1.12 kg
PulseBook 14 Laptop | laptop, 14-inch | ₹64,999 | Core Ultra 5 · 16 GB RAM · 512 GB SSD · 1.29 kg
PulseBook Pro 16 Laptop | laptop, 16-inch | ₹1,34,999 | Core Ultra 9 · 32 GB RAM · 1 TB SSD · RTX 4060 · 1.95 kg
NovaTab Mini 8 Tablet | tablet, 8.4-inch | ₹17,999 | 6 GB RAM · 128 GB storage · stylus not supported
NovaTab 11 Tablet | tablet, 11-inch | ₹29,999 | 8 GB RAM · 256 GB storage · stylus supported, sold separately at ₹4,999
AuraWatch 3 Smartwatch | smartwatch | ₹8,999 | 14-day battery · GPS · 5 ATM
AuraWatch Pro Smartwatch | smartwatch | ₹15,999 | 18-day battery · ECG · dual-band GPS · 10 ATM
ClearView 27 Monitor | monitor, 27-inch | ₹22,999 | 4K · 144 Hz · USB-C with 90 W power delivery
ClearView 32 Ultra Monitor | monitor, 32-inch | ₹39,999 | 4K · 165 Hz · USB-C with 140 W power delivery · KVM switch
VoltCharge 65W GaN Charger | charger | ₹2,499 | 65 W · not sufficient to charge the PulseBook Pro 16 at full speed
VoltCharge 100W GaN Charger | charger | ₹3,999 | 100 W · required for full-speed charging of the PulseBook Pro 16
VoltBank 20000mAh Power Bank | power bank | ₹2,999 | 20000 mAh · 65 W USB-C output · 389 g

========== q024 [troubleshooting] ==========
QUESTION: My monitor says no signal.
NEEDED DOCS: ['tsg_monitor_no_signal']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Try these steps:

1. Check that the monitor’s input source matches the cable you’re using.
2. If using USB-C, confirm your laptop’s port supports DisplayPort Alt Mode.
3. Try another cable—many USB-C cables carry power but not video.
4. For 4K at 144 Hz, use DisplayPort 1.4 or HDMI 2.1.
5. Reset the monitor to factory defaults through its menu.

Which monitor model and cable connection are you using?

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_monitor_no_signal] Monitor Shows No Signal
If ClearView 27 reports no signal: 1) Confirm the input source matches the cable used, selectable in the on-screen menu. 2) For USB-C, confirm the laptop port supports DisplayPort Alt Mode; the PulseBook USB-A port does not. 3) Try a different cable, as many USB-C cables carry power but not video. 4) At 4K 144 Hz use DisplayPort 1.4 or HDMI 2.1; older cables cap the refresh rate. 5) Reset the monitor to factory defaults from the menu.
--- [tsg_monitor_flicker] Monitor Flickering
Flicker at high refresh rates is usually a cable limitation. For 4K at 144 Hz or above use a certified DisplayPort 1.4 or HDMI 2.1 cable under 2 metres. Disable adaptive sync temporarily to test. If flicker persists at 60 Hz with a known-good cable, the panel is a warranty defect.
--- [prod_clearview27] ClearView 27 Monitor
27-inch monitor. Price ₹22,999. 4K UHD IPS panel, 144 Hz refresh, 1 ms response, 95 percent DCI-P3 colour coverage, USB-C with 90 W power delivery, height and pivot adjustable stand, VESA 100 mount. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.
--- [prod_clearview32] ClearView 32 Ultra Monitor
32-inch monitor. Price ₹39,999. 4K UHD IPS Black panel, 165 Hz refresh, 1 ms response, 99 percent DCI-P3, HDR600, USB-C with 140 W power delivery, built-in KVM switch, height and pivot adjustable stand, VESA 100. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.

========== q025 [troubleshooting] ==========
QUESTION: My headphone battery drains much faster than advertised.
NEEDED DOCS: ['tsg_headphone_battery', 'pol_warranty_terms']   MISSING FROM WHAT THE MODEL SAW: ['pol_warranty_terms']

ANSWER:
I’m sorry your headphones aren’t lasting as expected. Which model do you have, how many hours does a full charge last, and is active noise cancellation (ANC) on?

1. Check for firmware updates in the SoundWave app.
2. Turn off ANC and lower the volume—ANC reduces rated battery life by roughly 30%.
3. Disable multipoint if you don’t need two devices connected.
4. Confirm the headphones power off rather than idle when removed.

If runtime is “below 50 percent of the rated figure with ANC off,” the battery is considered defective and covered under warranty.

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_headphone_battery] Headphone Battery Draining Fast
Rapid battery drain on SoundWave headphones is usually caused by active noise cancellation combined with high volume. ANC reduces rated battery life by roughly 30 percent. Check for firmware updates in the SoundWave app, disable multipoint if two devices are not needed, and confirm the unit powers off rather than idling when removed. If runtime is below 50 percent of the rated figure with ANC off, the battery is considered defective and covered under warranty.
--- [tsg_watch_battery] Smartwatch Battery Draining Fast
Always-on display reduces AuraWatch Pro battery life from 18 days to roughly 6. Continuous SpO2 monitoring and dual-band GPS also shorten runtime substantially. Disable always-on display and continuous SpO2 to restore rated life. If runtime is under 50 percent of the rated figure with those features off, the battery is a warranty defect.
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [prod_y500] SoundWave Y500 Premium Headphones
Flagship over-ear wireless headphones. Price ₹24,999. 60-hour battery life, Bluetooth 5.4, adaptive active noise cancellation rated at 45 dB with transparency mode, LDAC and aptX Lossless support, USB-C and wireless charging, multipoint pairing with three devices, 268 g, memory-foam earcups. Available in Graphite and Sand. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy. Recommended over the X200 for noisy environments such as open-plan offices and flights.

========== q027 [billing_dispute] ==========
QUESTION: My payment failed but the money was debited. No order was created. What happens now?
NEEDED DOCS: ['bill_failed_payment']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
The debit is a temporary bank hold that reverses automatically:

- **Card or UPI:** “5 to 7 business days”
- **Net banking:** “up to 10” business days

No order was created, so there’s nothing to cancel. If the money hasn’t reversed after the applicable period, contact support with your bank reference number. TechStore will raise a chargeback trace with the payment gateway.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_failed_payment] Payment Failed but Money Debited
If a payment fails but the amount is debited, the bank has placed a temporary hold that is released automatically. Card and UPI holds reverse within 5 to 7 business days; net banking can take up to 10. No order is created for a failed payment, so there is nothing to cancel. If the amount has not reversed after the stated period, contact support with the bank reference number and TechStore raises a chargeback trace with the payment gateway.
--- [acc_order_history] Order History and Invoices
All orders from the past 8 years are visible under Orders in the account, with status, tracking and downloadable invoice. Orders placed as part of a cancelled payment attempt do not appear, because no order is created for a failed payment.
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.
--- [ship_failed_delivery] Failed Delivery Attempts
The courier makes three delivery attempts on consecutive business days. After the third failed attempt the parcel is returned to our warehouse and the order is refunded in full, including any delivery charge paid, within 7 business days of the parcel being received back. A customer can reschedule delivery once through the tracking link.

========== q029 [billing_dispute] ==========
QUESTION: I bought on no-cost EMI and returned the product. The bank is still charging me interest. Who pays that?
NEEDED DOCS: ['bill_emi', 'pol_refund_timeline']   MISSING FROM WHAT THE MODEL SAW: ['pol_refund_timeline']

ANSWER:
Under “No-Cost EMI,” TechStore absorbs the interest as an upfront discount. If you return the order, that discount is deducted from your refund, and the bank may still charge interest already levied.

1. Contact your bank to cancel the EMI plan.
2. Ask the bank about the interest already charged—it isn’t automatically waived on return.

I don't have information about the specific interest amount charged to your account.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_emi] EMI and No-Cost EMI
EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount. If an order paid by no-cost EMI is returned, the discount is deducted from the refund and the bank may still charge interest already levied; the bank must be contacted to cancel the EMI plan.
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.
--- [bill_chargeback] Bank Chargebacks and Disputes
If a customer raises a chargeback with their bank, the order is frozen and any parallel TechStore refund is suspended to prevent a double credit. Chargebacks take 45 to 90 days to resolve through the card network. Contacting support directly is almost always faster than a chargeback, and support can withdraw a chargeback by providing the bank with resolution evidence.
--- [prod_voltbank20k] VoltBank 20000mAh Power Bank
20000 mAh power bank. Price ₹2,999. 65 W USB-C output, 20 W USB-A output, pass-through charging, LED capacity display, 389 g. Its capacity is under 100 Wh; check your airline's rules before carrying it on a flight. Can charge the PulseBook Air 13 once or the NovaTab 11 twice. 1-year manufacturer warranty.

========== q031 [technical_api] ==========
QUESTION: Your webhook returns 403 even though my HMAC signature is valid. Here is my Python: sig = hmac.new(secret, json.dumps(request.json).encode(), 'sha256').hexdigest()
NEEDED DOCS: ['api_webhook_signature']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Your code computes the HMAC over re-serialised JSON, not the raw request body. `json.dumps(request.json)` can change whitespace and key order, producing a different signature.

1. Capture the exact raw request bytes **before any JSON parsing**.
2. Use the **webhook secret**, not your API token:
   ```python
   sig = hmac.new(webhook_secret, raw_body, 'sha256').hexdigest()
   ```
3. Compare the result with the `X-TechStore-Signature` header.

If the 403 includes `insufficient_scope`, that’s a separate token-scope issue, not a signature failure.

EVIDENCE THE MODEL WAS GIVEN:
--- [api_webhook_signature] Webhook Signature Verification and 403 Errors
Every webhook carries an X-TechStore-Signature header containing an HMAC-SHA256 of the raw request body, keyed with the webhook secret, hex encoded. A 403 returned by our delivery checker almost always means the signature was computed over a parsed and re-serialised body rather than the raw bytes; JSON re-serialisation changes key order and whitespace and therefore changes the HMAC. Compute the HMAC over the exact raw body before any JSON parsing. The second most common cause is using the API token instead of the webhook secret as the HMAC key.
--- [api_scopes] Token Scopes and 403 Errors
Tokens carry scopes: orders:read, orders:write, inventory:read, shipments:read, webhooks:manage. A 403 with code insufficient_scope means the token is valid but lacks the required scope, which is different from a signature failure. Scopes are set when the token is created and cannot be widened afterwards; issue a new token instead.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_webhook_retries] Webhook Delivery and Retries
Webhooks expect a 2xx response within 5 seconds. Non-2xx or timeout triggers retries at 1, 5, 25 and 125 minutes, then the endpoint is marked unhealthy and deliveries pause until reactivated in the dashboard. Handlers must be idempotent, because a duplicate delivery is possible even after a successful response. Each delivery carries an X-TechStore-Delivery-Id that is stable across retries.

========== q033 [technical_api] ==========
QUESTION: My integration worked in sandbox but returns 401 in production with the same code. Why?
NEEDED DOCS: ['api_auth', 'api_overview']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
The most common cause is using a sandbox token in production—production rejects sandbox tokens.

1. Use a production bearer token issued in the partner dashboard.
2. Send it as `Authorization: Bearer <token>`.
3. Check that the token isn’t missing, malformed or expired. Tokens expire **90 days after issue**.

You can rotate tokens in the dashboard without downtime; the previous token remains valid for **24 hours after rotation**.

EVIDENCE THE MODEL WAS GIVEN:
--- [api_auth] API Authentication and 401 Errors
Authenticate with Authorization: Bearer <token>. A 401 means the token is missing, malformed, expired or from the wrong environment; sandbox tokens rejected by production is the most common cause. Tokens expire 90 days after issue and can be rotated in the dashboard without downtime, since the previous token stays valid for 24 hours after rotation.
--- [api_sandbox] Sandbox Environment
Sandbox runs at https://sandbox.techstore.example/v1 with separate credentials and synthetic data that resets nightly at 02:00 IST. Sandbox order IDs begin with a 9; production IDs do not. Webhooks fire in sandbox but use a separate signing secret. Sandbox has no rate limit but is not performance representative.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_overview] TechStore Partner API Overview
The Partner API is a REST API at https://api.techstore.example/v1. All requests require an Authorization header with a bearer token issued in the partner dashboard. Requests and responses are JSON. The API exposes orders, inventory, shipments and webhooks. Sandbox is available at https://sandbox.techstore.example/v1 with separate credentials and synthetic data.

========== q034 [technical_api] ==========
QUESTION: I am hitting 429 on the bulk export endpoint at 100 requests per minute. The docs say 600. Explain.
NEEDED DOCS: ['api_rate_limits']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
The **600 requests per minute per token** limit is the general Partner API limit. Bulk export endpoints have a lower limit: **“60 per minute for the bulk export endpoints.”** At 100 requests per minute, you’re exceeding that limit.

1. Reduce bulk export traffic to no more than 60 requests per minute.
2. On a 429, honour the `Retry-After` header (in seconds).
3. Use exponential backoff with jitter.

Sustained violations for more than 15 minutes result in a temporary 1-hour block.

EVIDENCE THE MODEL WAS GIVEN:
--- [api_rate_limits] API Rate Limits and 429 Errors
The Partner API allows 600 requests per minute per token, and 60 per minute for the bulk export endpoints. Exceeding the limit returns 429 with a Retry-After header in seconds. Clients should honour Retry-After and use exponential backoff with jitter. Sustained violation for more than 15 minutes results in a temporary 1-hour block.
--- [pol_bulk_orders] Bulk and Business Orders
Orders above 10 units of a single SKU are treated as business orders and require a GSTIN. Bulk pricing is quoted by the business desk and is not available at checkout. Business orders ship in 5 to 10 business days and carry a 15-day return window rather than 30 days.
--- [api_timeouts] API Timeouts and Retry Safety
Requests time out server side at 30 seconds. A timeout does not indicate whether the operation completed, so POST requests must be retried with the same Idempotency-Key to avoid duplicates. GET, PUT and DELETE are idempotent by design and safe to retry. Retries should use exponential backoff with jitter; retrying immediately in a tight loop triggers rate limiting.
--- [api_idempotency] API Idempotency
All POST endpoints accept an Idempotency-Key header. A repeated request with the same key and an identical payload returns the original response without creating a second resource. A repeated key with a different payload returns 409. Keys are retained for 24 hours. Clients should generate a UUID per logical operation, not per HTTP attempt, so that retries reuse the same key.

========== q036 [policy_edge_case] ==========
QUESTION: I bought a PulseBook 35 days ago and it is faulty. Your return window is 30 days but the warranty is 2 years. What are my rights?
NEEDED DOCS: ['pol_return_window', 'pol_warranty_terms', 'pol_warranty_claim']   MISSING FROM WHAT THE MODEL SAW: ['pol_warranty_claim']

ANSWER:
Your return eligibility depends on delivery, not purchase: the “30-day return window” starts on the delivery date shown in tracking. A return raised on day 31 or later is automatically rejected.

Warranty is separate from returns. If your PulseBook is within its manufacturer warranty, manufacturing defects and component failure under normal use may qualify for repair or replacement, even outside the return window.

I don't have information about your PulseBook’s exact model, confirmed warranty duration, delivery date, or fault.

When was it delivered, which model is it, and what is going wrong?

EVIDENCE THE MODEL WAS GIVEN:
--- [svc_accidental_damage] Accidental Damage Protection
PulseBook 14 and PulseBook Pro 16 include one year of accidental damage protection from the delivery date, covering drops and liquid spills. One claim is permitted in the coverage year, with a customer contribution of 10 percent of the product price. Accidental damage protection does not cover theft, loss, or cosmetic damage that does not affect function.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [pol_return_window] Return Window
TechStore accepts returns within 30 days of delivery. The 30 days are counted from the delivery date shown on the tracking record, not the order date. Items must be returned in their original packaging with all accessories, manuals and free gifts included. A return raised on day 31 or later is rejected automatically by the returns system.
--- [pol_warranty_terms] Standard Warranty Terms
All products carry the manufacturer warranty stated on the product page, counted from the delivery date. Warranty covers manufacturing defects and component failure under normal use. It does not cover physical damage, liquid ingress, unauthorised repair, or normal battery capacity decline above 80 percent of the rated capacity. Warranty is independent of the 30-day return window: a product outside the return window may still be repaired or replaced under warranty.

========== q040 [policy_edge_case] ==========
QUESTION: I found the X200 cheaper elsewhere 6 days after buying, but it was during their clearance sale. Does your price match apply?
NEEDED DOCS: ['pol_price_match']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No. The Price Match Guarantee states: “Price matching does not apply during flash sales or clearance events.” Even though you found the X200 cheaper within 7 days of purchase, the competitor’s clearance sale is excluded.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [pol_price_match] Price Match Guarantee
If a customer finds the identical product cheaper on a competing authorised Indian retailer within 7 days of their purchase, TechStore refunds the difference. The competing listing must be for a new, sealed unit sold and shipped by the retailer itself, not a marketplace seller. Price matching does not apply during flash sales or clearance events.
--- [bill_price_drop] Price Drop After Purchase
If a product's TechStore price drops within 7 days of purchase, the difference is refunded on request. This applies once per order line and does not apply during flash sales, festive events or clearance. This is distinct from the price match guarantee, which covers competitor pricing.
--- [pol_exchange] Exchange Policy
An exchange can be requested within 30 days of delivery for a different size, colour or variant of the same product line, subject to stock. If the new variant costs more, the difference is charged before dispatch. If it costs less, the difference is refunded. Only one exchange is permitted per order line.

========== q053 [simple_faq] ==========
QUESTION: Can I pay with my Paytm wallet?
NEEDED DOCS: ['bill_payment_methods']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No, Paytm wallet isn’t accepted: “Wallet payments and international cards are not accepted.” You can use UPI, eligible credit/debit cards, net banking, or cash on delivery for orders up to ₹20,000.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.
--- [bill_emi] EMI and No-Cost EMI
EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount. If an order paid by no-cost EMI is returned, the discount is deducted from the refund and the bank may still charge interest already levied; the bank must be contacted to cancel the EMI plan.
--- [acc_create] Creating and Verifying an Account
An account is created with an email address or an Indian mobile number and verified by a one-time password valid for 10 minutes. A maximum of five OTPs may be requested per hour. An account is required to place an order; guest checkout is not offered.
--- [bill_refund_to_closed_card] Refund to a Closed or Expired Card
Refunds are issued to the original payment method. If that card is closed or expired, the issuing bank still routes the credit to the underlying account in most cases. If the bank rejects the credit, the funds return to TechStore within 10 business days, after which support can arrange a bank transfer once account details and identity are verified. We cannot refund to a different card at the customer's request when the original card is still active.

========== q062 [policy_edge_case] ==========
QUESTION: If my headphones get replaced, does the 2 year cover restart?
NEEDED DOCS: ['pol_replacement_warranty']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No—the 2-year cover does not restart. The replacement “inherits the remaining warranty of the original.” If fewer than 90 days remain, it carries “90 days from the replacement date.”

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_return_exclusions] Non-Returnable Items
For hygiene reasons the following are non-returnable once the seal is broken: headphones of every type (over-ear, on-ear and in-ear), earbuds, fitness bands worn on the wrist, and any personal grooming device. Opened software licences and redeemed digital gift cards are also non-returnable. These items remain covered by warranty if they are faulty; a hygiene exclusion never removes warranty rights.
--- [pol_replacement_warranty] Warranty on Replaced Units
When a unit is replaced under warranty, the replacement inherits the remaining warranty of the original; it does not start a fresh term. If fewer than 90 days remain, the replacement carries 90 days from the replacement date. Replacement units may be factory refurbished and are functionally equivalent with matching cosmetic grade.
--- [svc_out_of_warranty] Out-of-Warranty Repair
Out-of-warranty repairs are chargeable. A diagnosis fee of ₹499 applies and is waived if the repair is approved. A quotation is shared before any work begins and no work proceeds without approval. Repaired parts carry a 90-day warranty on the replaced component only.
--- [prod_y500] SoundWave Y500 Premium Headphones
Flagship over-ear wireless headphones. Price ₹24,999. 60-hour battery life, Bluetooth 5.4, adaptive active noise cancellation rated at 45 dB with transparency mode, LDAC and aptX Lossless support, USB-C and wireless charging, multipoint pairing with three devices, 268 g, memory-foam earcups. Available in Graphite and Sand. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy. Recommended over the X200 for noisy environments such as open-plan offices and flights.

========== q063 [technical_api] ==========
QUESTION: The API keeps telling me I'm sending too many requests
NEEDED DOCS: ['api_rate_limits']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
That sounds like a **429 rate-limit error**. To resolve it:

1. Check your request rate: the Partner API allows **600 requests per minute per token**, or **60 per minute for bulk export endpoints**.
2. Honour the `Retry-After` response header—it specifies how many seconds to wait.
3. Use exponential backoff with jitter for retries; avoid retrying immediately in a tight loop.
4. If violations continue for **“more than 15 minutes”**, a temporary **“1-hour block”** applies.

EVIDENCE THE MODEL WAS GIVEN:
--- [api_rate_limits] API Rate Limits and 429 Errors
The Partner API allows 600 requests per minute per token, and 60 per minute for the bulk export endpoints. Exceeding the limit returns 429 with a Retry-After header in seconds. Clients should honour Retry-After and use exponential backoff with jitter. Sustained violation for more than 15 minutes results in a temporary 1-hour block.
--- [api_timeouts] API Timeouts and Retry Safety
Requests time out server side at 30 seconds. A timeout does not indicate whether the operation completed, so POST requests must be retried with the same Idempotency-Key to avoid duplicates. GET, PUT and DELETE are idempotent by design and safe to retry. Retries should use exponential backoff with jitter; retrying immediately in a tight loop triggers rate limiting.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_idempotency] API Idempotency
All POST endpoints accept an Idempotency-Key header. A repeated request with the same key and an identical payload returns the original response without creating a second resource. A repeated key with a different payload returns 409. Keys are retained for 24 hours. Clients should generate a UUID per logical operation, not per HTTP attempt, so that retries reuse the same key.
