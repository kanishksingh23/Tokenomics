# Answers to grade

Grade each answer ONLY against the evidence shown with it. Store date: 30 September 2026.
Verdicts: correct / partial / wrong / hallucinated (rubric: Tokenomics.md §7, Grading Rubric).


========== q001 [simple_faq] ==========
QUESTION: How long do I have to return something?
NEEDED DOCS: ['pol_return_window']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
TechStore accepts returns “within 30 days of delivery,” counted from the delivery date shown on the tracking record—not the order date. A return raised on day 31 or later is rejected automatically.

Items must be in their original packaging with all accessories, manuals, and free gifts included.

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_return_window] Return Window
TechStore accepts returns within 30 days of delivery. The 30 days are counted from the delivery date shown on the tracking record, not the order date. Items must be returned in their original packaging with all accessories, manuals and free gifts included. A return raised on day 31 or later is rejected automatically by the returns system.
--- [pol_refund_timeline] Refund Processing Time
Once a returned item is received and inspected at our warehouse, refunds are initiated within 2 business days. The money reaches the original payment method in 5 to 7 business days for cards and UPI, and up to 10 business days for net banking. Refunds are always issued to the original payment method; we cannot redirect a refund to a different card or account.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [ship_failed_delivery] Failed Delivery Attempts
The courier makes three delivery attempts on consecutive business days. After the third failed attempt the parcel is returned to our warehouse and the order is refunded in full, including any delivery charge paid, within 7 business days of the parcel being received back. A customer can reschedule delivery once through the tracking link.

========== q006 [order_status] ==========
QUESTION: Where is my order #48213?
NEEDED DOCS: ['ship_tracking']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Your order #48213 for SoundWave X200 Wireless Headphones has shipped via BlueDart and is due today, 30 September 2026.

- **Tracking ID:** BD4471920381
- **Track it:** Check **Orders** in your TechStore account, or use the tracking link sent by email and SMS.

If tracking has not updated for “more than 48 hours,” contact support so a courier trace can be raised.

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

========== q009 [order_status] ==========
QUESTION: I cancelled order 48455, when do I get my refund?
NEEDED DOCS: ['pol_refund_timeline']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Your refund of ₹2,499 for order #48455 has been initiated to your original UPI payment method and is expected by **1 October 2026**.

Cancelled orders are refunded “within 5 to 7 business days.”

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

========== q011 [product_info] ==========
QUESTION: Does the SoundWave X200 have noise cancellation?
NEEDED DOCS: ['prod_x200']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Yes, the SoundWave X200 has **hybrid active noise cancellation rated at 35 dB**. It costs ₹12,999.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [prod_y500] SoundWave Y500 Premium Headphones
Flagship over-ear wireless headphones. Price ₹24,999. 60-hour battery life, Bluetooth 5.4, adaptive active noise cancellation rated at 45 dB with transparency mode, LDAC and aptX Lossless support, USB-C and wireless charging, multipoint pairing with three devices, 268 g, memory-foam earcups. Available in Graphite and Sand. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy. Recommended over the X200 for noisy environments such as open-plan offices and flights.
--- [prod_m100] SoundWave M100 Wireless Earbuds
Entry-level true wireless earbuds. Price ₹3,499. 7 hours playback per charge and 28 hours with the case, Bluetooth 5.2, IPX4 splash resistance, touch controls, USB-C charging. No active noise cancellation. Available in Black and Ivory. 1-year manufacturer warranty. Worn in the ear, therefore non-returnable once the seal is opened, under the hygiene policy.
--- [prod_studiobuds] SoundWave Studio Buds Pro
Premium true wireless earbuds. Price ₹6,999. 9 hours playback and 32 hours with the case, Bluetooth 5.4, active noise cancellation rated 30 dB, IPX5, wireless charging case, multipoint pairing with two devices, in-ear detection. 1-year manufacturer warranty. Non-returnable once opened, under the hygiene policy.

========== q016 [product_comparison] ==========
QUESTION: X200 or Y500 for a noisy open-plan office?
NEEDED DOCS: ['prod_x200', 'prod_y500']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
For a noisy open-plan office, I recommend the **SoundWave Y500**.

