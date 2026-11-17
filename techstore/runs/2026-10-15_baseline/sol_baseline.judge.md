# Answers to grade

Grade each answer ONLY against the evidence shown with it. Store date: 30 September 2026.
Verdicts: correct / partial / wrong / hallucinated (rubric: Tokenomics.md §7, Grading Rubric).


========== q001 [simple_faq] ==========
QUESTION: How long do I have to return something?
NEEDED DOCS: ['pol_return_window']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
You have a **30-day return window**, counted from the delivery date shown on your tracking record—not the order date. Returns raised on day 31 or later are automatically rejected.

The item must be in its original packaging with all accessories, manuals, and free gifts included.

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
Delivery is free on orders above ₹999. Below ₹999, a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149 and is available in metro cities only for orders placed before 2 PM.

I don't have information about the delivery charge for orders totaling exactly ₹999.

EVIDENCE THE MODEL WAS GIVEN:
--- [ship_charges] Delivery Charges
Delivery is free on all orders above ₹999. Below that a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149 and is available in metro cities only for orders placed before 2 PM. Delivery charges are refunded if the order is cancelled before shipping or if the item arrives damaged.
--- [ship_open_box] Open-Box Delivery
Open-box delivery is available in 22 cities on orders above ₹20,000. The courier opens the package in the customer's presence for inspection before handover. Refusal at open-box inspection is free and refunds process within 5 to 7 business days. Open-box delivery adds 1 business day to the estimate.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.

========== q003 [simple_faq] ==========
QUESTION: What payment methods do you accept?
NEEDED DOCS: ['bill_payment_methods']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
TechStore accepts:
- UPI
- Credit and debit cards from all major Indian issuers
- Net banking from 40 partner banks
- Gift cards
- Cash on delivery for orders up to ₹20,000, with a ₹49 handling fee

Wallet payments and international cards are not accepted.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.
--- [bill_emi] EMI and No-Cost EMI
EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount. If an order paid by no-cost EMI is returned, the discount is deducted from the refund and the bank may still charge interest already levied; the bank must be contacted to cancel the EMI plan.
--- [bill_gift_card] Gift Cards and Store Credit
Gift cards are valid for 12 months from issue and can be used across multiple orders. They cannot be exchanged for cash. If an order paid partly by gift card is returned, the gift-card portion is refunded as store credit and the remainder to the original payment method. Redeemed gift cards are non-returnable.
--- [bill_cod_refund] Refunds on Cash-on-Delivery Orders
Cash-on-delivery orders cannot be refunded to a payment method because none was used. Refunds are made by bank transfer after the customer submits account number and IFSC through the secure link sent by support. Transfers complete within 5 to 7 business days of verification. The ₹49 COD handling fee is refunded only if the order is cancelled before dispatch.

========== q004 [simple_faq] ==========
QUESTION: Do you ship outside India?
NEEDED DOCS: ['ship_international']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No. TechStore ships within India only and does not ship to international, APO, or diplomatic addresses. Orders with an international billing address are accepted if the delivery address is in India.

EVIDENCE THE MODEL WAS GIVEN:
--- [ship_international] International Shipping
TechStore ships within India only. We do not ship to international addresses and cannot deliver to APO or diplomatic addresses. Orders placed with an international billing address but an Indian delivery address are accepted.
--- [ship_open_box] Open-Box Delivery
Open-box delivery is available in 22 cities on orders above ₹20,000. The courier opens the package in the customer's presence for inspection before handover. Refusal at open-box inspection is free and refunds process within 5 to 7 business days. Open-box delivery adds 1 business day to the estimate.
--- [ship_charges] Delivery Charges
Delivery is free on all orders above ₹999. Below that a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149 and is available in metro cities only for orders placed before 2 PM. Delivery charges are refunded if the order is cancelled before shipping or if the item arrives damaged.
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.

========== q005 [simple_faq] ==========
QUESTION: Can I return earbuds I already opened?
NEEDED DOCS: ['pol_return_exclusions']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No. Under TechStore’s “Non-Returnable Items” policy, earbuds are **“non-returnable once the seal is broken”** for hygiene reasons.

If they’re faulty, they remain covered by warranty—the hygiene exclusion does not remove warranty rights.

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_return_exclusions] Non-Returnable Items
For hygiene reasons the following are non-returnable once the seal is broken: headphones of every type (over-ear, on-ear and in-ear), earbuds, fitness bands worn on the wrist, and any personal grooming device. Opened software licences and redeemed digital gift cards are also non-returnable. These items remain covered by warranty if they are faulty; a hygiene exclusion never removes warranty rights.
--- [tsg_earbuds_one_side] Only One Earbud Working
If only one SoundWave earbud plays: 1) Place both buds in the case, close the lid for 10 seconds and reopen. 2) Forget the device in phone Bluetooth settings and re-pair. 3) Reset the buds by holding both touch panels for 15 seconds until the LED flashes red and white. 4) Clean the charging contacts on the silent bud with a dry cloth; contact dirt is the most common cause. 5) If the silent bud still does not charge, it is a warranty defect.
--- [prod_studiobuds] SoundWave Studio Buds Pro
Premium true wireless earbuds. Price ₹6,999. 9 hours playback and 32 hours with the case, Bluetooth 5.4, active noise cancellation rated 30 dB, IPX5, wireless charging case, multipoint pairing with two devices, in-ear detection. 1-year manufacturer warranty. Non-returnable once opened, under the hygiene policy.
--- [tsg_earbuds_case_charge] Earbud Case Not Charging
If the charging case does not charge: confirm the cable is USB-C and carries data or power, try a different 5 V adapter, and check the LED responds when plugged in. A case left fully discharged for over a month may need 15 minutes before any LED appears. If no LED appears after 30 minutes on a known-good charger, raise a warranty claim.

========== q006 [order_status] ==========
QUESTION: Where is my order #48213?
NEEDED DOCS: ['ship_tracking']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Your order #48213 is marked **Shipped** with BlueDart.

- **Item:** SoundWave X200 Wireless Headphones
- **Tracking ID:** BD4471920381
- **Expected delivery:** 30 September 2026 — this date has passed.

You can check tracking under **Orders** in your account or through the link sent by email and SMS. I don't have information about its current location or the reason for the delay. I can connect you with a human agent to investigate the overdue delivery.

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

========== q007 [order_status] ==========
QUESTION: Has order 48390 shipped yet?
NEEDED DOCS: ['ship_tracking']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No, order #48390 is still **Processing** and has not shipped yet. Its estimated delivery date is **2 October 2026**.

Once it is marked Shipped, your tracking link will be sent by email and SMS.

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [ship_tracking] Tracking an Order
A tracking link is emailed and sent by SMS when the order is marked Shipped. Tracking can also be seen under Orders in the account. Tracking information can take up to 12 hours after dispatch to become active with the courier. If tracking has not updated for more than 48 hours, contact support so a courier trace can be raised.
--- [pol_bulk_orders] Bulk and Business Orders
Orders above 10 units of a single SKU are treated as business orders and require a GSTIN. Bulk pricing is quoted by the business desk and is not available at checkout. Business orders ship in 5 to 10 business days and carry a 15-day return window rather than 30 days.
--- [ship_charges] Delivery Charges
Delivery is free on all orders above ₹999. Below that a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149 and is available in metro cities only for orders placed before 2 PM. Delivery charges are refunded if the order is cancelled before shipping or if the item arrives damaged.
--- ORDER 48390
{"order_id": "48390", "customer_id": "cust_3117", "email": "priya.m@example.com", "placed_at": "2026-09-20", "status": "Processing", "items": [{"sku": "prod_pulsebook14", "name": "PulseBook 14 Laptop", "qty": 1, "unit_price": 64999}], "total": 64999, "payment_method": "No-Cost EMI (6 months)", "delivery_pin": "110024", "courier": null, "tracking_id": null, "eta": "2026-10-02", "charges": [{"date": "2026-09-20", "amount": 64999, "type": "capture", "status": "settled"}]}

========== q008 [order_status] ==========
QUESTION: When will order 48677 arrive?
NEEDED DOCS: ['ship_delivery_times']   MISSING FROM WHAT THE MODEL SAW: ['ship_delivery_times']

ANSWER:
Order #48677 is shipped and expected to arrive today, 30 September 2026, via BlueDart.

Your tracking ID is **BD4473001199**. You can check tracking under **Orders** in your TechStore account.

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
Your refund of ₹2,499 for order #48455 has been initiated and is expected by **1 October 2026**. As of today, 30 September, it is not overdue.

The cancellation policy provides a full refund within **“5 to 7 business days.”** The money will return to your original UPI payment method.

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
You ordered **1 SoundWave Y500 Premium Headphones** in **order #48501** for **₹24,999**. It was delivered on **26 September 2026**.

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

========== q011 [product_info] ==========
QUESTION: Does the SoundWave X200 have noise cancellation?
NEEDED DOCS: ['prod_x200']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Yes, the SoundWave X200 has **hybrid active noise cancellation rated at 35 dB**.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [prod_y500] SoundWave Y500 Premium Headphones
Flagship over-ear wireless headphones. Price ₹24,999. 60-hour battery life, Bluetooth 5.4, adaptive active noise cancellation rated at 45 dB with transparency mode, LDAC and aptX Lossless support, USB-C and wireless charging, multipoint pairing with three devices, 268 g, memory-foam earcups. Available in Graphite and Sand. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy. Recommended over the X200 for noisy environments such as open-plan offices and flights.
--- [prod_m100] SoundWave M100 Wireless Earbuds
Entry-level true wireless earbuds. Price ₹3,499. 7 hours playback per charge and 28 hours with the case, Bluetooth 5.2, IPX4 splash resistance, touch controls, USB-C charging. No active noise cancellation. Available in Black and Ivory. 1-year manufacturer warranty. Worn in the ear, therefore non-returnable once the seal is opened, under the hygiene policy.
--- [prod_studiobuds] SoundWave Studio Buds Pro
Premium true wireless earbuds. Price ₹6,999. 9 hours playback and 32 hours with the case, Bluetooth 5.4, active noise cancellation rated 30 dB, IPX5, wireless charging case, multipoint pairing with two devices, in-ear detection. 1-year manufacturer warranty. Non-returnable once opened, under the hygiene policy.

========== q012 [product_info] ==========
QUESTION: How much is the PulseBook 14?
NEEDED DOCS: ['prod_pulsebook14']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
The PulseBook 14 costs ₹64,999.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_pulsebook14] PulseBook 14 Laptop
14-inch ultrabook. Price ₹64,999. Intel Core Ultra 5, 16 GB LPDDR5 RAM, 512 GB NVMe SSD, 14-inch 2.8K OLED display at 90 Hz, 65 W USB-C charging, 1.29 kg, 12-hour rated battery. Ports: two USB-C Thunderbolt, one USB-A, HDMI 2.1, headphone jack. 2-year manufacturer warranty including one year of accidental damage protection.
--- [prod_pulsebook_pro16] PulseBook Pro 16 Laptop
16-inch creator laptop. Price ₹1,34,999. Intel Core Ultra 9, 32 GB RAM, 1 TB NVMe SSD, discrete RTX 4060 graphics, 16-inch 3.2K OLED at 120 Hz, 100 W USB-C charging, 1.95 kg. 2-year manufacturer warranty including one year of accidental damage protection.
--- [prod_pulsebook_air13] PulseBook Air 13 Laptop
13-inch entry ultrabook. Price ₹44,999. Intel Core Ultra 3, 8 GB LPDDR5 RAM, 256 GB NVMe SSD, 13.3-inch 1920x1200 IPS display at 60 Hz, 45 W USB-C charging, 1.12 kg, 10-hour rated battery. Ports: two USB-C, one USB-A, headphone jack. No HDMI port. 2-year manufacturer warranty. Accidental damage protection is not included on the Air 13; it is included only on the PulseBook 14 and Pro 16.
--- [prod_novatab11] NovaTab 11 Tablet
11-inch Android tablet. Price ₹29,999. Snapdragon 7 Gen 3, 8 GB RAM, 256 GB storage expandable by microSD, 11-inch 2.5K LCD at 120 Hz, 8000 mAh battery, stylus supported and sold separately at ₹4,999. 1-year manufacturer warranty.