- **Stronger noise cancellation:** adaptive ANC rated at 45 dB, versus the X200’s 35 dB hybrid ANC.
- **Longer battery life:** 60 hours versus 40 hours.
- **More device connections:** multipoint pairing with three devices versus two.
- **Price:** Y500 costs ₹24,999; X200 costs ₹12,999.

The X200 is the lower-cost option, but the Y500 is specifically recommended for noisy offices. Both have a **“2-year manufacturer warranty”** and are **“Non-returnable once the seal is opened”** under the hygiene policy.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [prod_y500] SoundWave Y500 Premium Headphones
Flagship over-ear wireless headphones. Price ₹24,999. 60-hour battery life, Bluetooth 5.4, adaptive active noise cancellation rated at 45 dB with transparency mode, LDAC and aptX Lossless support, USB-C and wireless charging, multipoint pairing with three devices, 268 g, memory-foam earcups. Available in Graphite and Sand. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy. Recommended over the X200 for noisy environments such as open-plan offices and flights.
--- [prod_m100] SoundWave M100 Wireless Earbuds
Entry-level true wireless earbuds. Price ₹3,499. 7 hours playback per charge and 28 hours with the case, Bluetooth 5.2, IPX4 splash resistance, touch controls, USB-C charging. No active noise cancellation. Available in Black and Ivory. 1-year manufacturer warranty. Worn in the ear, therefore non-returnable once the seal is opened, under the hygiene policy.
--- [prod_studiobuds] SoundWave Studio Buds Pro
Premium true wireless earbuds. Price ₹6,999. 9 hours playback and 32 hours with the case, Bluetooth 5.4, active noise cancellation rated 30 dB, IPX5, wireless charging case, multipoint pairing with two devices, in-ear detection. 1-year manufacturer warranty. Non-returnable once opened, under the hygiene policy.

========== q020 [product_comparison] ==========
QUESTION: I want a tablet for reading and a laptop for college. What should I buy under 1 lakh total?
NEEDED DOCS: ['prod_novatab11', 'prod_pulsebook14']   MISSING FROM WHAT THE MODEL SAW: ['prod_pulsebook14']

ANSWER:
I’d recommend this pair for reading and college work:

| Product | Why it fits | Price |
|---|---|---:|
| **NovaTab Mini 8** | Compact 8.4-inch screen for reading, with 6 GB RAM and 128 GB expandable storage. Stylus **not supported**. | ₹17,999 |
| **PulseBook 14** | 14-inch laptop with Core Ultra 5, 16 GB RAM and 512 GB SSD; weighs 1.29 kg. A good balance of memory, storage and portability for college. | ₹64,999 |
| **Total** | | **₹82,998** |

That leaves **₹17,002** within your ₹1,00,000 budget.

**If handwritten notes matter:** choose the **NovaTab 11 + stylus + PulseBook 14** instead, totalling **₹99,997**. The tablet has an 11-inch display, 8 GB RAM and 256 GB expandable storage; the stylus is sold separately at ₹4,999.

What’s your college course, and do you want to take handwritten notes?

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

========== q023 [troubleshooting] ==========
QUESTION: My AuraWatch will not sync with the app.
NEEDED DOCS: ['tsg_watch_sync']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
If your watch is an AuraWatch 3, try these steps:

1. Give the companion app Bluetooth and background-activity permissions.
2. Confirm your phone runs Android 9 or later, or iOS 14 or later.
3. On Android, exclude the app from battery optimisation—this is the most common cause of background syncing issues.
4. Force-close and reopen the app.
5. Ensure the watch firmware is current.

I don't have information about syncing other AuraWatch models.

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_watch_sync] Smartwatch Not Syncing
If AuraWatch 3 will not sync: confirm the companion app has Bluetooth and background-activity permission, confirm the phone runs Android 9 or later or iOS 14 or later, force-close and reopen the app, and ensure the watch firmware is current. Battery optimisation settings on some Android phones stop the app in the background and are the most common cause; exclude the app from optimisation.
--- [tsg_watch_inaccurate_hr] Heart Rate Readings Inaccurate
Optical heart-rate sensors need firm skin contact. Wear the watch one finger-width above the wrist bone, snug but not tight. Tattoos, very cold skin and loose fits all reduce accuracy. If readings remain implausible when stationary after adjusting fit, the sensor is a warranty defect.

========== q025 [troubleshooting] ==========
QUESTION: My headphone battery drains much faster than advertised.
NEEDED DOCS: ['tsg_headphone_battery', 'pol_warranty_terms']   MISSING FROM WHAT THE MODEL SAW: ['pol_warranty_terms']

ANSWER:
If you’re using SoundWave headphones, active noise cancellation (ANC) combined with high volume is a common cause of faster drain. ANC reduces rated battery life by roughly 30 percent.

1. Check for firmware updates in the SoundWave app.
2. Disable multipoint if you don’t need two devices connected.
3. Confirm the headphones power off rather than idle when removed.
4. Check the runtime with ANC off. If it’s “below 50 percent of the rated figure with ANC off,” the battery is considered defective and covered under warranty.

Which model do you have, and how long does a full charge last with ANC off?

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_headphone_battery] Headphone Battery Draining Fast
Rapid battery drain on SoundWave headphones is usually caused by active noise cancellation combined with high volume. ANC reduces rated battery life by roughly 30 percent. Check for firmware updates in the SoundWave app, disable multipoint if two devices are not needed, and confirm the unit powers off rather than idling when removed. If runtime is below 50 percent of the rated figure with ANC off, the battery is considered defective and covered under warranty.

========== q029 [billing_dispute] ==========
QUESTION: I bought on no-cost EMI and returned the product. The bank is still charging me interest. Who pays that?
NEEDED DOCS: ['bill_emi', 'pol_refund_timeline']   MISSING FROM WHAT THE MODEL SAW: ['pol_refund_timeline']

ANSWER:
I understand that’s frustrating. Under TechStore’s no-cost EMI terms, “the discount is deducted from the refund and the bank may still charge interest already levied.” TechStore doesn’t cover that bank interest.

1. Contact your bank to cancel the EMI plan; returning the product doesn’t cancel it automatically.
2. Ask the bank to confirm the interest already levied and whether it can be reversed.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_emi] EMI and No-Cost EMI
EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount. If an order paid by no-cost EMI is returned, the discount is deducted from the refund and the bank may still charge interest already levied; the bank must be contacted to cancel the EMI plan.
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.
--- [bill_chargeback] Bank Chargebacks and Disputes
If a customer raises a chargeback with their bank, the order is frozen and any parallel TechStore refund is suspended to prevent a double credit. Chargebacks take 45 to 90 days to resolve through the card network. Contacting support directly is almost always faster than a chargeback, and support can withdraw a chargeback by providing the bank with resolution evidence.

========== q030 [billing_dispute] ==========
QUESTION: I forgot to add my GSTIN at checkout on order 48750. Can you reissue the invoice so I can claim input credit?
NEEDED DOCS: ['bill_invoice_gst']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
I’m sorry, but we can’t reissue the invoice for order #48750 to add your GSTIN. Our policy states: “TechStore cannot add a GSTIN to an invoice afterwards and does not issue a fresh invoice for a completed order.”

Your existing invoice remains downloadable from Orders for “8 years.”

I don't have information about whether you can claim input credit using the existing invoice.

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
Your code computes the HMAC over re-serialised JSON: `json.dumps(request.json).encode()`. That can change whitespace or key order, so the signature won’t match the original raw body.

1. Read the **exact raw request-body bytes before any JSON parsing**.
2. Compute the HMAC using the **webhook secret**, not your API token:
   ```python
   sig = hmac.new(webhook_secret, raw_body, 'sha256').hexdigest()
   ```
3. Compare the hex digest with the `X-TechStore-Signature` header.
4. Parse the JSON only after signature verification.

EVIDENCE THE MODEL WAS GIVEN:
--- [api_webhook_signature] Webhook Signature Verification and 403 Errors
Every webhook carries an X-TechStore-Signature header containing an HMAC-SHA256 of the raw request body, keyed with the webhook secret, hex encoded. A 403 returned by our delivery checker almost always means the signature was computed over a parsed and re-serialised body rather than the raw bytes; JSON re-serialisation changes key order and whitespace and therefore changes the HMAC. Compute the HMAC over the exact raw body before any JSON parsing. The second most common cause is using the API token instead of the webhook secret as the HMAC key.