========== q013 [product_info] ==========
QUESTION: What is the battery life of the AuraWatch 3?
NEEDED DOCS: ['prod_aurawatch3']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
The AuraWatch 3 has a rated battery life of **14 days**.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_aurawatch3] AuraWatch 3 Smartwatch
Fitness smartwatch. Price ₹8,999. 1.4-inch AMOLED display, 14-day battery, heart-rate and SpO2 sensors, built-in GPS, 5 ATM water resistance, sleep tracking. Compatible with Android 9 and above and iOS 14 and above. 1-year manufacturer warranty. Worn on the wrist, therefore non-returnable once used, under the hygiene policy.
--- [tsg_watch_battery] Smartwatch Battery Draining Fast
Always-on display reduces AuraWatch Pro battery life from 18 days to roughly 6. Continuous SpO2 monitoring and dual-band GPS also shorten runtime substantially. Disable always-on display and continuous SpO2 to restore rated life. If runtime is under 50 percent of the rated figure with those features off, the battery is a warranty defect.
--- [prod_aurawatch_pro] AuraWatch Pro Smartwatch
Premium fitness smartwatch. Price ₹15,999. 1.5-inch AMOLED always-on display, 18-day battery, ECG and SpO2 sensors, dual-band GPS, 10 ATM water resistance, offline maps, 100 sport modes. Compatible with Android 10 and above and iOS 15 and above. 2-year manufacturer warranty. Non-returnable once used, under the hygiene policy.
--- [tsg_watch_sync] Smartwatch Not Syncing
If AuraWatch 3 will not sync: confirm the companion app has Bluetooth and background-activity permission, confirm the phone runs Android 9 or later or iOS 14 or later, force-close and reopen the app, and ensure the watch firmware is current. Battery optimisation settings on some Android phones stop the app in the background and are the most common cause; exclude the app from optimisation.

========== q014 [product_info] ==========
QUESTION: Does the ClearView 27 support USB-C?
NEEDED DOCS: ['prod_clearview27']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Yes, the ClearView 27 supports USB-C with **90 W power delivery**, allowing it to supply up to 90 W to a connected laptop.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_clearview27] ClearView 27 Monitor
27-inch monitor. Price ₹22,999. 4K UHD IPS panel, 144 Hz refresh, 1 ms response, 95 percent DCI-P3 colour coverage, USB-C with 90 W power delivery, height and pivot adjustable stand, VESA 100 mount. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.
--- [tsg_monitor_usbc_power] Monitor Not Charging Laptop over USB-C
The ClearView 27 supplies 90 W and the ClearView 32 Ultra supplies 140 W over USB-C. A PulseBook Pro 16 drawing 100 W will charge slowly from a ClearView 27 under sustained load. Confirm the cable is rated for both video and 100 W power delivery; many are not. Verify USB-C power delivery is enabled in the monitor menu, as it is off by default on some firmware.
--- [tsg_monitor_no_signal] Monitor Shows No Signal
If ClearView 27 reports no signal: 1) Confirm the input source matches the cable used, selectable in the on-screen menu. 2) For USB-C, confirm the laptop port supports DisplayPort Alt Mode; the PulseBook USB-A port does not. 3) Try a different cable, as many USB-C cables carry power but not video. 4) At 4K 144 Hz use DisplayPort 1.4 or HDMI 2.1; older cables cap the refresh rate. 5) Reset the monitor to factory defaults from the menu.
--- [prod_clearview32] ClearView 32 Ultra Monitor
32-inch monitor. Price ₹39,999. 4K UHD IPS Black panel, 165 Hz refresh, 1 ms response, 99 percent DCI-P3, HDR600, USB-C with 140 W power delivery, built-in KVM switch, height and pivot adjustable stand, VESA 100. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.

========== q015 [product_info] ==========
QUESTION: Is the NovaTab 11 stylus included?
NEEDED DOCS: ['prod_novatab11']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No, the NovaTab 11 stylus is sold separately for ₹4,999. The tablet costs ₹29,999.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_novatab11] NovaTab 11 Tablet
11-inch Android tablet. Price ₹29,999. Snapdragon 7 Gen 3, 8 GB RAM, 256 GB storage expandable by microSD, 11-inch 2.5K LCD at 120 Hz, 8000 mAh battery, stylus supported and sold separately at ₹4,999. 1-year manufacturer warranty.
--- [prod_novatab_mini8] NovaTab Mini 8 Tablet
8-inch compact Android tablet. Price ₹17,999. Snapdragon 6 Gen 1, 6 GB RAM, 128 GB storage expandable by microSD, 8.4-inch 1920x1200 LCD at 90 Hz, 5500 mAh battery. Stylus is not supported on the Mini 8; stylus support is exclusive to the NovaTab 11. 1-year manufacturer warranty.
--- [prod_aurawatch3] AuraWatch 3 Smartwatch
Fitness smartwatch. Price ₹8,999. 1.4-inch AMOLED display, 14-day battery, heart-rate and SpO2 sensors, built-in GPS, 5 ATM water resistance, sleep tracking. Compatible with Android 9 and above and iOS 14 and above. 1-year manufacturer warranty. Worn on the wrist, therefore non-returnable once used, under the hygiene policy.
--- [prod_m100] SoundWave M100 Wireless Earbuds
Entry-level true wireless earbuds. Price ₹3,499. 7 hours playback per charge and 28 hours with the case, Bluetooth 5.2, IPX4 splash resistance, touch controls, USB-C charging. No active noise cancellation. Available in Black and Ivory. 1-year manufacturer warranty. Worn in the ear, therefore non-returnable once the seal is opened, under the hygiene policy.

========== q016 [product_comparison] ==========
QUESTION: X200 or Y500 for a noisy open-plan office?
NEEDED DOCS: ['prod_x200', 'prod_y500']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
For a noisy open-plan office, I recommend the **SoundWave Y500**—the product guidance specifically recommends it over the X200 for this setting.

- **Y500 — ₹24,999:** Adaptive active noise cancellation rated at **45 dB**, transparency mode, 60-hour battery life, and memory-foam earcups.
- **X200 — ₹12,999:** Hybrid active noise cancellation rated at **35 dB** and 40-hour battery life—a lower-priced option if budget matters more.

Both have a **2-year manufacturer warranty** and are **“non-returnable once the seal is opened” under the hygiene policy**.

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
**For demanding video editing, the PulseBook Pro 16 offers substantial upgrades—but it isn’t necessarily worth twice the price for lighter work.**

| Feature | PulseBook 14 | PulseBook Pro 16 |
|---|---|---|
| Price | ₹64,999 | ₹1,34,999 |
| Processor | Intel Core Ultra 5 | Intel Core Ultra 9 |
| RAM | 16 GB | 32 GB |
| SSD | 512 GB | 1 TB |
| Graphics | Not specified | Discrete RTX 4060 |
| Display | 14-inch 2.8K OLED, 90 Hz | 16-inch 3.2K OLED, 120 Hz |
| Weight | 1.29 kg | 1.95 kg |

The Pro costs **₹70,000 more—slightly over twice the price**. Its higher-tier processor, double the RAM and storage, discrete graphics, and larger display make it the stronger specification-based choice for demanding editing. The PulseBook 14 is the lower-cost, lighter option.

Both include a **“2-year manufacturer warranty”** and **“one year of accidental damage protection”**, so warranty coverage doesn’t distinguish them.

I don't have information about video-editing benchmarks or performance in your specific editing software, so I can’t confirm whether the extra cost would pay off for your workflow.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_pulsebook14] PulseBook 14 Laptop
14-inch ultrabook. Price ₹64,999. Intel Core Ultra 5, 16 GB LPDDR5 RAM, 512 GB NVMe SSD, 14-inch 2.8K OLED display at 90 Hz, 65 W USB-C charging, 1.29 kg, 12-hour rated battery. Ports: two USB-C Thunderbolt, one USB-A, HDMI 2.1, headphone jack. 2-year manufacturer warranty including one year of accidental damage protection.
--- [prod_pulsebook_pro16] PulseBook Pro 16 Laptop
16-inch creator laptop. Price ₹1,34,999. Intel Core Ultra 9, 32 GB RAM, 1 TB NVMe SSD, discrete RTX 4060 graphics, 16-inch 3.2K OLED at 120 Hz, 100 W USB-C charging, 1.95 kg. 2-year manufacturer warranty including one year of accidental damage protection.
--- [prod_pulsebook_air13] PulseBook Air 13 Laptop
13-inch entry ultrabook. Price ₹44,999. Intel Core Ultra 3, 8 GB LPDDR5 RAM, 256 GB NVMe SSD, 13.3-inch 1920x1200 IPS display at 60 Hz, 45 W USB-C charging, 1.12 kg, 10-hour rated battery. Ports: two USB-C, one USB-A, headphone jack. No HDMI port. 2-year manufacturer warranty. Accidental damage protection is not included on the Air 13; it is included only on the PulseBook 14 and Pro 16.
--- [svc_accidental_damage] Accidental Damage Protection
PulseBook 14 and PulseBook Pro 16 include one year of accidental damage protection from the delivery date, covering drops and liquid spills. One claim is permitted in the coverage year, with a customer contribution of 10 percent of the product price. Accidental damage protection does not cover theft, loss, or cosmetic damage that does not affect function.

========== q018 [product_comparison] ==========
QUESTION: Will the VoltCharge 65W charge my PulseBook Pro 16 properly?
NEEDED DOCS: ['prod_voltcharge65', 'prod_pulsebook_pro16']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No—the VoltCharge 65W won’t charge your PulseBook Pro 16 properly: it may charge very slowly or not at all. The laptop requires **100 W** for full-speed charging.

The **VoltCharge 100W GaN Charger**, priced at **₹3,999**, supports full-speed charging and includes a detachable braided cable.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_pulsebook_pro16] PulseBook Pro 16 Laptop
16-inch creator laptop. Price ₹1,34,999. Intel Core Ultra 9, 32 GB RAM, 1 TB NVMe SSD, discrete RTX 4060 graphics, 16-inch 3.2K OLED at 120 Hz, 100 W USB-C charging, 1.95 kg. 2-year manufacturer warranty including one year of accidental damage protection.
--- [prod_voltcharge65] VoltCharge 65W GaN Charger
65 W GaN fast charger. Price ₹2,499. Two USB-C ports and one USB-A, supports Power Delivery 3.1 and Quick Charge 5, foldable pins. Compatible with PulseBook 14, NovaTab 11 and all SoundWave headphones. Not sufficient to charge the PulseBook Pro 16 at full speed, which requires 100 W. 1-year manufacturer warranty.
--- [tsg_laptop_not_charging] Laptop Not Charging
If a PulseBook will not charge: 1) Confirm the charger wattage matches the model; the PulseBook Pro 16 needs 100 W and will charge very slowly or not at all on a 65 W unit. 2) Try the other Thunderbolt port; the right-hand port on the PulseBook 14 supports charging. 3) Inspect the cable for damage. 4) Hold the power button for 15 seconds to reset the embedded controller. 5) If the charging LED never illuminates with a known-good charger, raise a warranty service request.
--- [prod_voltcharge100] VoltCharge 100W GaN Charger
100 W GaN fast charger. Price ₹3,999. Two USB-C ports and one USB-A, supports Power Delivery 3.1 and Quick Charge 5, detachable braided cable included. Required for full-speed charging of the PulseBook Pro 16. Also charges the PulseBook 14, PulseBook Air 13, NovaTab and all SoundWave products. 1-year manufacturer warranty.

========== q019 [product_comparison] ==========
QUESTION: Which of your headphones is lighter and does it matter for long flights?
NEEDED DOCS: ['prod_x200', 'prod_y500']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
The **SoundWave X200** is lighter at **250 g**, versus **268 g** for the Y500—a difference of **18 g**.

For flights, the **Y500 is the recommended option** in our product guide because of its stronger **45 dB adaptive noise cancellation**, compared with the X200’s **35 dB ANC**. It also offers **60-hour rated battery life** versus **40 hours** for the X200, plus memory-foam earcups.

I don't have information about how much the 18 g weight difference affects comfort on long flights.

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
My recommendation is the **NovaTab Mini 8 + PulseBook 14**, for a total of **₹82,998**.

| Product | Price | Why pick it |
|---|---:|---|
| **NovaTab Mini 8** | ₹17,999 | Compact 8.4-inch display for reading, with 6 GB RAM and 128 GB expandable storage. Stylus not supported. |
| **PulseBook 14** | ₹64,999 | Core Ultra 5, 16 GB RAM and 512 GB SSD, weighing 1.29 kg—a balanced choice for college. |

**If you prefer a larger reading screen:** choose the **NovaTab 11 + PulseBook 14** for **₹94,998**. The tablet has an 11-inch 2.5K display, 8 GB RAM and 256 GB expandable storage. Adding its optional ₹4,999 stylus brings the total to **₹99,997**, still under ₹1,00,000.