========== q035 [technical_api] ==========
QUESTION: A valid order ID returns 404 for my token but works in the dashboard. What is happening?
NEEDED DOCS: ['api_error_codes', 'api_auth']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
A 404 can mean “resource not found, including a valid order ID belonging to a different partner.” The order may exist in the dashboard but belong to a different partner than the one associated with your token.

I don't have information about your token’s partner association or that specific order to confirm the cause.

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
I’m sorry your PulseBook is faulty. Your return eligibility and warranty coverage are separate:

- **Returns:** TechStore accepts returns “within 30 days of delivery,” counted from the tracking record—not the purchase date. A return raised on “day 31 or later is rejected automatically,” so buying it 35 days ago does not by itself establish whether your return window has closed.
- **Warranty:** Coverage starts from delivery and covers “manufacturing defects and component failure under normal use.” Warranty is “independent of the 30-day return window,” so an eligible fault may still qualify for repair or replacement after returns close.
- **Exclusions:** Standard warranty does not cover “physical damage, liquid ingress, unauthorised repair, or normal battery capacity decline above 80 percent of the rated capacity.”

I don't have information about your specific PulseBook’s warranty duration, delivery date, or fault to confirm the stated two-year coverage or your eligibility.

EVIDENCE THE MODEL WAS GIVEN:
--- [svc_accidental_damage] Accidental Damage Protection
PulseBook 14 and PulseBook Pro 16 include one year of accidental damage protection from the delivery date, covering drops and liquid spills. One claim is permitted in the coverage year, with a customer contribution of 10 percent of the product price. Accidental damage protection does not cover theft, loss, or cosmetic damage that does not affect function.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [pol_return_window] Return Window
TechStore accepts returns within 30 days of delivery. The 30 days are counted from the delivery date shown on the tracking record, not the order date. Items must be returned in their original packaging with all accessories, manuals and free gifts included. A return raised on day 31 or later is rejected automatically by the returns system.
--- [pol_warranty_terms] Standard Warranty Terms
All products carry the manufacturer warranty stated on the product page, counted from the delivery date. Warranty covers manufacturing defects and component failure under normal use. It does not cover physical damage, liquid ingress, unauthorised repair, or normal battery capacity decline above 80 percent of the rated capacity. Warranty is independent of the 30-day return window: a product outside the return window may still be repaired or replaced under warranty.

========== q038 [policy_edge_case] ==========
QUESTION: I spilled coffee on my PulseBook 14 four months after delivery. Warranty excludes liquid damage. Is there anything that covers me?
NEEDED DOCS: ['pol_warranty_terms', 'svc_accidental_damage']   MISSING FROM WHAT THE MODEL SAW: ['pol_warranty_terms']

ANSWER:
Yes—your PulseBook 14 includes **“one year of accidental damage protection from the delivery date,”** covering **“drops and liquid spills.”** A coffee spill four months after delivery falls within that coverage period.

You can make **one claim in the coverage year**, provided you haven’t already used it. The required **“customer contribution of 10 percent of the product price”** is ₹6,499.90, based on the listed price of ₹64,999.

I don't have information about the claim submission process, but I can connect you with a human agent who can help.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_pulsebook14] PulseBook 14 Laptop
14-inch ultrabook. Price ₹64,999. Intel Core Ultra 5, 16 GB LPDDR5 RAM, 512 GB NVMe SSD, 14-inch 2.8K OLED display at 90 Hz, 65 W USB-C charging, 1.29 kg, 12-hour rated battery. Ports: two USB-C Thunderbolt, one USB-A, HDMI 2.1, headphone jack. 2-year manufacturer warranty including one year of accidental damage protection.
--- [svc_accidental_damage] Accidental Damage Protection
PulseBook 14 and PulseBook Pro 16 include one year of accidental damage protection from the delivery date, covering drops and liquid spills. One claim is permitted in the coverage year, with a customer contribution of 10 percent of the product price. Accidental damage protection does not cover theft, loss, or cosmetic damage that does not affect function.