I’d choose the **Mini 8 combination for compactness and savings**, or the **NovaTab 11 combination for a larger screen and stylus support**.

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

========== q021 [troubleshooting] ==========
QUESTION: My headphones will not pair with my phone.
NEEDED DOCS: ['tsg_headphone_pairing']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
If these are SoundWave headphones, try these steps:

1. Hold the power button for **7 seconds** until the LED flashes blue and white to enter pairing mode.
2. In your phone’s Bluetooth settings, forget any existing SoundWave entry.
3. Turn Bluetooth off for **10 seconds**, turn it back on, and select the headphones.
4. If multipoint is active, disconnect the headphones from any other device they’re connected to, then try again.
5. If the LED doesn’t flash at all, charge the headphones for **30 minutes** and retry.

What model are your headphones, and does the LED flash blue and white?

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_headphone_pairing] Headphones Will Not Pair
If SoundWave headphones will not pair: 1) Hold the power button for 7 seconds until the LED flashes blue and white, which puts the unit in pairing mode. 2) On the phone, forget any existing SoundWave entry in Bluetooth settings. 3) Disable Bluetooth for 10 seconds, re-enable, and select the device. 4) If multipoint is active the headphones may already be connected to another device; disconnect there first. 5) If the LED does not flash at all, charge for 30 minutes and retry.
--- [tsg_earbuds_one_side] Only One Earbud Working
If only one SoundWave earbud plays: 1) Place both buds in the case, close the lid for 10 seconds and reopen. 2) Forget the device in phone Bluetooth settings and re-pair. 3) Reset the buds by holding both touch panels for 15 seconds until the LED flashes red and white. 4) Clean the charging contacts on the silent bud with a dry cloth; contact dirt is the most common cause. 5) If the silent bud still does not charge, it is a warranty defect.
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [tsg_headphone_battery] Headphone Battery Draining Fast
Rapid battery drain on SoundWave headphones is usually caused by active noise cancellation combined with high volume. ANC reduces rated battery life by roughly 30 percent. Check for firmware updates in the SoundWave app, disable multipoint if two devices are not needed, and confirm the unit powers off rather than idling when removed. If runtime is below 50 percent of the rated figure with ANC off, the battery is considered defective and covered under warranty.

========== q022 [troubleshooting] ==========
QUESTION: My PulseBook is not charging.
NEEDED DOCS: ['tsg_laptop_not_charging']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Sorry your PulseBook isn’t charging. Please try these steps:

1. **Check the charger wattage matches your model.** The PulseBook Pro 16 needs **100 W** and may charge very slowly or not at all with a 65 W charger.
2. **Try the other Thunderbolt port.** On the PulseBook 14, the right-hand port supports charging.
3. **Inspect the cable for damage.**
4. **Hold the power button for 15 seconds** to reset the embedded controller.
5. If the charging LED never lights up with a known-good charger, a warranty service request is needed.

Which PulseBook model do you have, and what wattage is your charger?

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_laptop_not_charging] Laptop Not Charging
If a PulseBook will not charge: 1) Confirm the charger wattage matches the model; the PulseBook Pro 16 needs 100 W and will charge very slowly or not at all on a 65 W unit. 2) Try the other Thunderbolt port; the right-hand port on the PulseBook 14 supports charging. 3) Inspect the cable for damage. 4) Hold the power button for 15 seconds to reset the embedded controller. 5) If the charging LED never illuminates with a known-good charger, raise a warranty service request.
--- [tsg_earbuds_case_charge] Earbud Case Not Charging
If the charging case does not charge: confirm the cable is USB-C and carries data or power, try a different 5 V adapter, and check the LED responds when plugged in. A case left fully discharged for over a month may need 15 minutes before any LED appears. If no LED appears after 30 minutes on a known-good charger, raise a warranty claim.
--- [tsg_monitor_usbc_power] Monitor Not Charging Laptop over USB-C
The ClearView 27 supplies 90 W and the ClearView 32 Ultra supplies 140 W over USB-C. A PulseBook Pro 16 drawing 100 W will charge slowly from a ClearView 27 under sustained load. Confirm the cable is rated for both video and 100 W power delivery; many are not. Verify USB-C power delivery is enabled in the monitor menu, as it is off by default on some firmware.
--- [tsg_powerbank_not_charging] Power Bank Not Charging Devices
The VoltBank 20000 requires a double press of the power button to begin output for low-draw devices such as earbuds. For laptops, use the 65 W USB-C port, not the USB-A port. If the capacity display shows charge but no output occurs on any port, raise a warranty claim.

========== q023 [troubleshooting] ==========
QUESTION: My AuraWatch will not sync with the app.
NEEDED DOCS: ['tsg_watch_sync']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
If you have an **AuraWatch 3**, please try these steps:

1. Confirm the companion app has **Bluetooth** and **background-activity** permissions.
2. Check that your phone runs **Android 9 or later** or **iOS 14 or later**.
3. On Android, exclude the app from **battery optimisation**—this is the most common cause of background syncing problems.
4. Force-close and reopen the app.
5. Ensure the watch firmware is current.

Is your watch an AuraWatch 3 or AuraWatch Pro? I don't have information about AuraWatch Pro sync troubleshooting.

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_watch_sync] Smartwatch Not Syncing
If AuraWatch 3 will not sync: confirm the companion app has Bluetooth and background-activity permission, confirm the phone runs Android 9 or later or iOS 14 or later, force-close and reopen the app, and ensure the watch firmware is current. Battery optimisation settings on some Android phones stop the app in the background and are the most common cause; exclude the app from optimisation.
--- [tsg_watch_inaccurate_hr] Heart Rate Readings Inaccurate
Optical heart-rate sensors need firm skin contact. Wear the watch one finger-width above the wrist bone, snug but not tight. Tattoos, very cold skin and loose fits all reduce accuracy. If readings remain implausible when stationary after adjusting fit, the sensor is a warranty defect.
--- [prod_aurawatch3] AuraWatch 3 Smartwatch
Fitness smartwatch. Price ₹8,999. 1.4-inch AMOLED display, 14-day battery, heart-rate and SpO2 sensors, built-in GPS, 5 ATM water resistance, sleep tracking. Compatible with Android 9 and above and iOS 14 and above. 1-year manufacturer warranty. Worn on the wrist, therefore non-returnable once used, under the hygiene policy.
--- [prod_aurawatch_pro] AuraWatch Pro Smartwatch
Premium fitness smartwatch. Price ₹15,999. 1.5-inch AMOLED always-on display, 18-day battery, ECG and SpO2 sensors, dual-band GPS, 10 ATM water resistance, offline maps, 100 sport modes. Compatible with Android 10 and above and iOS 15 and above. 2-year manufacturer warranty. Non-returnable once used, under the hygiene policy.

========== q024 [troubleshooting] ==========
QUESTION: My monitor says no signal.
NEEDED DOCS: ['tsg_monitor_no_signal']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
If your monitor is a ClearView 27, try these steps:

1. Confirm the input source in the monitor’s on-screen menu matches the cable you’re using.
2. If using USB-C, confirm your laptop’s port supports DisplayPort Alt Mode. The PulseBook USB-A port does not.
3. Try a different cable—many USB-C cables carry power but not video.
4. For 4K at 144 Hz, use DisplayPort 1.4 or HDMI 2.1; older cables cap the refresh rate.
5. Reset the monitor to factory defaults from its menu.

Which monitor model do you have, and what cable are you using?

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
I’m sorry your headphones aren’t lasting as expected. For SoundWave headphones, try these checks:

1. **Turn off ANC and lower the volume.** ANC reduces rated battery life by roughly 30%, and high volume also contributes to rapid drain.
2. **Check for firmware updates** in the SoundWave app.
3. **Disable multipoint** if you don’t need multiple devices connected.
4. **Confirm the headphones power off**, rather than idle, when removed.
5. **Measure runtime with ANC off.** If it’s below 50% of the rated battery life, the battery is considered defective and covered under warranty.

Which model do you have, how long does a full charge last, and is ANC usually on?

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_headphone_battery] Headphone Battery Draining Fast
Rapid battery drain on SoundWave headphones is usually caused by active noise cancellation combined with high volume. ANC reduces rated battery life by roughly 30 percent. Check for firmware updates in the SoundWave app, disable multipoint if two devices are not needed, and confirm the unit powers off rather than idling when removed. If runtime is below 50 percent of the rated figure with ANC off, the battery is considered defective and covered under warranty.
--- [tsg_watch_battery] Smartwatch Battery Draining Fast
Always-on display reduces AuraWatch Pro battery life from 18 days to roughly 6. Continuous SpO2 monitoring and dual-band GPS also shorten runtime substantially. Disable always-on display and continuous SpO2 to restore rated life. If runtime is under 50 percent of the rated figure with those features off, the battery is a warranty defect.
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [prod_y500] SoundWave Y500 Premium Headphones
Flagship over-ear wireless headphones. Price ₹24,999. 60-hour battery life, Bluetooth 5.4, adaptive active noise cancellation rated at 45 dB with transparency mode, LDAC and aptX Lossless support, USB-C and wireless charging, multipoint pairing with three devices, 268 g, memory-foam earcups. Available in Graphite and Sand. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy. Recommended over the X200 for noisy environments such as open-plan offices and flights.

========== q026 [billing_dispute] ==========
QUESTION: I was charged 12,999 three times for order 48712. Two were supposed to be cancelled but I only see one refund. Where is my money?
NEEDED DOCS: ['bill_duplicate_charge', 'pol_refund_timeline']   MISSING FROM WHAT THE MODEL SAW: ['pol_refund_timeline']

ANSWER:
I understand why seeing three charges is worrying. Your records show **one order #48712**, not three separate orders. The extra two entries were duplicate authorisation holds, rather than payments for additional orders.

Here’s where each ₹12,999 entry stands:

| Charge date | Amount | Status |
|---|---:|---|
| 27 September 2026 | ₹12,999 | Settled payment for order #48712, which is still Processing. |
| 27 September 2026 | ₹12,999 | Duplicate hold reversed on **29 September 2026**—this matches the one reversal you’re seeing. |
| 27 September 2026 | ₹12,999 | Duplicate hold awaiting reversal, due **by 4 October 2026**. |

**What happens next:**
1. The remaining ₹12,999 hold should reverse automatically. The policy timeframe is **“5 to 7 business days”**; your record specifically lists 4 October as the reversal deadline.
2. As of today, 30 September, that reversal is **not overdue**.
3. Once it reverses, only the ₹12,999 payment for order #48712 should remain. If it hasn’t reversed by 4 October, I can connect you with a human agent to investigate.

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_cancellation] Order Cancellation
An order can be cancelled free of charge at any time before it is marked Shipped. Once shipped, cancellation is not possible; the customer should refuse delivery or raise a return after delivery. Cancelled orders are refunded in full, including any delivery charge paid, within 5 to 7 business days.
--- [bill_duplicate_charge] Duplicate or Multiple Charges
A duplicate charge occurs when a payment page is submitted more than once. Only one order is created; the additional authorisations are holds that reverse automatically within 5 to 7 business days. If two or more distinct orders were created, each must be cancelled separately and each refund is processed separately, so a customer may see refunds arrive on different days. When resolving a multi-charge dispute, list every charge with its date and amount, state which one corresponds to the surviving order, and give the expected reversal date for each of the others.
--- [bill_chargeback] Bank Chargebacks and Disputes
If a customer raises a chargeback with their bank, the order is frozen and any parallel TechStore refund is suspended to prevent a double credit. Chargebacks take 45 to 90 days to resolve through the card network. Contacting support directly is almost always faster than a chargeback, and support can withdraw a chargeback by providing the bank with resolution evidence.
--- [bill_cod_refund] Refunds on Cash-on-Delivery Orders
Cash-on-delivery orders cannot be refunded to a payment method because none was used. Refunds are made by bank transfer after the customer submits account number and IFSC through the secure link sent by support. Transfers complete within 5 to 7 business days of verification. The ₹49 COD handling fee is refunded only if the order is cancelled before dispatch.
--- ORDER 48712
{"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== q027 [billing_dispute] ==========
QUESTION: My payment failed but the money was debited. No order was created. What happens now?
NEEDED DOCS: ['bill_failed_payment']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
The debit is a **temporary bank hold** that is released automatically. The reversal timeframe depends on your payment method:

- **Card or UPI:** within **5 to 7 business days**.
- **Net banking:** up to **10 business days**.

No order is created for a failed payment, so there is nothing to cancel.

If the money has not reversed after the applicable period, contact support with your **bank reference number**. TechStore will raise a **chargeback trace with the payment gateway**.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_failed_payment] Payment Failed but Money Debited
If a payment fails but the amount is debited, the bank has placed a temporary hold that is released automatically. Card and UPI holds reverse within 5 to 7 business days; net banking can take up to 10. No order is created for a failed payment, so there is nothing to cancel. If the amount has not reversed after the stated period, contact support with the bank reference number and TechStore raises a chargeback trace with the payment gateway.
--- [acc_order_history] Order History and Invoices
All orders from the past 8 years are visible under Orders in the account, with status, tracking and downloadable invoice. Orders placed as part of a cancelled payment attempt do not appear, because no order is created for a failed payment.
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.
--- [ship_failed_delivery] Failed Delivery Attempts
The courier makes three delivery attempts on consecutive business days. After the third failed attempt the parcel is returned to our warehouse and the order is refunded in full, including any delivery charge paid, within 7 business days of the parcel being received back. A customer can reschedule delivery once through the tracking link.