========== q040 [policy_edge_case] ==========
QUESTION: I found the X200 cheaper elsewhere 6 days after buying, but it was during their clearance sale. Does your price match apply?
NEEDED DOCS: ['pol_price_match']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No—our Price Match Guarantee states: “Price matching does not apply during flash sales or clearance events.” Although you found it within 7 days of purchase, the competitor’s clearance sale is excluded.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [pol_price_match] Price Match Guarantee
If a customer finds the identical product cheaper on a competing authorised Indian retailer within 7 days of their purchase, TechStore refunds the difference. The competing listing must be for a new, sealed unit sold and shipped by the retailer itself, not a marketplace seller. Price matching does not apply during flash sales or clearance events.
--- [bill_price_drop] Price Drop After Purchase
If a product's TechStore price drops within 7 days of purchase, the difference is refunded on request. This applies once per order line and does not apply during flash sales, festive events or clearance. This is distinct from the price match guarantee, which covers competitor pricing.

========== q051 [simple_faq] ==========
QUESTION: What's the last day I can send an item back?
NEEDED DOCS: ['pol_return_window']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
TechStore accepts returns “within 30 days of delivery,” counted from the delivery date shown on your tracking record—not the order date. A return raised on day 31 or later is rejected automatically.

What delivery date does your tracking show?

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
If you’ve broken the seal, your earphones are “non-returnable once the seal is broken” under TechStore’s hygiene policy.

If they’re faulty, they remain covered by warranty; “a hygiene exclusion never removes warranty rights.”

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_return_exclusions] Non-Returnable Items
For hygiene reasons the following are non-returnable once the seal is broken: headphones of every type (over-ear, on-ear and in-ear), earbuds, fitness bands worn on the wrist, and any personal grooming device. Opened software licences and redeemed digital gift cards are also non-returnable. These items remain covered by warranty if they are faulty; a hygiene exclusion never removes warranty rights.

========== q054 [simple_faq] ==========
QUESTION: How much is shipping on a ₹500 order?
NEEDED DOCS: ['ship_charges']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Shipping on a ₹500 order is ₹79, as a “flat ₹79 delivery charge applies” to orders below ₹999.

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
Sorry your smartwatch’s pulse readings seem inaccurate. Try these steps:

1. Wear it one finger-width above your wrist bone.
2. Adjust the strap so it’s snug but not tight, with firm skin contact.
3. Check whether tattoos, very cold skin, or a loose fit may be affecting accuracy.
4. Stay stationary and check the readings again after adjusting the fit.

If the readings remain implausible while stationary after adjusting the fit, the sensor is a “warranty defect.”

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_watch_inaccurate_hr] Heart Rate Readings Inaccurate
Optical heart-rate sensors need firm skin contact. Wear the watch one finger-width above the wrist bone, snug but not tight. Tattoos, very cold skin and loose fits all reduce accuracy. If readings remain implausible when stationary after adjusting fit, the sensor is a warranty defect.

========== q057 [billing_dispute] ==========
QUESTION: I paid twice by mistake for the same thing
NEEDED DOCS: ['bill_duplicate_charge']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
I’m sorry for the confusion. Here’s how duplicate payments are handled:

1. **If only one order was created:** the extra payment is an authorisation hold that reverses automatically within **“5 to 7 business days.”**
2. **If two separate orders were created:** each unwanted order must be cancelled separately. Refunds are processed separately and may arrive on different days.