========== q028 [billing_dispute] ==========
QUESTION: I returned one item from a two-item order but my refund is less than the item price. Why?
NEEDED DOCS: ['bill_refund_partial']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
For a partial return, the refund covers the returned item’s value, but two terms may explain the difference:

- **Delivery charge:** “The delivery charge is refunded only if the entire order is returned.” Returning one of two items does not qualify.
- **Promotional discount:** If the promotion required a minimum basket value and the remaining item falls below it, “the discount is recalculated and the difference deducted from the refund.”

I don't have information about your order’s item prices, delivery charge, promotional discount, or refund amount, so I can’t confirm the exact deduction; a human agent can review the billing breakdown.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_refund_partial] Partial Refunds on Multi-Item Orders
When only some items in an order are returned, the refund covers the returned items' value. The delivery charge is refunded only if the entire order is returned. If a promotional discount applied to the order required a minimum basket value and the remaining items fall below it, the discount is recalculated and the difference deducted from the refund.
--- [bill_price_drop] Price Drop After Purchase
If a product's TechStore price drops within 7 days of purchase, the difference is refunded on request. This applies once per order line and does not apply during flash sales, festive events or clearance. This is distinct from the price match guarantee, which covers competitor pricing.
--- [bill_duplicate_charge] Duplicate or Multiple Charges
A duplicate charge occurs when a payment page is submitted more than once. Only one order is created; the additional authorisations are holds that reverse automatically within 5 to 7 business days. If two or more distinct orders were created, each must be cancelled separately and each refund is processed separately, so a customer may see refunds arrive on different days. When resolving a multi-charge dispute, list every charge with its date and amount, state which one corresponds to the surviving order, and give the expected reversal date for each of the others.
--- [pol_price_match] Price Match Guarantee
If a customer finds the identical product cheaper on a competing authorised Indian retailer within 7 days of their purchase, TechStore refunds the difference. The competing listing must be for a new, sealed unit sold and shipped by the retailer itself, not a marketplace seller. Price matching does not apply during flash sales or clearance events.

========== q029 [billing_dispute] ==========
QUESTION: I bought on no-cost EMI and returned the product. The bank is still charging me interest. Who pays that?
NEEDED DOCS: ['bill_emi', 'pol_refund_timeline']   MISSING FROM WHAT THE MODEL SAW: ['pol_refund_timeline']

ANSWER:
Under the **“No-Cost EMI”** terms, TechStore absorbs the interest as an upfront discount. If you return the order, that discount is deducted from your refund, and **the bank may still charge interest already levied**—so you may still have to pay that interest.

Next steps:
1. Contact your bank to cancel the EMI plan.
2. Ask the bank to confirm the interest already levied and any amount still payable.

I don't have information about your order’s charges, discount amount, or refund amount.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_emi] EMI and No-Cost EMI
EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount. If an order paid by no-cost EMI is returned, the discount is deducted from the refund and the bank may still charge interest already levied; the bank must be contacted to cancel the EMI plan.
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.
--- [bill_chargeback] Bank Chargebacks and Disputes
If a customer raises a chargeback with their bank, the order is frozen and any parallel TechStore refund is suspended to prevent a double credit. Chargebacks take 45 to 90 days to resolve through the card network. Contacting support directly is almost always faster than a chargeback, and support can withdraw a chargeback by providing the bank with resolution evidence.
--- [prod_voltbank20k] VoltBank 20000mAh Power Bank
20000 mAh power bank. Price ₹2,999. 65 W USB-C output, 20 W USB-A output, pass-through charging, LED capacity display, 389 g. Its capacity is under 100 Wh; check your airline's rules before carrying it on a flight. Can charge the PulseBook Air 13 once or the NovaTab 11 twice. 1-year manufacturer warranty.

========== q030 [billing_dispute] ==========
QUESTION: I forgot to add my GSTIN at checkout on order 48750. Can you reissue the invoice so I can claim input credit?
NEEDED DOCS: ['bill_invoice_gst']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
I’m sorry, but we can’t reissue the invoice for order #48750 to add your GSTIN. Under our invoice policy, business customers must enter their GSTIN “at checkout, before placing the order.” TechStore “cannot add a GSTIN to an invoice afterwards” and “does not issue a fresh invoice for a completed order.”

Your existing invoice remains downloadable from Orders for 8 years. I don't have information about your eligibility to claim input credit without the GSTIN on this invoice.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_invoice_gst] Invoice and GST
A tax invoice is emailed within 24 hours of dispatch and is downloadable from Orders. Business customers who need their GSTIN on the invoice must enter it at checkout, before placing the order. TechStore cannot add a GSTIN to an invoice afterwards and does not issue a fresh invoice for a completed order. Invoices remain downloadable for 8 years.
--- [pol_bulk_orders] Bulk and Business Orders
Orders above 10 units of a single SKU are treated as business orders and require a GSTIN. Bulk pricing is quoted by the business desk and is not available at checkout. Business orders ship in 5 to 10 business days and carry a 15-day return window rather than 30 days.
--- [pol_warranty_claim] How to Raise a Warranty Claim
To claim warranty, raise a service request from Orders in the account, or contact support with the order ID. TechStore arranges a free pickup for products above ₹5,000; smaller items are shipped by the customer and reimbursed up to ₹200. Diagnosis takes 3 to 5 business days at the service centre. If the unit is found defective it is repaired or replaced; if no fault is found it is returned at no charge.
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.
--- ORDER 48750
{"order_id": "48750", "customer_id": "cust_8123", "email": "arjun.t@example.com", "placed_at": "2026-08-24", "status": "Delivered", "items": [{"sku": "prod_pulsebook_pro16", "name": "PulseBook Pro 16 Laptop", "qty": 1, "unit_price": 134999}], "total": 134999, "payment_method": "Credit Card", "delivery_pin": "122018", "courier": "BlueDart", "tracking_id": "BD4470012288", "delivered_at": "2026-08-25", "charges": [{"date": "2026-08-24", "amount": 134999, "type": "capture", "status": "settled"}]}

========== q031 [technical_api] ==========
QUESTION: Your webhook returns 403 even though my HMAC signature is valid. Here is my Python: sig = hmac.new(secret, json.dumps(request.json).encode(), 'sha256').hexdigest()
NEEDED DOCS: ['api_webhook_signature']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Your code computes the HMAC over re-serialised JSON, not the original raw request body. `json.dumps(request.json)` can change whitespace and key order, so a correctly calculated HMAC can still fail verification.

1. Capture the **exact raw request-body bytes before any JSON parsing**.
2. Compute the signature using those bytes:
   ```python
   sig = hmac.new(webhook_secret, raw_body, 'sha256').hexdigest()
   ```
3. Use the **webhook secret**, not your API token, as the HMAC key.
4. Compare the hex-encoded result with the `X-TechStore-Signature` header.

If the 403 includes `insufficient_scope`, it indicates a token-scope issue rather than a signature failure. Scopes cannot be widened after token creation; issue a new token with the required scope instead.

EVIDENCE THE MODEL WAS GIVEN:
--- [api_webhook_signature] Webhook Signature Verification and 403 Errors
Every webhook carries an X-TechStore-Signature header containing an HMAC-SHA256 of the raw request body, keyed with the webhook secret, hex encoded. A 403 returned by our delivery checker almost always means the signature was computed over a parsed and re-serialised body rather than the raw bytes; JSON re-serialisation changes key order and whitespace and therefore changes the HMAC. Compute the HMAC over the exact raw body before any JSON parsing. The second most common cause is using the API token instead of the webhook secret as the HMAC key.
--- [api_scopes] Token Scopes and 403 Errors
Tokens carry scopes: orders:read, orders:write, inventory:read, shipments:read, webhooks:manage. A 403 with code insufficient_scope means the token is valid but lacks the required scope, which is different from a signature failure. Scopes are set when the token is created and cannot be widened afterwards; issue a new token instead.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_webhook_retries] Webhook Delivery and Retries
Webhooks expect a 2xx response within 5 seconds. Non-2xx or timeout triggers retries at 1, 5, 25 and 125 minutes, then the endpoint is marked unhealthy and deliveries pause until reactivated in the dashboard. Handlers must be idempotent, because a duplicate delivery is possible even after a successful response. Each delivery carries an X-TechStore-Delivery-Id that is stable across retries.

========== q032 [technical_api] ==========
QUESTION: I am getting 409 on order creation when I retry after a timeout. What am I doing wrong?
NEEDED DOCS: ['api_idempotency', 'api_error_codes']   MISSING FROM WHAT THE MODEL SAW: ['api_idempotency']

ANSWER:
A **409 means an idempotency conflict**: you reused the same `Idempotency-Key` with a different payload.

1. **Check the retry payload against the original request.** For a POST retry after a timeout, use the **same `Idempotency-Key` and the same payload**.
2. **Don’t switch to a new key just because the request timed out.** Requests time out server-side at 30 seconds, but a timeout does not tell you whether order creation completed. Using the same key avoids duplicates.
3. **Retry with exponential backoff and jitter**, rather than immediately in a tight loop, which can trigger rate limiting.

The likely issue is that something in your order-creation payload changed between the original request and the retry.

EVIDENCE THE MODEL WAS GIVEN:
--- [api_timeouts] API Timeouts and Retry Safety
Requests time out server side at 30 seconds. A timeout does not indicate whether the operation completed, so POST requests must be retried with the same Idempotency-Key to avoid duplicates. GET, PUT and DELETE are idempotent by design and safe to retry. Retries should use exponential backoff with jitter; retrying immediately in a tight loop triggers rate limiting.
--- [api_rate_limits] API Rate Limits and 429 Errors
The Partner API allows 600 requests per minute per token, and 60 per minute for the bulk export endpoints. Exceeding the limit returns 429 with a Retry-After header in seconds. Clients should honour Retry-After and use exponential backoff with jitter. Sustained violation for more than 15 minutes results in a temporary 1-hour block.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [ship_failed_delivery] Failed Delivery Attempts
The courier makes three delivery attempts on consecutive business days. After the third failed attempt the parcel is returned to our warehouse and the order is refunded in full, including any delivery charge paid, within 7 business days of the parcel being received back. A customer can reschedule delivery once through the tracking link.

========== q033 [technical_api] ==========
QUESTION: My integration worked in sandbox but returns 401 in production with the same code. Why?
NEEDED DOCS: ['api_auth', 'api_overview']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
The most common cause is using a **sandbox token in production**. Sandbox and production require separate credentials, even when your code is unchanged.

1. Confirm your production requests use `https://api.techstore.example/v1`.
2. Send a production token in the header: `Authorization: Bearer <token>`.
3. Check that the token is present, correctly formatted, and not expired. Tokens expire **90 days after issue**.
4. If needed, rotate the token in the partner dashboard. The previous token remains valid for **24 hours after rotation**, allowing a switch without downtime.

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
The **600 requests per minute per token** limit is the general Partner API limit. **Bulk export endpoints have a separate limit of 60 requests per minute**, so 100 requests per minute exceeds that limit and triggers 429 responses.

1. Reduce your bulk export request rate to no more than 60 per minute.
2. Honour the 429 response’s `Retry-After` header, which specifies the wait in seconds.
3. Use exponential backoff with jitter for retries rather than retrying immediately.

Sustained limit violations for more than 15 minutes result in a temporary **1-hour block**.

EVIDENCE THE MODEL WAS GIVEN:
--- [api_rate_limits] API Rate Limits and 429 Errors
The Partner API allows 600 requests per minute per token, and 60 per minute for the bulk export endpoints. Exceeding the limit returns 429 with a Retry-After header in seconds. Clients should honour Retry-After and use exponential backoff with jitter. Sustained violation for more than 15 minutes results in a temporary 1-hour block.
--- [pol_bulk_orders] Bulk and Business Orders
Orders above 10 units of a single SKU are treated as business orders and require a GSTIN. Bulk pricing is quoted by the business desk and is not available at checkout. Business orders ship in 5 to 10 business days and carry a 15-day return window rather than 30 days.
--- [api_timeouts] API Timeouts and Retry Safety
Requests time out server side at 30 seconds. A timeout does not indicate whether the operation completed, so POST requests must be retried with the same Idempotency-Key to avoid duplicates. GET, PUT and DELETE are idempotent by design and safe to retry. Retries should use exponential backoff with jitter; retrying immediately in a tight loop triggers rate limiting.
--- [api_idempotency] API Idempotency
All POST endpoints accept an Idempotency-Key header. A repeated request with the same key and an identical payload returns the original response without creating a second resource. A repeated key with a different payload returns 409. Keys are retained for 24 hours. Clients should generate a UUID per logical operation, not per HTTP attempt, so that retries reuse the same key.

========== q035 [technical_api] ==========
QUESTION: A valid order ID returns 404 for my token but works in the dashboard. What is happening?
NEEDED DOCS: ['api_error_codes', 'api_auth']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
A **404** can occur even for a valid order ID if the order belongs to a **different partner** than the one associated with your token. That could explain why it works in the dashboard but not through the API.

1. Check that your token belongs to the partner that owns the order.
2. Check that you’re requesting the intended order ID.

A missing scope would return **403 `insufficient_scope`**, not 404.

EVIDENCE THE MODEL WAS GIVEN:
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_scopes] Token Scopes and 403 Errors
Tokens carry scopes: orders:read, orders:write, inventory:read, shipments:read, webhooks:manage. A 403 with code insufficient_scope means the token is valid but lacks the required scope, which is different from a signature failure. Scopes are set when the token is created and cannot be widened afterwards; issue a new token instead.
--- [api_auth] API Authentication and 401 Errors
Authenticate with Authorization: Bearer <token>. A 401 means the token is missing, malformed, expired or from the wrong environment; sandbox tokens rejected by production is the most common cause. Tokens expire 90 days after issue and can be rotated in the dashboard without downtime, since the previous token stays valid for 24 hours after rotation.
--- [api_webhook_signature] Webhook Signature Verification and 403 Errors
Every webhook carries an X-TechStore-Signature header containing an HMAC-SHA256 of the raw request body, keyed with the webhook secret, hex encoded. A 403 returned by our delivery checker almost always means the signature was computed over a parsed and re-serialised body rather than the raw bytes; JSON re-serialisation changes key order and whitespace and therefore changes the HMAC. Compute the HMAC over the exact raw body before any JSON parsing. The second most common cause is using the API token instead of the webhook secret as the HMAC key.

========== q036 [policy_edge_case] ==========
QUESTION: I bought a PulseBook 35 days ago and it is faulty. Your return window is 30 days but the warranty is 2 years. What are my rights?
NEEDED DOCS: ['pol_return_window', 'pol_warranty_terms', 'pol_warranty_claim']   MISSING FROM WHAT THE MODEL SAW: ['pol_warranty_claim']

ANSWER:
You may still have warranty support even if you’re outside the return window.

- **Returns:** TechStore’s **“30-day return window”** starts from the delivery date shown on tracking—not the purchase date. Buying your PulseBook 35 days ago does not necessarily mean you’re outside it. A return raised on day 31 or later after delivery is rejected automatically.
- **Warranty:** Warranty also starts from delivery and is **independent of the 30-day return window**. If your product page states a two-year manufacturer warranty, a qualifying fault may still be repaired or replaced under warranty.
- **Covered faults:** Warranty covers manufacturing defects and component failure under normal use. It excludes physical damage, liquid ingress, unauthorised repair, and normal battery capacity decline above 80 percent of rated capacity.

I don't have information about your PulseBook’s confirmed warranty duration, delivery date, or the nature of the fault.

What date was it delivered, and what fault are you experiencing?

EVIDENCE THE MODEL WAS GIVEN:
--- [svc_accidental_damage] Accidental Damage Protection
PulseBook 14 and PulseBook Pro 16 include one year of accidental damage protection from the delivery date, covering drops and liquid spills. One claim is permitted in the coverage year, with a customer contribution of 10 percent of the product price. Accidental damage protection does not cover theft, loss, or cosmetic damage that does not affect function.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [pol_return_window] Return Window
TechStore accepts returns within 30 days of delivery. The 30 days are counted from the delivery date shown on the tracking record, not the order date. Items must be returned in their original packaging with all accessories, manuals and free gifts included. A return raised on day 31 or later is rejected automatically by the returns system.
--- [pol_warranty_terms] Standard Warranty Terms
All products carry the manufacturer warranty stated on the product page, counted from the delivery date. Warranty covers manufacturing defects and component failure under normal use. It does not cover physical damage, liquid ingress, unauthorised repair, or normal battery capacity decline above 80 percent of the rated capacity. Warranty is independent of the 30-day return window: a product outside the return window may still be repaired or replaced under warranty.

========== q037 [policy_edge_case] ==========
QUESTION: I opened my Y500 headphones and they are defective. You say opened headphones are non-returnable. Am I stuck with broken headphones?
NEEDED DOCS: ['pol_return_exclusions', 'pol_warranty_terms']   MISSING FROM WHAT THE MODEL SAW: ['pol_warranty_terms']

ANSWER:
No—you’re not stuck with broken headphones. The **“non-returnable once the seal is broken”** hygiene exclusion applies to returns, but **“a hygiene exclusion never removes warranty rights.”**

Your SoundWave Y500 headphones have a **2-year manufacturer warranty**, and faulty headphones remain covered even after opening. I can connect you with a human agent to help with your warranty claim.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_y500] SoundWave Y500 Premium Headphones
Flagship over-ear wireless headphones. Price ₹24,999. 60-hour battery life, Bluetooth 5.4, adaptive active noise cancellation rated at 45 dB with transparency mode, LDAC and aptX Lossless support, USB-C and wireless charging, multipoint pairing with three devices, 268 g, memory-foam earcups. Available in Graphite and Sand. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy. Recommended over the X200 for noisy environments such as open-plan offices and flights.
--- [pol_return_exclusions] Non-Returnable Items
For hygiene reasons the following are non-returnable once the seal is broken: headphones of every type (over-ear, on-ear and in-ear), earbuds, fitness bands worn on the wrist, and any personal grooming device. Opened software licences and redeemed digital gift cards are also non-returnable. These items remain covered by warranty if they are faulty; a hygiene exclusion never removes warranty rights.
--- [tsg_headphone_pairing] Headphones Will Not Pair
If SoundWave headphones will not pair: 1) Hold the power button for 7 seconds until the LED flashes blue and white, which puts the unit in pairing mode. 2) On the phone, forget any existing SoundWave entry in Bluetooth settings. 3) Disable Bluetooth for 10 seconds, re-enable, and select the device. 4) If multipoint is active the headphones may already be connected to another device; disconnect there first. 5) If the LED does not flash at all, charge for 30 minutes and retry.
--- [tsg_earbuds_one_side] Only One Earbud Working
If only one SoundWave earbud plays: 1) Place both buds in the case, close the lid for 10 seconds and reopen. 2) Forget the device in phone Bluetooth settings and re-pair. 3) Reset the buds by holding both touch panels for 15 seconds until the LED flashes red and white. 4) Clean the charging contacts on the silent bud with a dry cloth; contact dirt is the most common cause. 5) If the silent bud still does not charge, it is a warranty defect.

========== q038 [policy_edge_case] ==========
QUESTION: I spilled coffee on my PulseBook 14 four months after delivery. Warranty excludes liquid damage. Is there anything that covers me?
NEEDED DOCS: ['pol_warranty_terms', 'svc_accidental_damage']   MISSING FROM WHAT THE MODEL SAW: ['pol_warranty_terms']

ANSWER:
Yes—your PulseBook 14 includes **“one year of accidental damage protection”** from the delivery date, covering **“drops and liquid spills.”** A coffee spill four months after delivery falls within that coverage period.

- **Claim limit:** One claim in the coverage year, so coverage depends on whether you’ve already used it.
- **Your contribution:** “10 percent of the product price”—₹6,499.90 based on the listed price of ₹64,999.
- **Exclusion:** Cosmetic damage that does not affect function is not covered.

I can connect you with a human agent to help submit an accidental damage claim.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_pulsebook14] PulseBook 14 Laptop
14-inch ultrabook. Price ₹64,999. Intel Core Ultra 5, 16 GB LPDDR5 RAM, 512 GB NVMe SSD, 14-inch 2.8K OLED display at 90 Hz, 65 W USB-C charging, 1.29 kg, 12-hour rated battery. Ports: two USB-C Thunderbolt, one USB-A, HDMI 2.1, headphone jack. 2-year manufacturer warranty including one year of accidental damage protection.
--- [svc_accidental_damage] Accidental Damage Protection
PulseBook 14 and PulseBook Pro 16 include one year of accidental damage protection from the delivery date, covering drops and liquid spills. One claim is permitted in the coverage year, with a customer contribution of 10 percent of the product price. Accidental damage protection does not cover theft, loss, or cosmetic damage that does not affect function.
--- [prod_pulsebook_pro16] PulseBook Pro 16 Laptop
16-inch creator laptop. Price ₹1,34,999. Intel Core Ultra 9, 32 GB RAM, 1 TB NVMe SSD, discrete RTX 4060 graphics, 16-inch 3.2K OLED at 120 Hz, 100 W USB-C charging, 1.95 kg. 2-year manufacturer warranty including one year of accidental damage protection.
--- [tsg_laptop_not_charging] Laptop Not Charging
If a PulseBook will not charge: 1) Confirm the charger wattage matches the model; the PulseBook Pro 16 needs 100 W and will charge very slowly or not at all on a 65 W unit. 2) Try the other Thunderbolt port; the right-hand port on the PulseBook 14 supports charging. 3) Inspect the cable for damage. 4) Hold the power button for 15 seconds to reset the embedded controller. 5) If the charging LED never illuminates with a known-good charger, raise a warranty service request.

========== q039 [policy_edge_case] ==========
QUESTION: The courier failed three delivery attempts while I was travelling and the order was returned. I was not told. Do I get a full refund including the delivery charge?
NEEDED DOCS: ['ship_failed_delivery', 'ship_charges']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Yes. Under the “Failed Delivery Attempts” policy, after the third failed attempt, the parcel is returned to our warehouse and the order is **“refunded in full, including any delivery charge paid,” within 7 business days of the parcel being received back**.

I don't have information about whether you were notified or when your parcel reached the warehouse.

EVIDENCE THE MODEL WAS GIVEN:
--- [ship_failed_delivery] Failed Delivery Attempts
The courier makes three delivery attempts on consecutive business days. After the third failed attempt the parcel is returned to our warehouse and the order is refunded in full, including any delivery charge paid, within 7 business days of the parcel being received back. A customer can reschedule delivery once through the tracking link.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [bill_cod_refund] Refunds on Cash-on-Delivery Orders
Cash-on-delivery orders cannot be refunded to a payment method because none was used. Refunds are made by bank transfer after the customer submits account number and IFSC through the secure link sent by support. Transfers complete within 5 to 7 business days of verification. The ₹49 COD handling fee is refunded only if the order is cancelled before dispatch.
--- [ship_charges] Delivery Charges
Delivery is free on all orders above ₹999. Below that a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149 and is available in metro cities only for orders placed before 2 PM. Delivery charges are refunded if the order is cancelled before shipping or if the item arrives damaged.

========== q040 [policy_edge_case] ==========
QUESTION: I found the X200 cheaper elsewhere 6 days after buying, but it was during their clearance sale. Does your price match apply?
NEEDED DOCS: ['pol_price_match']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No. Although you found the X200 cheaper within the “7 days of their purchase” window, the Price Match Guarantee states: “Price matching does not apply during flash sales or clearance events.” The competitor’s clearance-sale price is therefore not eligible.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [pol_price_match] Price Match Guarantee
If a customer finds the identical product cheaper on a competing authorised Indian retailer within 7 days of their purchase, TechStore refunds the difference. The competing listing must be for a new, sealed unit sold and shipped by the retailer itself, not a marketplace seller. Price matching does not apply during flash sales or clearance events.
--- [bill_price_drop] Price Drop After Purchase
If a product's TechStore price drops within 7 days of purchase, the difference is refunded on request. This applies once per order line and does not apply during flash sales, festive events or clearance. This is distinct from the price match guarantee, which covers competitor pricing.
--- [pol_exchange] Exchange Policy
An exchange can be requested within 30 days of delivery for a different size, colour or variant of the same product line, subject to stock. If the new variant costs more, the difference is charged before dispatch. If it costs less, the difference is refunded. Only one exchange is permitted per order line.