I don't have information about your two charge dates, amounts, or order numbers—could you share these so we can identify which charge belongs to the order you want to keep and the expected reversal date for the other?

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_duplicate_charge] Duplicate or Multiple Charges
A duplicate charge occurs when a payment page is submitted more than once. Only one order is created; the additional authorisations are holds that reverse automatically within 5 to 7 business days. If two or more distinct orders were created, each must be cancelled separately and each refund is processed separately, so a customer may see refunds arrive on different days. When resolving a multi-charge dispute, list every charge with its date and amount, state which one corresponds to the surviving order, and give the expected reversal date for each of the others.
--- [bill_chargeback] Bank Chargebacks and Disputes
If a customer raises a chargeback with their bank, the order is frozen and any parallel TechStore refund is suspended to prevent a double credit. Chargebacks take 45 to 90 days to resolve through the card network. Contacting support directly is almost always faster than a chargeback, and support can withdraw a chargeback by providing the bank with resolution evidence.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [bill_failed_payment] Payment Failed but Money Debited
If a payment fails but the amount is debited, the bank has placed a temporary hold that is released automatically. Card and UPI holds reverse within 5 to 7 business days; net banking can take up to 10. No order is created for a failed payment, so there is nothing to cancel. If the amount has not reversed after the stated period, contact support with the bank reference number and TechStore raises a chargeback trace with the payment gateway.

========== q061 [simple_faq] ==========
QUESTION: How can I make my login safer with a code on my phone?
NEEDED DOCS: ['acc_two_factor']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
You can enable **two-factor authentication (2FA)** to make your login safer with a code on your phone:

1. Open **Security** in your TechStore account.
2. Enable 2FA using an **authenticator app or SMS**.

Enabling 2FA “signs out all other sessions.”

EVIDENCE THE MODEL WAS GIVEN:
--- [acc_password] Password Reset
Use Forgot Password on the sign-in page. A reset link valid for 30 minutes is emailed. If the email does not arrive, check spam and confirm the address matches the registered one; for privacy we do not disclose whether an address is registered. After three failed sign-in attempts the account is locked for 15 minutes.
--- [acc_two_factor] Two-Factor Authentication
Two-factor authentication can be enabled from Security in the account, using an authenticator app or SMS. Enabling 2FA signs out all other sessions. To disable 2FA, current authentication is required; if the device is lost, identity is verified with the last order details and a government ID, and removal takes up to 48 hours.
--- [acc_create] Creating and Verifying an Account
An account is created with an email address or an Indian mobile number and verified by a one-time password valid for 10 minutes. A maximum of five OTPs may be requested per hour. An account is required to place an order; guest checkout is not offered.
--- [pol_privacy_data] Customer Data and Privacy
TechStore stores order history, delivery addresses and payment metadata. Full card numbers are never stored. A customer may request deletion of their account and associated personal data by writing to privacy@techstore.example; deletion completes within 30 days. TechStore keeps invoice records for 8 years, including after an account is deleted.

========== q063 [technical_api] ==========
QUESTION: The API keeps telling me I'm sending too many requests
NEEDED DOCS: ['api_rate_limits']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
That sounds like a **429 rate-limit error**. Here’s how to handle it:

1. Check your request rate. The Partner API allows **600 requests per minute per token**, or **60 per minute for bulk export endpoints**.
2. Honour the response’s **`Retry-After` header**, which specifies how many seconds to wait.
3. Use **exponential backoff with jitter** for retries rather than retrying immediately in a tight loop.
4. Avoid sustained retries above the limit: “Sustained violation for more than 15 minutes results in a temporary 1-hour block.”

Are you using a bulk export endpoint, and what `Retry-After` value are you seeing?

EVIDENCE THE MODEL WAS GIVEN:
--- [api_rate_limits] API Rate Limits and 429 Errors
The Partner API allows 600 requests per minute per token, and 60 per minute for the bulk export endpoints. Exceeding the limit returns 429 with a Retry-After header in seconds. Clients should honour Retry-After and use exponential backoff with jitter. Sustained violation for more than 15 minutes results in a temporary 1-hour block.
--- [api_timeouts] API Timeouts and Retry Safety
Requests time out server side at 30 seconds. A timeout does not indicate whether the operation completed, so POST requests must be retried with the same Idempotency-Key to avoid duplicates. GET, PUT and DELETE are idempotent by design and safe to retry. Retries should use exponential backoff with jitter; retrying immediately in a tight loop triggers rate limiting.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_idempotency] API Idempotency
All POST endpoints accept an Idempotency-Key header. A repeated request with the same key and an identical payload returns the original response without creating a second resource. A repeated key with a different payload returns 409. Keys are retained for 24 hours. Clients should generate a UUID per logical operation, not per HTTP attempt, so that retries reuse the same key.