========== q041 [out_of_scope] ==========
QUESTION: What is the capital of France?
EXPECTED BEHAVIOUR (out of scope): decline_off_topic
NEEDED DOCS: []   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
I can only help with TechStore orders, products, and support.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_clearview27] ClearView 27 Monitor
27-inch monitor. Price ₹22,999. 4K UHD IPS panel, 144 Hz refresh, 1 ms response, 95 percent DCI-P3 colour coverage, USB-C with 90 W power delivery, height and pivot adjustable stand, VESA 100 mount. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.
--- [prod_novatab11] NovaTab 11 Tablet
11-inch Android tablet. Price ₹29,999. Snapdragon 7 Gen 3, 8 GB RAM, 256 GB storage expandable by microSD, 11-inch 2.5K LCD at 120 Hz, 8000 mAh battery, stylus supported and sold separately at ₹4,999. 1-year manufacturer warranty.
--- [ship_international] International Shipping
TechStore ships within India only. We do not ship to international addresses and cannot deliver to APO or diplomatic addresses. Orders placed with an international billing address but an Indian delivery address are accepted.
--- [prod_novatab_mini8] NovaTab Mini 8 Tablet
8-inch compact Android tablet. Price ₹17,999. Snapdragon 6 Gen 1, 6 GB RAM, 128 GB storage expandable by microSD, 8.4-inch 1920x1200 LCD at 90 Hz, 5500 mAh battery. Stylus is not supported on the Mini 8; stylus support is exclusive to the NovaTab 11. 1-year manufacturer warranty.

========== q042 [out_of_scope] ==========
QUESTION: Can you write me a short poem about the monsoon?
EXPECTED BEHAVIOUR (out of scope): decline_off_topic
NEEDED DOCS: []   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
I can only help with TechStore orders, products, and support.

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_laptop_overheating] Laptop Overheating
Surface temperatures up to 45 C under sustained load are within specification. If the machine thermally throttles or shuts down: ensure the vents are unobstructed and not used on fabric, clean the intake grilles with compressed air, and update the BIOS. Shutdowns under light load indicate a fan or sensor fault and are covered by warranty.
--- [acc_create] Creating and Verifying an Account
An account is created with an email address or an Indian mobile number and verified by a one-time password valid for 10 minutes. A maximum of five OTPs may be requested per hour. An account is required to place an order; guest checkout is not offered.
--- [prod_novatab_mini8] NovaTab Mini 8 Tablet
8-inch compact Android tablet. Price ₹17,999. Snapdragon 6 Gen 1, 6 GB RAM, 128 GB storage expandable by microSD, 8.4-inch 1920x1200 LCD at 90 Hz, 5500 mAh battery. Stylus is not supported on the Mini 8; stylus support is exclusive to the NovaTab 11. 1-year manufacturer warranty.
--- [ship_international] International Shipping
TechStore ships within India only. We do not ship to international addresses and cannot deliver to APO or diplomatic addresses. Orders placed with an international billing address but an Indian delivery address are accepted.

========== q043 [out_of_scope] ==========
QUESTION: Who won the last cricket World Cup?
EXPECTED BEHAVIOUR (out of scope): decline_off_topic
NEEDED DOCS: []   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
I can only help with TechStore orders, products, and support.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_aurawatch_pro] AuraWatch Pro Smartwatch
Premium fitness smartwatch. Price ₹15,999. 1.5-inch AMOLED always-on display, 18-day battery, ECG and SpO2 sensors, dual-band GPS, 10 ATM water resistance, offline maps, 100 sport modes. Compatible with Android 10 and above and iOS 15 and above. 2-year manufacturer warranty. Non-returnable once used, under the hygiene policy.
--- [prod_aurawatch3] AuraWatch 3 Smartwatch
Fitness smartwatch. Price ₹8,999. 1.4-inch AMOLED display, 14-day battery, heart-rate and SpO2 sensors, built-in GPS, 5 ATM water resistance, sleep tracking. Compatible with Android 9 and above and iOS 14 and above. 1-year manufacturer warranty. Worn on the wrist, therefore non-returnable once used, under the hygiene policy.
--- [svc_centres] Service Centre Network
TechStore operates authorised service centres in 48 Indian cities. The nearest centre can be found by pin code on the Support page. Walk-in service is available for laptops and monitors; headphones, watches and tablets are handled by courier pickup only. Carry the invoice or order ID for any walk-in visit.
--- [prod_pulsebook_pro16] PulseBook Pro 16 Laptop
16-inch creator laptop. Price ₹1,34,999. Intel Core Ultra 9, 32 GB RAM, 1 TB NVMe SSD, discrete RTX 4060 graphics, 16-inch 3.2K OLED at 120 Hz, 100 W USB-C charging, 1.95 kg. 2-year manufacturer warranty including one year of accidental damage protection.

========== q044 [out_of_scope] ==========
QUESTION: Do you offer a student discount?
EXPECTED BEHAVIOUR (out of scope): admit_unknown
NEEDED DOCS: []   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
I don't have that information. I can connect you with a human agent who can help.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_promo_codes] Promotional Codes and Stacking
One promotional code applies per order. Codes cannot be combined with each other or with no-cost EMI unless the code explicitly states otherwise. A code cannot be applied after an order is placed and a replacement order is required. Codes tied to a minimum basket value are void if returns take the order below that value, and the discount is recovered from the refund.
--- [bill_emi] EMI and No-Cost EMI
EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount. If an order paid by no-cost EMI is returned, the discount is deducted from the refund and the bank may still charge interest already levied; the bank must be contacted to cancel the EMI plan.
--- [prod_voltcharge100] VoltCharge 100W GaN Charger
100 W GaN fast charger. Price ₹3,999. Two USB-C ports and one USB-A, supports Power Delivery 3.1 and Quick Charge 5, detachable braided cable included. Required for full-speed charging of the PulseBook Pro 16. Also charges the PulseBook 14, PulseBook Air 13, NovaTab and all SoundWave products. 1-year manufacturer warranty.
--- [prod_pulsebook_pro16] PulseBook Pro 16 Laptop
16-inch creator laptop. Price ₹1,34,999. Intel Core Ultra 9, 32 GB RAM, 1 TB NVMe SSD, discrete RTX 4060 graphics, 16-inch 3.2K OLED at 120 Hz, 100 W USB-C charging, 1.95 kg. 2-year manufacturer warranty including one year of accidental damage protection.

========== q045 [out_of_scope] ==========
QUESTION: Can I collect my order from your warehouse instead of waiting for delivery?
EXPECTED BEHAVIOUR (out of scope): admit_unknown
NEEDED DOCS: []   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
I don't have that information. I can connect you with a human agent who can help.

EVIDENCE THE MODEL WAS GIVEN:
--- [ship_open_box] Open-Box Delivery
Open-box delivery is available in 22 cities on orders above ₹20,000. The courier opens the package in the customer's presence for inspection before handover. Refusal at open-box inspection is free and refunds process within 5 to 7 business days. Open-box delivery adds 1 business day to the estimate.
--- [pol_bulk_orders] Bulk and Business Orders
Orders above 10 units of a single SKU are treated as business orders and require a GSTIN. Bulk pricing is quoted by the business desk and is not available at checkout. Business orders ship in 5 to 10 business days and carry a 15-day return window rather than 30 days.
--- [pol_preorder] Pre-Orders
Pre-ordered items are charged at the time of order, not at dispatch. The estimated dispatch date on the product page is indicative; if it slips by more than 14 days the customer may cancel for a full refund. The 30-day return window begins at delivery, not at the order date.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.

========== q046 [out_of_scope] ==========
QUESTION: Do I earn loyalty points on my purchases?
EXPECTED BEHAVIOUR (out of scope): admit_unknown
NEEDED DOCS: []   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
I don't have that information. I can connect you with a human agent who can help.

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_price_match] Price Match Guarantee
If a customer finds the identical product cheaper on a competing authorised Indian retailer within 7 days of their purchase, TechStore refunds the difference. The competing listing must be for a new, sealed unit sold and shipped by the retailer itself, not a marketplace seller. Price matching does not apply during flash sales or clearance events.
--- [bill_emi] EMI and No-Cost EMI
EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount. If an order paid by no-cost EMI is returned, the discount is deducted from the refund and the bank may still charge interest already levied; the bank must be contacted to cancel the EMI plan.
--- [bill_promo_codes] Promotional Codes and Stacking
One promotional code applies per order. Codes cannot be combined with each other or with no-cost EMI unless the code explicitly states otherwise. A code cannot be applied after an order is placed and a replacement order is required. Codes tied to a minimum basket value are void if returns take the order below that value, and the discount is recovered from the refund.
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.

========== q047 [out_of_scope] ==========
QUESTION: Who is the CEO of TechStore?
EXPECTED BEHAVIOUR (out of scope): admit_unknown
NEEDED DOCS: []   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
I don't have that information. I can connect you with a human agent who can help.

EVIDENCE THE MODEL WAS GIVEN:
--- [about_techstore] About TechStore
TechStore is an online-only consumer electronics retailer in India. It has no physical retail stores or showrooms, so there are no store opening hours; orders are placed only on the TechStore website and app. TechStore sells six product families: headphones and earbuds (SoundWave), laptops (PulseBook), tablets (NovaTab), smartwatches (AuraWatch), monitors (ClearView), and chargers and power banks (VoltCharge, VoltBank). TechStore does not sell mobile phones, televisions, cameras, gaming consoles, or home appliances such as washing machines, refrigerators, or air conditioners. Repairs are handled at authorised service centres in 48 cities. Customer support is available by chat and email from 9 AM to 9 PM IST, seven days a week.
--- [api_overview] TechStore Partner API Overview
The Partner API is a REST API at https://api.techstore.example/v1. All requests require an Authorization header with a bearer token issued in the partner dashboard. Requests and responses are JSON. The API exposes orders, inventory, shipments and webhooks. Sandbox is available at https://sandbox.techstore.example/v1 with separate credentials and synthetic data.
--- [pol_privacy_data] Customer Data and Privacy
TechStore stores order history, delivery addresses and payment metadata. Full card numbers are never stored. A customer may request deletion of their account and associated personal data by writing to privacy@techstore.example; deletion completes within 30 days. TechStore keeps invoice records for 8 years, including after an account is deleted.
--- [svc_centres] Service Centre Network
TechStore operates authorised service centres in 48 Indian cities. The nearest centre can be found by pin code on the Support page. Walk-in service is available for laptops and monitors; headphones, watches and tablets are handled by courier pickup only. Carry the invoice or order ID for any walk-in visit.

========== q048 [out_of_scope] ==========
QUESTION: Do you sell washing machines?
EXPECTED BEHAVIOUR (out of scope): answer_from_about
NEEDED DOCS: ['about_techstore']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No, TechStore does not sell washing machines or other home appliances.

EVIDENCE THE MODEL WAS GIVEN:
--- [about_techstore] About TechStore
TechStore is an online-only consumer electronics retailer in India. It has no physical retail stores or showrooms, so there are no store opening hours; orders are placed only on the TechStore website and app. TechStore sells six product families: headphones and earbuds (SoundWave), laptops (PulseBook), tablets (NovaTab), smartwatches (AuraWatch), monitors (ClearView), and chargers and power banks (VoltCharge, VoltBank). TechStore does not sell mobile phones, televisions, cameras, gaming consoles, or home appliances such as washing machines, refrigerators, or air conditioners. Repairs are handled at authorised service centres in 48 cities. Customer support is available by chat and email from 9 AM to 9 PM IST, seven days a week.
--- [pol_return_exclusions] Non-Returnable Items
For hygiene reasons the following are non-returnable once the seal is broken: headphones of every type (over-ear, on-ear and in-ear), earbuds, fitness bands worn on the wrist, and any personal grooming device. Opened software licences and redeemed digital gift cards are also non-returnable. These items remain covered by warranty if they are faulty; a hygiene exclusion never removes warranty rights.
--- [pol_bulk_orders] Bulk and Business Orders
Orders above 10 units of a single SKU are treated as business orders and require a GSTIN. Bulk pricing is quoted by the business desk and is not available at checkout. Business orders ship in 5 to 10 business days and carry a 15-day return window rather than 30 days.
--- [svc_centres] Service Centre Network
TechStore operates authorised service centres in 48 Indian cities. The nearest centre can be found by pin code on the Support page. Walk-in service is available for laptops and monitors; headphones, watches and tablets are handled by courier pickup only. Carry the invoice or order ID for any walk-in visit.

========== q049 [out_of_scope] ==========
QUESTION: What time does your Bangalore store open?
EXPECTED BEHAVIOUR (out of scope): answer_from_about
NEEDED DOCS: ['about_techstore']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
TechStore is online-only and has no physical retail stores or showrooms, including in Bangalore, so there are no store opening hours. You can place orders on our website or app. Customer support is available from 9 AM to 9 PM IST, seven days a week.

EVIDENCE THE MODEL WAS GIVEN:
--- [about_techstore] About TechStore
TechStore is an online-only consumer electronics retailer in India. It has no physical retail stores or showrooms, so there are no store opening hours; orders are placed only on the TechStore website and app. TechStore sells six product families: headphones and earbuds (SoundWave), laptops (PulseBook), tablets (NovaTab), smartwatches (AuraWatch), monitors (ClearView), and chargers and power banks (VoltCharge, VoltBank). TechStore does not sell mobile phones, televisions, cameras, gaming consoles, or home appliances such as washing machines, refrigerators, or air conditioners. Repairs are handled at authorised service centres in 48 cities. Customer support is available by chat and email from 9 AM to 9 PM IST, seven days a week.
--- [pol_bulk_orders] Bulk and Business Orders
Orders above 10 units of a single SKU are treated as business orders and require a GSTIN. Bulk pricing is quoted by the business desk and is not available at checkout. Business orders ship in 5 to 10 business days and carry a 15-day return window rather than 30 days.
--- [ship_open_box] Open-Box Delivery
Open-box delivery is available in 22 cities on orders above ₹20,000. The courier opens the package in the customer's presence for inspection before handover. Refusal at open-box inspection is free and refunds process within 5 to 7 business days. Open-box delivery adds 1 business day to the estimate.
--- [svc_centres] Service Centre Network
TechStore operates authorised service centres in 48 Indian cities. The nearest centre can be found by pin code on the Support page. Walk-in service is available for laptops and monitors; headphones, watches and tablets are handled by courier pickup only. Carry the invoice or order ID for any walk-in visit.

========== q050 [out_of_scope] ==========
QUESTION: What is the battery life of the X200, and do you offer a student discount?
EXPECTED BEHAVIOUR (out of scope): partial
NEEDED DOCS: ['prod_x200']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
The SoundWave X200 has a **40-hour battery life**.

I don't have information about whether TechStore offers a student discount.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [prod_voltbank20k] VoltBank 20000mAh Power Bank
20000 mAh power bank. Price ₹2,999. 65 W USB-C output, 20 W USB-A output, pass-through charging, LED capacity display, 389 g. Its capacity is under 100 Wh; check your airline's rules before carrying it on a flight. Can charge the PulseBook Air 13 once or the NovaTab 11 twice. 1-year manufacturer warranty.
--- [tsg_watch_battery] Smartwatch Battery Draining Fast
Always-on display reduces AuraWatch Pro battery life from 18 days to roughly 6. Continuous SpO2 monitoring and dual-band GPS also shorten runtime substantially. Disable always-on display and continuous SpO2 to restore rated life. If runtime is under 50 percent of the rated figure with those features off, the battery is a warranty defect.
--- [prod_aurawatch_pro] AuraWatch Pro Smartwatch
Premium fitness smartwatch. Price ₹15,999. 1.5-inch AMOLED always-on display, 18-day battery, ECG and SpO2 sensors, dual-band GPS, 10 ATM water resistance, offline maps, 100 sport modes. Compatible with Android 10 and above and iOS 15 and above. 2-year manufacturer warranty. Non-returnable once used, under the hygiene policy.

========== q051 [simple_faq] ==========
QUESTION: What's the last day I can send an item back?
NEEDED DOCS: ['pol_return_window']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
TechStore’s **“30-day return window”** runs from the delivery date shown on your tracking record—not the order date. A return raised on day 31 or later is automatically rejected.

What delivery date is shown on your tracking record? I can use it to calculate your last day to raise a return.

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [pol_return_window] Return Window
TechStore accepts returns within 30 days of delivery. The 30 days are counted from the delivery date shown on the tracking record, not the order date. Items must be returned in their original packaging with all accessories, manuals and free gifts included. A return raised on day 31 or later is rejected automatically by the returns system.
--- [ship_failed_delivery] Failed Delivery Attempts
The courier makes three delivery attempts on consecutive business days. After the third failed attempt the parcel is returned to our warehouse and the order is refunded in full, including any delivery charge paid, within 7 business days of the parcel being received back. A customer can reschedule delivery once through the tracking link.
--- [pol_preorder] Pre-Orders
Pre-ordered items are charged at the time of order, not at dispatch. The estimated dispatch date on the product page is indicative; if it slips by more than 14 days the customer may cancel for a full refund. The 30-day return window begins at delivery, not at the order date.

========== q052 [simple_faq] ==========
QUESTION: I broke the seal on my earphones, can I still send them back?
NEEDED DOCS: ['pol_return_exclusions']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
If you’ve broken the seal, your earphones are **“non-returnable once the seal is broken”** under TechStore’s hygiene policy.

If they’re faulty, they remain covered by warranty. If they arrived damaged or you received the wrong item, report it **“within 48 hours of delivery”** with photographs of the package and product for a free replacement.

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_return_exclusions] Non-Returnable Items
For hygiene reasons the following are non-returnable once the seal is broken: headphones of every type (over-ear, on-ear and in-ear), earbuds, fitness bands worn on the wrist, and any personal grooming device. Opened software licences and redeemed digital gift cards are also non-returnable. These items remain covered by warranty if they are faulty; a hygiene exclusion never removes warranty rights.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [prod_studiobuds] SoundWave Studio Buds Pro
Premium true wireless earbuds. Price ₹6,999. 9 hours playback and 32 hours with the case, Bluetooth 5.4, active noise cancellation rated 30 dB, IPX5, wireless charging case, multipoint pairing with two devices, in-ear detection. 1-year manufacturer warranty. Non-returnable once opened, under the hygiene policy.
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.

========== q053 [simple_faq] ==========
QUESTION: Can I pay with my Paytm wallet?
NEEDED DOCS: ['bill_payment_methods']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No, TechStore does not accept wallet payments, including Paytm wallet. You can pay using UPI, credit or debit cards from major Indian issuers, net banking from 40 partner banks, or cash on delivery for orders up to ₹20,000. Cash on delivery carries a ₹49 handling fee.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.
--- [bill_emi] EMI and No-Cost EMI
EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount. If an order paid by no-cost EMI is returned, the discount is deducted from the refund and the bank may still charge interest already levied; the bank must be contacted to cancel the EMI plan.
--- [acc_create] Creating and Verifying an Account
An account is created with an email address or an Indian mobile number and verified by a one-time password valid for 10 minutes. A maximum of five OTPs may be requested per hour. An account is required to place an order; guest checkout is not offered.
--- [bill_refund_to_closed_card] Refund to a Closed or Expired Card
Refunds are issued to the original payment method. If that card is closed or expired, the issuing bank still routes the credit to the underlying account in most cases. If the bank rejects the credit, the funds return to TechStore within 10 business days, after which support can arrange a bank transfer once account details and identity are verified. We cannot refund to a different card at the customer's request when the original card is still active.

========== q054 [simple_faq] ==========
QUESTION: How much is shipping on a ₹500 order?
NEEDED DOCS: ['ship_charges']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Shipping on a ₹500 order costs ₹79 under the “flat ₹79 delivery charge” policy for orders below ₹999.

EVIDENCE THE MODEL WAS GIVEN:
--- [ship_charges] Delivery Charges
Delivery is free on all orders above ₹999. Below that a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149 and is available in metro cities only for orders placed before 2 PM. Delivery charges are refunded if the order is cancelled before shipping or if the item arrives damaged.
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.
--- [ship_open_box] Open-Box Delivery
Open-box delivery is available in 22 cities on orders above ₹20,000. The courier opens the package in the customer's presence for inspection before handover. Refusal at open-box inspection is free and refunds process within 5 to 7 business days. Open-box delivery adds 1 business day to the estimate.
--- [ship_international] International Shipping
TechStore ships within India only. We do not ship to international addresses and cannot deliver to APO or diplomatic addresses. Orders placed with an international billing address but an Indian delivery address are accepted.

========== q055 [troubleshooting] ==========
QUESTION: My smartwatch shows the wrong pulse readings
NEEDED DOCS: ['tsg_watch_inaccurate_hr']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Try these steps to check the heart-rate readings:

1. Wear the watch one finger-width above your wrist bone, snug but not tight, so the sensor has firm skin contact.
2. Check whether the sensor sits over a tattoo or your skin is very cold—both can reduce accuracy, as can a loose fit.
3. After adjusting the fit, stay stationary and check whether the readings still seem implausible.

If readings remain implausible while stationary after adjusting the fit, the guide identifies this as a **sensor warranty defect**. I can connect you with a human agent for help with a warranty claim.

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_watch_inaccurate_hr] Heart Rate Readings Inaccurate
Optical heart-rate sensors need firm skin contact. Wear the watch one finger-width above the wrist bone, snug but not tight. Tattoos, very cold skin and loose fits all reduce accuracy. If readings remain implausible when stationary after adjusting fit, the sensor is a warranty defect.
--- [prod_aurawatch_pro] AuraWatch Pro Smartwatch
Premium fitness smartwatch. Price ₹15,999. 1.5-inch AMOLED always-on display, 18-day battery, ECG and SpO2 sensors, dual-band GPS, 10 ATM water resistance, offline maps, 100 sport modes. Compatible with Android 10 and above and iOS 15 and above. 2-year manufacturer warranty. Non-returnable once used, under the hygiene policy.
--- [prod_aurawatch3] AuraWatch 3 Smartwatch
Fitness smartwatch. Price ₹8,999. 1.4-inch AMOLED display, 14-day battery, heart-rate and SpO2 sensors, built-in GPS, 5 ATM water resistance, sleep tracking. Compatible with Android 9 and above and iOS 14 and above. 1-year manufacturer warranty. Worn on the wrist, therefore non-returnable once used, under the hygiene policy.
--- [tsg_watch_sync] Smartwatch Not Syncing
If AuraWatch 3 will not sync: confirm the companion app has Bluetooth and background-activity permission, confirm the phone runs Android 9 or later or iOS 14 or later, force-close and reopen the app, and ensure the watch firmware is current. Battery optimisation settings on some Android phones stop the app in the background and are the most common cause; exclude the app from optimisation.

========== q056 [troubleshooting] ==========
QUESTION: The screen on my monitor keeps blinking
NEEDED DOCS: ['tsg_monitor_flicker']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Sorry your monitor keeps blinking. Try these steps to check the flicker:

1. If you’re using **4K at 144 Hz or above**, use a certified **DisplayPort 1.4 or HDMI 2.1 cable under 2 metres**—high-refresh-rate flicker is usually a cable limitation.
2. Temporarily disable **adaptive sync** and check whether the blinking stops.
3. Set the refresh rate to **60 Hz** and test with a known-good cable. If the flicker persists, the troubleshooting guide identifies this as a **panel warranty defect**.

Which monitor model, cable type, and refresh rate are you using?

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_monitor_flicker] Monitor Flickering
Flicker at high refresh rates is usually a cable limitation. For 4K at 144 Hz or above use a certified DisplayPort 1.4 or HDMI 2.1 cable under 2 metres. Disable adaptive sync temporarily to test. If flicker persists at 60 Hz with a known-good cable, the panel is a warranty defect.
--- [tsg_monitor_no_signal] Monitor Shows No Signal
If ClearView 27 reports no signal: 1) Confirm the input source matches the cable used, selectable in the on-screen menu. 2) For USB-C, confirm the laptop port supports DisplayPort Alt Mode; the PulseBook USB-A port does not. 3) Try a different cable, as many USB-C cables carry power but not video. 4) At 4K 144 Hz use DisplayPort 1.4 or HDMI 2.1; older cables cap the refresh rate. 5) Reset the monitor to factory defaults from the menu.
--- [prod_clearview27] ClearView 27 Monitor
27-inch monitor. Price ₹22,999. 4K UHD IPS panel, 144 Hz refresh, 1 ms response, 95 percent DCI-P3 colour coverage, USB-C with 90 W power delivery, height and pivot adjustable stand, VESA 100 mount. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.
--- [prod_clearview32] ClearView 32 Ultra Monitor
32-inch monitor. Price ₹39,999. 4K UHD IPS Black panel, 165 Hz refresh, 1 ms response, 99 percent DCI-P3, HDR600, USB-C with 140 W power delivery, built-in KVM switch, height and pivot adjustable stand, VESA 100. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.

========== q057 [billing_dispute] ==========
QUESTION: I paid twice by mistake for the same thing
NEEDED DOCS: ['bill_duplicate_charge']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
I’m sorry about the double payment. Here’s how it’s resolved:

1. **If only one order was created:** The extra payment is an authorisation hold that reverses automatically within **“5 to 7 business days.”**
2. **If two separate orders were created:** Each unwanted order must be cancelled separately. Refunds are processed separately and may arrive on different days.

I don't have information about your charge dates, amounts, or order details—please share both payment dates and amounts, and any order numbers, so we can identify which situation applies.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_duplicate_charge] Duplicate or Multiple Charges
A duplicate charge occurs when a payment page is submitted more than once. Only one order is created; the additional authorisations are holds that reverse automatically within 5 to 7 business days. If two or more distinct orders were created, each must be cancelled separately and each refund is processed separately, so a customer may see refunds arrive on different days. When resolving a multi-charge dispute, list every charge with its date and amount, state which one corresponds to the surviving order, and give the expected reversal date for each of the others.
--- [bill_chargeback] Bank Chargebacks and Disputes
If a customer raises a chargeback with their bank, the order is frozen and any parallel TechStore refund is suspended to prevent a double credit. Chargebacks take 45 to 90 days to resolve through the card network. Contacting support directly is almost always faster than a chargeback, and support can withdraw a chargeback by providing the bank with resolution evidence.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [bill_failed_payment] Payment Failed but Money Debited
If a payment fails but the amount is debited, the bank has placed a temporary hold that is released automatically. Card and UPI holds reverse within 5 to 7 business days; net banking can take up to 10. No order is created for a failed payment, so there is nothing to cancel. If the amount has not reversed after the stated period, contact support with the bank reference number and TechStore raises a chargeback trace with the payment gateway.

========== q058 [billing_dispute] ==========
QUESTION: Can my company's tax number be added to the bill later?
NEEDED DOCS: ['bill_invoice_gst']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No. Your company’s GSTIN must be entered **“at checkout, before placing the order.”** TechStore cannot add it to an invoice afterwards or issue a fresh invoice for a completed order.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_invoice_gst] Invoice and GST
A tax invoice is emailed within 24 hours of dispatch and is downloadable from Orders. Business customers who need their GSTIN on the invoice must enter it at checkout, before placing the order. TechStore cannot add a GSTIN to an invoice afterwards and does not issue a fresh invoice for a completed order. Invoices remain downloadable for 8 years.
--- [acc_address] Changing a Delivery Address
The delivery address can be changed from Orders until the order is marked Shipped. After dispatch the address cannot be changed, but delivery can be rescheduled once through the courier tracking link. Changing the address to a different pin code after dispatch is not possible; the order must be refused and reordered.
--- [bill_duplicate_charge] Duplicate or Multiple Charges
A duplicate charge occurs when a payment page is submitted more than once. Only one order is created; the additional authorisations are holds that reverse automatically within 5 to 7 business days. If two or more distinct orders were created, each must be cancelled separately and each refund is processed separately, so a customer may see refunds arrive on different days. When resolving a multi-charge dispute, list every charge with its date and amount, state which one corresponds to the surviving order, and give the expected reversal date for each of the others.
--- [bill_promo_codes] Promotional Codes and Stacking
One promotional code applies per order. Codes cannot be combined with each other or with no-cost EMI unless the code explicitly states otherwise. A code cannot be applied after an order is placed and a replacement order is required. Codes tied to a minimum basket value are void if returns take the order below that value, and the discount is recovered from the refund.

========== q059 [simple_faq] ==========
QUESTION: Do you deliver to Dubai?
NEEDED DOCS: ['ship_international']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No. TechStore “ships within India only” and does not deliver to international addresses, including Dubai.

EVIDENCE THE MODEL WAS GIVEN:
--- [ship_international] International Shipping
TechStore ships within India only. We do not ship to international addresses and cannot deliver to APO or diplomatic addresses. Orders placed with an international billing address but an Indian delivery address are accepted.
--- [ship_open_box] Open-Box Delivery
Open-box delivery is available in 22 cities on orders above ₹20,000. The courier opens the package in the customer's presence for inspection before handover. Refusal at open-box inspection is free and refunds process within 5 to 7 business days. Open-box delivery adds 1 business day to the estimate.
--- [ship_charges] Delivery Charges
Delivery is free on all orders above ₹999. Below that a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149 and is available in metro cities only for orders placed before 2 PM. Delivery charges are refunded if the order is cancelled before shipping or if the item arrives damaged.
--- [acc_address] Changing a Delivery Address
The delivery address can be changed from Orders until the order is marked Shipped. After dispatch the address cannot be changed, but delivery can be rescheduled once through the courier tracking link. Changing the address to a different pin code after dispatch is not possible; the order must be refused and reordered.

========== q060 [troubleshooting] ==========
QUESTION: My laptop gets really hot and switches itself off
NEEDED DOCS: ['tsg_laptop_overheating']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
I’m sorry your laptop is getting so hot and shutting down. Please try these steps:

1. Make sure the vents are unobstructed, and avoid using the laptop on fabric.
2. Clean the intake grilles with compressed air.
3. Update the BIOS.

Surface temperatures up to 45°C under sustained load are within specification, but shutdowns under light load indicate a fan or sensor fault and are covered by warranty.

Which laptop model do you have, and does it shut down during demanding tasks or even during light use?

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_laptop_overheating] Laptop Overheating
Surface temperatures up to 45 C under sustained load are within specification. If the machine thermally throttles or shuts down: ensure the vents are unobstructed and not used on fabric, clean the intake grilles with compressed air, and update the BIOS. Shutdowns under light load indicate a fan or sensor fault and are covered by warranty.
--- [tsg_laptop_not_charging] Laptop Not Charging
If a PulseBook will not charge: 1) Confirm the charger wattage matches the model; the PulseBook Pro 16 needs 100 W and will charge very slowly or not at all on a 65 W unit. 2) Try the other Thunderbolt port; the right-hand port on the PulseBook 14 supports charging. 3) Inspect the cable for damage. 4) Hold the power button for 15 seconds to reset the embedded controller. 5) If the charging LED never illuminates with a known-good charger, raise a warranty service request.
--- [prod_pulsebook_air13] PulseBook Air 13 Laptop
13-inch entry ultrabook. Price ₹44,999. Intel Core Ultra 3, 8 GB LPDDR5 RAM, 256 GB NVMe SSD, 13.3-inch 1920x1200 IPS display at 60 Hz, 45 W USB-C charging, 1.12 kg, 10-hour rated battery. Ports: two USB-C, one USB-A, headphone jack. No HDMI port. 2-year manufacturer warranty. Accidental damage protection is not included on the Air 13; it is included only on the PulseBook 14 and Pro 16.
--- [tsg_laptop_slow] Laptop Running Slowly
For a PulseBook running slowly: check available storage, as NVMe drives slow markedly above 90 percent full; open Task Manager to identify background processes; confirm the power mode is not set to Battery Saver while plugged in; and update the chipset and graphics drivers. The PulseBook Air 13 with 8 GB RAM will swap under heavy multitasking; this is expected behaviour, not a defect.

========== q061 [simple_faq] ==========
QUESTION: How can I make my login safer with a code on my phone?
NEEDED DOCS: ['acc_two_factor']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
You can enable **two-factor authentication (2FA)** to use a code on your phone when signing in:

1. Open **Security** in your TechStore account.
2. Enable **two-factor authentication**.
3. Choose an **authenticator app** or **SMS** for your codes.

Enabling 2FA signs out all other sessions.

EVIDENCE THE MODEL WAS GIVEN:
--- [acc_password] Password Reset
Use Forgot Password on the sign-in page. A reset link valid for 30 minutes is emailed. If the email does not arrive, check spam and confirm the address matches the registered one; for privacy we do not disclose whether an address is registered. After three failed sign-in attempts the account is locked for 15 minutes.
--- [acc_two_factor] Two-Factor Authentication
Two-factor authentication can be enabled from Security in the account, using an authenticator app or SMS. Enabling 2FA signs out all other sessions. To disable 2FA, current authentication is required; if the device is lost, identity is verified with the last order details and a government ID, and removal takes up to 48 hours.
--- [acc_create] Creating and Verifying an Account
An account is created with an email address or an Indian mobile number and verified by a one-time password valid for 10 minutes. A maximum of five OTPs may be requested per hour. An account is required to place an order; guest checkout is not offered.
--- [pol_privacy_data] Customer Data and Privacy
TechStore stores order history, delivery addresses and payment metadata. Full card numbers are never stored. A customer may request deletion of their account and associated personal data by writing to privacy@techstore.example; deletion completes within 30 days. TechStore keeps invoice records for 8 years, including after an account is deleted.

========== q062 [policy_edge_case] ==========
QUESTION: If my headphones get replaced, does the 2 year cover restart?
NEEDED DOCS: ['pol_replacement_warranty']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No—the 2-year warranty does not restart. Under **“Warranty on Replaced Units,”** the replacement inherits the remaining warranty of your original headphones. If fewer than 90 days remain, the replacement carries **90 days from the replacement date**.

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
That sounds like a **429 rate-limit error**. Here’s what to check:

1. **Check your request rate:** The Partner API allows **600 requests per minute per token**, or **60 per minute for bulk export endpoints**.
2. **Honour the `Retry-After` header:** Its value tells you how many seconds to wait before retrying.
3. **Use exponential backoff with jitter:** Increase the delay between retries and add randomized timing. Avoid retrying immediately in a tight loop.
4. **Check for a temporary block:** Sustained limit violations for **more than 15 minutes** result in a **temporary 1-hour block**.

Which endpoint are you calling, and what `Retry-After` value are you receiving?

EVIDENCE THE MODEL WAS GIVEN:
--- [api_rate_limits] API Rate Limits and 429 Errors
The Partner API allows 600 requests per minute per token, and 60 per minute for the bulk export endpoints. Exceeding the limit returns 429 with a Retry-After header in seconds. Clients should honour Retry-After and use exponential backoff with jitter. Sustained violation for more than 15 minutes results in a temporary 1-hour block.
--- [api_timeouts] API Timeouts and Retry Safety
Requests time out server side at 30 seconds. A timeout does not indicate whether the operation completed, so POST requests must be retried with the same Idempotency-Key to avoid duplicates. GET, PUT and DELETE are idempotent by design and safe to retry. Retries should use exponential backoff with jitter; retrying immediately in a tight loop triggers rate limiting.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_idempotency] API Idempotency
All POST endpoints accept an Idempotency-Key header. A repeated request with the same key and an identical payload returns the original response without creating a second resource. A repeated key with a different payload returns 409. Keys are retained for 24 hours. Clients should generate a UUID per logical operation, not per HTTP attempt, so that retries reuse the same key.

========== q064 [simple_faq] ==========
QUESTION: Can I change where my parcel goes after it has left?
NEEDED DOCS: ['acc_address']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
After dispatch, the delivery address cannot be changed. You can reschedule delivery once through the courier tracking link.

If you need delivery to a different pin code, the order must be refused and reordered.

EVIDENCE THE MODEL WAS GIVEN:
--- [acc_address] Changing a Delivery Address
The delivery address can be changed from Orders until the order is marked Shipped. After dispatch the address cannot be changed, but delivery can be rescheduled once through the courier tracking link. Changing the address to a different pin code after dispatch is not possible; the order must be refused and reordered.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [ship_tracking] Tracking an Order
A tracking link is emailed and sent by SMS when the order is marked Shipped. Tracking can also be seen under Orders in the account. Tracking information can take up to 12 hours after dispatch to become active with the courier. If tracking has not updated for more than 48 hours, contact support so a courier trace can be raised.
--- [pol_privacy_data] Customer Data and Privacy
TechStore stores order history, delivery addresses and payment metadata. Full card numbers are never stored. A customer may request deletion of their account and associated personal data by writing to privacy@techstore.example; deletion completes within 30 days. TechStore keeps invoice records for 8 years, including after an account is deleted.
