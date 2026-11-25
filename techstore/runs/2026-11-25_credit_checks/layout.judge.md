# Prompt-layout answers to grade

Store date: 30 September 2026. Two versions of the agent answered the SAME long chats.
`classic`: documents in the instructions; `cache`: documents placed in the customer's message (for provider caching). Each version saw its own earlier answers.

========== c01+c02+c03 turn 1 ==========
CUSTOMER: Hi, what's happening with order 48712?

--- version `classic`
Your order #48712 for the SoundWave X200 Wireless Headphones (₹12,999) is **Processing**, with estimated delivery on **1 October 2026**. As of today, 30 September, it isn’t overdue.

No courier or tracking number has been assigned yet. Once it’s marked Shipped, you’ll receive a tracking link by email and SMS; it will also appear under Orders in your account.
   evidence docs: ['ship_tracking', 'api_inventory', 'pol_damaged_in_transit', 'pol_bulk_orders']  orders: ['48712']

--- version `cache`
Your order #48712 for the SoundWave X200 Wireless Headphones (₹12,999) is **Processing**, with an estimated delivery date of **1 October 2026**. As of 30 September, it isn’t overdue.

No courier or tracking ID has been assigned yet. When it’s marked Shipped, you’ll receive a tracking link by email and SMS; you can also find it under Orders in your account. Tracking can take “up to 12 hours after dispatch” to become active.
   evidence docs: ['ship_tracking', 'api_inventory', 'pol_damaged_in_transit', 'pol_bulk_orders']  orders: ['48712']

EVIDENCE:
--- [api_inventory] Inventory Endpoint
GET /v1/inventory returns stock by SKU and warehouse. Quantities are eventually consistent with up to 60 seconds of lag, so a successful inventory read does not guarantee a subsequent order will succeed; handle 422 out_of_stock on order creation. The inventory.low webhook fires when a SKU falls below its configured threshold.
--- [pol_bulk_orders] Bulk and Business Orders
Orders above 10 units of a single SKU are treated as business orders and require a GSTIN. Bulk pricing is quoted by the business desk and is not available at checkout. Business orders ship in 5 to 10 business days and carry a 15-day return window rather than 30 days.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [ship_tracking] Tracking an Order
A tracking link is emailed and sent by SMS when the order is marked Shipped. Tracking can also be seen under Orders in the account. Tracking information can take up to 12 hours after dispatch to become active with the courier. If tracking has not updated for more than 48 hours, contact support so a courier trace can be raised.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c01+c02+c03 turn 2 ==========
CUSTOMER: Why do I see three charges on my card for it?

EARLIER CUSTOMER MESSAGES: Hi, what's happening with order 48712?

--- version `classic`
I’m sorry for the confusion. Only **one order was created**—order #48712. The three card entries are:

| Date | Amount | Status |
|---|---:|---|
| 27 September 2026 | ₹12,999 | Settled payment for order #48712 |
| 27 September 2026 | ₹12,999 | Duplicate authorisation hold, reversed on **29 September 2026** |
| 27 September 2026 | ₹12,999 | Duplicate authorisation hold, expected to reverse by **4 October 2026** |

The extra authorisations resulted from a duplicate payment-page submission. These holds reverse automatically within **“5 to 7 business days.”**

1. Keep the settled ₹12,999 payment—it covers your order.
2. Check your card statement for the hold released on 29 September.
3. Allow until 4 October for the remaining hold to reverse. If it hasn’t reversed by then, I can connect you with a human agent to investigate.
   evidence docs: ['bill_duplicate_charge', 'ship_charges', 'bill_emi', 'bill_payment_methods']  orders: ['48712']

--- version `cache`
I understand why three entries look concerning. For order #48712, only **one is a settled payment**; the other two are duplicate authorisation holds caused by repeated payment submission.

| Date | Amount | Status |
|---|---|---|
| 27 September 2026 | ₹12,999 | Settled payment for order #48712 |
| 27 September 2026 | ₹12,999 | Duplicate hold—already reversed on 29 September 2026 |
| 27 September 2026 | ₹12,999 | Duplicate hold—expected to reverse by 4 October 2026 |

**Resolution:**
1. Keep the settled ₹12,999 payment—it corresponds to your single order.
2. One duplicate hold has already been released; the remaining hold is scheduled to reverse automatically by 4 October. The policy allows “5 to 7 business days” for automatic reversals.
3. If the remaining hold has not reversed after 4 October, I can connect you with a human agent to investigate.
   evidence docs: ['bill_duplicate_charge', 'ship_charges', 'bill_emi', 'bill_payment_methods']  orders: ['48712']

EVIDENCE:
--- [bill_duplicate_charge] Duplicate or Multiple Charges
A duplicate charge occurs when a payment page is submitted more than once. Only one order is created; the additional authorisations are holds that reverse automatically within 5 to 7 business days. If two or more distinct orders were created, each must be cancelled separately and each refund is processed separately, so a customer may see refunds arrive on different days. When resolving a multi-charge dispute, list every charge with its date and amount, state which one corresponds to the surviving order, and give the expected reversal date for each of the others.
--- [bill_emi] EMI and No-Cost EMI
EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount. If an order paid by no-cost EMI is returned, the discount is deducted from the refund and the bank may still charge interest already levied; the bank must be contacted to cancel the EMI plan.
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.
--- [ship_charges] Delivery Charges
Delivery is free on all orders above ₹999. Below that a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149 and is available in metro cities only for orders placed before 2 PM. Delivery charges are refunded if the order is cancelled before shipping or if the item arrives damaged.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c01+c02+c03 turn 3 ==========
CUSTOMER: When will the extra money come back?

EARLIER CUSTOMER MESSAGES: Hi, what's happening with order 48712? | Why do I see three charges on my card for it?

--- version `classic`
The two extra entries are authorisation holds, not additional settled payments:

- **27 September — ₹12,999:** Settled payment for order #48712; this stays as your order payment.
- **27 September — ₹12,999:** Duplicate hold already reversed on **29 September 2026**.
- **27 September — ₹12,999:** Duplicate hold expected to reverse by **4 October 2026**.

Duplicate holds reverse automatically within **“5 to 7 business days.”**

1. Check your card statement for the reversal dated 29 September.
2. Allow until 4 October for the remaining hold to reverse.
3. If either reversal is missing after its stated date, I can connect you with a human agent to investigate.
   evidence docs: ['bill_duplicate_charge', 'bill_chargeback', 'bill_emi', 'bill_refund_to_closed_card']  orders: ['48712']

--- version `cache`
One extra hold has already been released; the other is expected to reverse **by 4 October 2026**.

Here’s every card entry for order #48712:

| Date | Amount | Status |
|---|---|---|
| 27 September 2026 | ₹12,999 | Settled payment for order #48712—this payment remains |
| 27 September 2026 | ₹12,999 | Duplicate authorisation hold—reversed on 29 September 2026 |
| 27 September 2026 | ₹12,999 | Duplicate authorisation hold—expected to reverse by 4 October 2026 |

**Next steps:**
1. No action is needed for the automatic reversal. The policy timeframe is “5 to 7 business days.”
2. Wait until 4 October for the remaining hold to reverse; as of 30 September, it isn’t overdue.
3. If it remains after that date, I can connect you with a human agent to investigate.
   evidence docs: ['bill_duplicate_charge', 'bill_chargeback', 'bill_emi', 'bill_refund_to_closed_card']  orders: ['48712']

EVIDENCE:
--- [bill_chargeback] Bank Chargebacks and Disputes
If a customer raises a chargeback with their bank, the order is frozen and any parallel TechStore refund is suspended to prevent a double credit. Chargebacks take 45 to 90 days to resolve through the card network. Contacting support directly is almost always faster than a chargeback, and support can withdraw a chargeback by providing the bank with resolution evidence.
--- [bill_duplicate_charge] Duplicate or Multiple Charges
A duplicate charge occurs when a payment page is submitted more than once. Only one order is created; the additional authorisations are holds that reverse automatically within 5 to 7 business days. If two or more distinct orders were created, each must be cancelled separately and each refund is processed separately, so a customer may see refunds arrive on different days. When resolving a multi-charge dispute, list every charge with its date and amount, state which one corresponds to the surviving order, and give the expected reversal date for each of the others.
--- [bill_emi] EMI and No-Cost EMI
EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount. If an order paid by no-cost EMI is returned, the discount is deducted from the refund and the bank may still charge interest already levied; the bank must be contacted to cancel the EMI plan.
--- [bill_refund_to_closed_card] Refund to a Closed or Expired Card
Refunds are issued to the original payment method. If that card is closed or expired, the issuing bank still routes the credit to the underlying account in most cases. If the bank rejects the credit, the funds return to TechStore within 10 business days, after which support can arrange a bank transfer once account details and identity are verified. We cannot refund to a different card at the customer's request when the original card is still active.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c01+c02+c03 turn 4 ==========
CUSTOMER: Can I still cancel the order?

EARLIER CUSTOMER MESSAGES: Hi, what's happening with order 48712? | Why do I see three charges on my card for it? | When will the extra money come back?

--- version `classic`
Yes. Order #48712 is still **Processing**, so it can be cancelled **“free of charge at any time before it is marked Shipped.”**

The settled payment of **₹12,999** would be refunded to your original credit card within **“5 to 7 business days.”** The remaining duplicate hold reverses separately, by **4 October 2026**.

I can connect you with a human agent to request the cancellation.
   evidence docs: ['pol_cancellation', 'bill_failed_payment', 'bill_cod_refund', 'bill_refund_to_closed_card']  orders: ['48712']

--- version `cache`
Yes—order #48712 is still **Processing**, so it can be cancelled “free of charge” before it is marked Shipped.

If cancelled, the ₹12,999 payment will be refunded to your original credit card within “5 to 7 business days.” The duplicate holds are separate from this cancellation refund.

I can’t cancel the order directly, but I can connect you with a human agent to arrange it.
   evidence docs: ['pol_cancellation', 'bill_failed_payment', 'bill_cod_refund', 'bill_refund_to_closed_card']  orders: ['48712']

EVIDENCE:
--- [bill_cod_refund] Refunds on Cash-on-Delivery Orders
Cash-on-delivery orders cannot be refunded to a payment method because none was used. Refunds are made by bank transfer after the customer submits account number and IFSC through the secure link sent by support. Transfers complete within 5 to 7 business days of verification. The ₹49 COD handling fee is refunded only if the order is cancelled before dispatch.
--- [bill_failed_payment] Payment Failed but Money Debited
If a payment fails but the amount is debited, the bank has placed a temporary hold that is released automatically. Card and UPI holds reverse within 5 to 7 business days; net banking can take up to 10. No order is created for a failed payment, so there is nothing to cancel. If the amount has not reversed after the stated period, contact support with the bank reference number and TechStore raises a chargeback trace with the payment gateway.
--- [bill_refund_to_closed_card] Refund to a Closed or Expired Card
Refunds are issued to the original payment method. If that card is closed or expired, the issuing bank still routes the credit to the underlying account in most cases. If the bank rejects the credit, the funds return to TechStore within 10 business days, after which support can arrange a bank transfer once account details and identity are verified. We cannot refund to a different card at the customer's request when the original card is still active.
--- [pol_cancellation] Order Cancellation
An order can be cancelled free of charge at any time before it is marked Shipped. Once shipped, cancellation is not possible; the customer should refuse delivery or raise a return after delivery. Cancelled orders are refunded in full, including any delivery charge paid, within 5 to 7 business days.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c01+c02+c03 turn 5 ==========
CUSTOMER: If I cancel, how long until I get the refund?

EARLIER CUSTOMER MESSAGES: Hi, what's happening with order 48712? | Why do I see three charges on my card for it? | When will the extra money come back? | Can I still cancel the order?

--- version `classic`
If you cancel order #48712 while it’s still **Processing**, your **₹12,999** payment will be refunded in full to your original credit card within **“5 to 7 business days”** of cancellation.

The duplicate authorisation hold is separate and is due to reverse by **4 October 2026**.
   evidence docs: ['pol_cancellation', 'bill_refund_to_closed_card', 'bill_cod_refund', 'bill_chargeback']  orders: ['48712']

--- version `cache`
If you cancel order #48712 while it’s still **Processing**, your full ₹12,999 payment will be refunded to your original credit card within “5 to 7 business days.”

That refund is separate from the two duplicate holds:

| Entry date | Amount | Status |
|---|---|---|
| 27 September 2026 | ₹12,999 | Settled payment for order #48712—refundable upon cancellation |
| 27 September 2026 | ₹12,999 | Duplicate hold—reversed on 29 September 2026 |
| 27 September 2026 | ₹12,999 | Duplicate hold—expected to reverse by 4 October 2026 |

1. I can connect you with a human agent to arrange cancellation before the order is marked Shipped.
2. Once cancelled, allow “5 to 7 business days” for the payment refund. The remaining duplicate hold reverses separately.
   evidence docs: ['pol_cancellation', 'bill_refund_to_closed_card', 'bill_cod_refund', 'bill_chargeback']  orders: ['48712']

EVIDENCE:
--- [bill_chargeback] Bank Chargebacks and Disputes
If a customer raises a chargeback with their bank, the order is frozen and any parallel TechStore refund is suspended to prevent a double credit. Chargebacks take 45 to 90 days to resolve through the card network. Contacting support directly is almost always faster than a chargeback, and support can withdraw a chargeback by providing the bank with resolution evidence.
--- [bill_cod_refund] Refunds on Cash-on-Delivery Orders
Cash-on-delivery orders cannot be refunded to a payment method because none was used. Refunds are made by bank transfer after the customer submits account number and IFSC through the secure link sent by support. Transfers complete within 5 to 7 business days of verification. The ₹49 COD handling fee is refunded only if the order is cancelled before dispatch.
--- [bill_refund_to_closed_card] Refund to a Closed or Expired Card
Refunds are issued to the original payment method. If that card is closed or expired, the issuing bank still routes the credit to the underlying account in most cases. If the bank rejects the credit, the funds return to TechStore within 10 business days, after which support can arrange a bank transfer once account details and identity are verified. We cannot refund to a different card at the customer's request when the original card is still active.
--- [pol_cancellation] Order Cancellation
An order can be cancelled free of charge at any time before it is marked Shipped. Once shipped, cancellation is not possible; the customer should refuse delivery or raise a return after delivery. Cancelled orders are refunded in full, including any delivery charge paid, within 5 to 7 business days.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c01+c02+c03 turn 6 ==========
CUSTOMER: Is the X200 good for the gym?

EARLIER CUSTOMER MESSAGES: Hi, what's happening with order 48712? | Why do I see three charges on my card for it? | When will the extra money come back? | Can I still cancel the order? | If I cancel, how long until I get the refund?

--- version `classic`
The SoundWave X200 has **40-hour battery life**, **35 dB hybrid active noise cancellation**, and a **250 g over-ear design**—features worth considering for gym use.

I don't have information about its sweat or water resistance or how securely it stays on during exercise.

Also note that it is **“Non-returnable once the seal is opened, under the hygiene policy.”**
   evidence docs: ['prod_x200', 'pol_cancellation', 'bill_refund_to_closed_card', 'pol_return_window']  orders: ['48712']

--- version `cache`
The X200 has some useful gym features: **40-hour battery life**, wireless Bluetooth 5.3, and hybrid active noise cancellation rated at 35 dB. It’s an over-ear model weighing 250 g.

I don't have information about its sweat or water resistance or how securely it fits during exercise.

Before buying for workouts, note that it’s “Non-returnable once the seal is opened, under the hygiene policy.”
   evidence docs: ['prod_x200', 'pol_cancellation', 'bill_refund_to_closed_card', 'pol_return_window']  orders: ['48712']

EVIDENCE:
--- [bill_refund_to_closed_card] Refund to a Closed or Expired Card
Refunds are issued to the original payment method. If that card is closed or expired, the issuing bank still routes the credit to the underlying account in most cases. If the bank rejects the credit, the funds return to TechStore within 10 business days, after which support can arrange a bank transfer once account details and identity are verified. We cannot refund to a different card at the customer's request when the original card is still active.
--- [pol_cancellation] Order Cancellation
An order can be cancelled free of charge at any time before it is marked Shipped. Once shipped, cancellation is not possible; the customer should refuse delivery or raise a return after delivery. Cancelled orders are refunded in full, including any delivery charge paid, within 5 to 7 business days.
--- [pol_return_window] Return Window
TechStore accepts returns within 30 days of delivery. The 30 days are counted from the delivery date shown on the tracking record, not the order date. Items must be returned in their original packaging with all accessories, manuals and free gifts included. A return raised on day 31 or later is rejected automatically by the returns system.
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c01+c02+c03 turn 7 ==========
CUSTOMER: What about the Y500?

EARLIER CUSTOMER MESSAGES: Hi, what's happening with order 48712? | Why do I see three charges on my card for it? | When will the extra money come back? | Can I still cancel the order? | If I cancel, how long until I get the refund? | Is the X200 good for the gym?

--- version `classic`
The **SoundWave Y500** costs **₹24,999** and offers:

- **60-hour battery life**
- **45 dB adaptive active noise cancellation** with transparency mode
- **Memory-foam earcups** and a **268 g over-ear design**

I don't have information about its sweat or water resistance or how securely it stays on during exercise, so I can’t confirm its suitability for the gym.

Its return restriction is **“Non-returnable once the seal is opened, under the hygiene policy.”**
   evidence docs: ['prod_x200', 'prod_y500', 'prod_aurawatch3', 'prod_aurawatch_pro']  orders: ['48712']

--- version `cache`
The **SoundWave Y500 costs ₹24,999** and upgrades on the X200 with:

- **60-hour battery life** versus 40 hours.
- **45 dB adaptive noise cancellation** with transparency mode versus 35 dB hybrid ANC.
- Memory-foam earcups, wireless charging, and pairing with three devices.
- A slightly higher weight: **268 g versus 250 g**.

It’s recommended over the X200 for noisy offices and flights, but I don't have information about its sweat or water resistance or secure fit during gym workouts.

It’s also “Non-returnable once the seal is opened, under the hygiene policy.”
   evidence docs: ['prod_x200', 'prod_y500', 'prod_aurawatch3', 'prod_aurawatch_pro']  orders: ['48712']

EVIDENCE:
--- [prod_aurawatch3] AuraWatch 3 Smartwatch
Fitness smartwatch. Price ₹8,999. 1.4-inch AMOLED display, 14-day battery, heart-rate and SpO2 sensors, built-in GPS, 5 ATM water resistance, sleep tracking. Compatible with Android 9 and above and iOS 14 and above. 1-year manufacturer warranty. Worn on the wrist, therefore non-returnable once used, under the hygiene policy.
--- [prod_aurawatch_pro] AuraWatch Pro Smartwatch
Premium fitness smartwatch. Price ₹15,999. 1.5-inch AMOLED always-on display, 18-day battery, ECG and SpO2 sensors, dual-band GPS, 10 ATM water resistance, offline maps, 100 sport modes. Compatible with Android 10 and above and iOS 15 and above. 2-year manufacturer warranty. Non-returnable once used, under the hygiene policy.
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [prod_y500] SoundWave Y500 Premium Headphones
Flagship over-ear wireless headphones. Price ₹24,999. 60-hour battery life, Bluetooth 5.4, adaptive active noise cancellation rated at 45 dB with transparency mode, LDAC and aptX Lossless support, USB-C and wireless charging, multipoint pairing with three devices, 268 g, memory-foam earcups. Available in Graphite and Sand. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy. Recommended over the X200 for noisy environments such as open-plan offices and flights.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c01+c02+c03 turn 8 ==========
CUSTOMER: Which one has the longer battery?

EARLIER CUSTOMER MESSAGES: Hi, what's happening with order 48712? | Why do I see three charges on my card for it? | When will the extra money come back? | Can I still cancel the order? | If I cancel, how long until I get the refund? | Is the X200 good for the gym? | What about the Y500?

--- version `classic`
The **Y500** has the longer battery life: **60 hours**, compared with **40 hours** for the X200—**20 hours more**.
   evidence docs: ['prod_y500', 'prod_voltbank20k', 'tsg_watch_battery', 'prod_x200']  orders: ['48712']

--- version `cache`
The **Y500** has the longer battery life: **60 hours**, compared with **40 hours** for the X200—20 hours more.
   evidence docs: ['prod_y500', 'prod_voltbank20k', 'tsg_watch_battery', 'prod_x200']  orders: ['48712']

EVIDENCE:
--- [prod_voltbank20k] VoltBank 20000mAh Power Bank
20000 mAh power bank. Price ₹2,999. 65 W USB-C output, 20 W USB-A output, pass-through charging, LED capacity display, 389 g. Its capacity is under 100 Wh; check your airline's rules before carrying it on a flight. Can charge the PulseBook Air 13 once or the NovaTab 11 twice. 1-year manufacturer warranty.
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [prod_y500] SoundWave Y500 Premium Headphones
Flagship over-ear wireless headphones. Price ₹24,999. 60-hour battery life, Bluetooth 5.4, adaptive active noise cancellation rated at 45 dB with transparency mode, LDAC and aptX Lossless support, USB-C and wireless charging, multipoint pairing with three devices, 268 g, memory-foam earcups. Available in Graphite and Sand. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy. Recommended over the X200 for noisy environments such as open-plan offices and flights.
--- [tsg_watch_battery] Smartwatch Battery Draining Fast
Always-on display reduces AuraWatch Pro battery life from 18 days to roughly 6. Continuous SpO2 monitoring and dual-band GPS also shorten runtime substantially. Disable always-on display and continuous SpO2 to restore rated life. If runtime is under 50 percent of the rated figure with those features off, the battery is a warranty defect.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c01+c02+c03 turn 9 ==========
CUSTOMER: Can I return it if I open the box and don't like it?

EARLIER CUSTOMER MESSAGES: Hi, what's happening with order 48712? | Why do I see three charges on my card for it? | When will the extra money come back? | Can I still cancel the order? | If I cancel, how long until I get the refund? | Is the X200 good for the gym? | What about the Y500? | Which one has the longer battery?

--- version `classic`
I don't have that information. I can connect you with a human agent who can help.

I’m sorry—my earlier statement that opened headphones are non-returnable wasn’t supported by the available policy documents.
   evidence docs: ['prod_voltbank20k', 'pol_damaged_in_transit', 'pol_exchange', 'prod_voltcharge65']  orders: ['48712']

--- version `cache`
For both the X200 and Y500, the policy is **“Non-returnable once the seal is opened, under the hygiene policy.”** So you can’t open the seal, try the headphones, and return them simply because you don’t like them.

If they arrive damaged or the wrong item is delivered, that’s separate: report it “within 48 hours of delivery” with photographs of the package and product for a free replacement.
   evidence docs: ['prod_voltbank20k', 'pol_damaged_in_transit', 'pol_exchange', 'prod_voltcharge65']  orders: ['48712']

EVIDENCE:
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [pol_exchange] Exchange Policy
An exchange can be requested within 30 days of delivery for a different size, colour or variant of the same product line, subject to stock. If the new variant costs more, the difference is charged before dispatch. If it costs less, the difference is refunded. Only one exchange is permitted per order line.
--- [prod_voltbank20k] VoltBank 20000mAh Power Bank
20000 mAh power bank. Price ₹2,999. 65 W USB-C output, 20 W USB-A output, pass-through charging, LED capacity display, 389 g. Its capacity is under 100 Wh; check your airline's rules before carrying it on a flight. Can charge the PulseBook Air 13 once or the NovaTab 11 twice. 1-year manufacturer warranty.
--- [prod_voltcharge65] VoltCharge 65W GaN Charger
65 W GaN fast charger. Price ₹2,499. Two USB-C ports and one USB-A, supports Power Delivery 3.1 and Quick Charge 5, foldable pins. Compatible with PulseBook 14, NovaTab 11 and all SoundWave headphones. Not sufficient to charge the PulseBook Pro 16 at full speed, which requires 100 W. 1-year manufacturer warranty.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c01+c02+c03 turn 10 ==========
CUSTOMER: I want to return my PulseBook 14, it was delivered 20 days ago

EARLIER CUSTOMER MESSAGES: Hi, what's happening with order 48712? | Why do I see three charges on my card for it? | When will the extra money come back? | Can I still cancel the order? | If I cancel, how long until I get the refund? | Is the X200 good for the gym? | What about the Y500? | Which one has the longer battery? | Can I return it if I open the box and don't like it?

--- version `classic`
Your PulseBook 14 is within the **“30 days of delivery”** return window, since it was delivered 20 days ago.

It must be returned in its **“original packaging with all accessories, manuals and free gifts included.”**

I can connect you with a human agent to help arrange the return.
   evidence docs: ['prod_pulsebook14', 'pol_return_window', 'pol_damaged_in_transit', 'svc_accidental_damage']  orders: ['48712']

--- version `cache`
Your PulseBook 14 is within the **“30 days of delivery”** return window if it was delivered 20 days ago. It must be returned in its original packaging with all accessories, manuals and free gifts included.

The record provided is for order #48712, which contains X200 headphones, not the laptop. Please share your PulseBook 14 order number so a human agent can help arrange the return.
   evidence docs: ['prod_pulsebook14', 'pol_return_window', 'pol_damaged_in_transit', 'svc_accidental_damage']  orders: ['48712']

EVIDENCE:
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [pol_return_window] Return Window
TechStore accepts returns within 30 days of delivery. The 30 days are counted from the delivery date shown on the tracking record, not the order date. Items must be returned in their original packaging with all accessories, manuals and free gifts included. A return raised on day 31 or later is rejected automatically by the returns system.
--- [prod_pulsebook14] PulseBook 14 Laptop
14-inch ultrabook. Price ₹64,999. Intel Core Ultra 5, 16 GB LPDDR5 RAM, 512 GB NVMe SSD, 14-inch 2.8K OLED display at 90 Hz, 65 W USB-C charging, 1.29 kg, 12-hour rated battery. Ports: two USB-C Thunderbolt, one USB-A, HDMI 2.1, headphone jack. 2-year manufacturer warranty including one year of accidental damage protection.
--- [svc_accidental_damage] Accidental Damage Protection
PulseBook 14 and PulseBook Pro 16 include one year of accidental damage protection from the delivery date, covering drops and liquid spills. One claim is permitted in the coverage year, with a customer contribution of 10 percent of the product price. Accidental damage protection does not cover theft, loss, or cosmetic damage that does not affect function.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c01+c02+c03 turn 11 ==========
CUSTOMER: Do I need the original box?

EARLIER CUSTOMER MESSAGES: Hi, what's happening with order 48712? | Why do I see three charges on my card for it? | When will the extra money come back? | Can I still cancel the order? | If I cancel, how long until I get the refund? | Is the X200 good for the gym? | What about the Y500? | Which one has the longer battery? | Can I return it if I open the box and don't like it? | I want to return my PulseBook 14, it was delivered 20 days ago

--- version `classic`
I don't have that information. I can connect you with a human agent who can help.

I’m sorry—my earlier statements about requiring original packaging and your return eligibility weren’t supported by the available policy documents.
   evidence docs: ['prod_pulsebook14', 'svc_accidental_damage', 'prod_pulsebook_pro16', 'pol_damaged_in_transit']  orders: ['48712']

--- version `cache`
Yes. Returns must be in their **“original packaging”**, including the original box, with **“all accessories, manuals and free gifts included.”**
   evidence docs: ['prod_pulsebook14', 'svc_accidental_damage', 'prod_pulsebook_pro16', 'pol_damaged_in_transit']  orders: ['48712']

EVIDENCE:
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [prod_pulsebook14] PulseBook 14 Laptop
14-inch ultrabook. Price ₹64,999. Intel Core Ultra 5, 16 GB LPDDR5 RAM, 512 GB NVMe SSD, 14-inch 2.8K OLED display at 90 Hz, 65 W USB-C charging, 1.29 kg, 12-hour rated battery. Ports: two USB-C Thunderbolt, one USB-A, HDMI 2.1, headphone jack. 2-year manufacturer warranty including one year of accidental damage protection.
--- [prod_pulsebook_pro16] PulseBook Pro 16 Laptop
16-inch creator laptop. Price ₹1,34,999. Intel Core Ultra 9, 32 GB RAM, 1 TB NVMe SSD, discrete RTX 4060 graphics, 16-inch 3.2K OLED at 120 Hz, 100 W USB-C charging, 1.95 kg. 2-year manufacturer warranty including one year of accidental damage protection.
--- [svc_accidental_damage] Accidental Damage Protection
PulseBook 14 and PulseBook Pro 16 include one year of accidental damage protection from the delivery date, covering drops and liquid spills. One claim is permitted in the coverage year, with a customer contribution of 10 percent of the product price. Accidental damage protection does not cover theft, loss, or cosmetic damage that does not affect function.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c01+c02+c03 turn 12 ==========
CUSTOMER: How long will the refund take?

EARLIER CUSTOMER MESSAGES: Hi, what's happening with order 48712? | Why do I see three charges on my card for it? | When will the extra money come back? | Can I still cancel the order? | If I cancel, how long until I get the refund? | Is the X200 good for the gym? | What about the Y500? | Which one has the longer battery? | Can I return it if I open the box and don't like it? | I want to return my PulseBook 14, it was delivered 20 days ago | Do I need the original box?

--- version `classic`
Once your returned item is **received and inspected at our warehouse**, the refund is initiated **“within 2 business days.”** It then reaches your original payment method in:

- **Cards or UPI:** “5 to 7 business days”
- **Net banking:** “up to 10 business days”

Refunds are always issued to the **original payment method**.
   evidence docs: ['pol_refund_timeline', 'pol_return_window', 'pol_damaged_in_transit', 'ship_open_box']  orders: ['48712']

--- version `cache`
For your PulseBook 14 return, the timeline starts once it is **received and inspected at our warehouse**:

- Refund initiated within **“2 business days.”**
- Money reaches your original payment method in **“5 to 7 business days”** for cards or UPI, or **“up to 10 business days”** for net banking.

I don't have information about your PulseBook order’s payment method or whether its return has reached the warehouse.
   evidence docs: ['pol_refund_timeline', 'pol_return_window', 'pol_damaged_in_transit', 'ship_open_box']  orders: ['48712']

EVIDENCE:
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [pol_refund_timeline] Refund Processing Time
Once a returned item is received and inspected at our warehouse, refunds are initiated within 2 business days. The money reaches the original payment method in 5 to 7 business days for cards and UPI, and up to 10 business days for net banking. Refunds are always issued to the original payment method; we cannot redirect a refund to a different card or account.
--- [pol_return_window] Return Window
TechStore accepts returns within 30 days of delivery. The 30 days are counted from the delivery date shown on the tracking record, not the order date. Items must be returned in their original packaging with all accessories, manuals and free gifts included. A return raised on day 31 or later is rejected automatically by the returns system.
--- [ship_open_box] Open-Box Delivery
Open-box delivery is available in 22 cities on orders above ₹20,000. The courier opens the package in the customer's presence for inspection before handover. Refusal at open-box inspection is free and refunds process within 5 to 7 business days. Open-box delivery adds 1 business day to the estimate.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c01+c02+c03 turn 13 ==========
CUSTOMER: And if I paid with net banking?

EARLIER CUSTOMER MESSAGES: Hi, what's happening with order 48712? | Why do I see three charges on my card for it? | When will the extra money come back? | Can I still cancel the order? | If I cancel, how long until I get the refund? | Is the X200 good for the gym? | What about the Y500? | Which one has the longer battery? | Can I return it if I open the box and don't like it? | I want to return my PulseBook 14, it was delivered 20 days ago | Do I need the original box? | How long will the refund take?

--- version `classic`
For net banking, once your return is received and inspected at our warehouse, the refund is initiated **“within 2 business days.”** It then takes **“up to 10 business days”** to reach your original bank account.
   evidence docs: ['pol_refund_timeline', 'bill_chargeback', 'bill_refund_to_closed_card', 'bill_cod_refund']  orders: ['48712']

--- version `cache`
For net banking, the refund is initiated within “2 business days” after your returned item is received and inspected at the warehouse. The money then takes “up to 10 business days” to reach your original net banking account.
   evidence docs: ['pol_refund_timeline', 'bill_chargeback', 'bill_refund_to_closed_card', 'bill_cod_refund']  orders: ['48712']

EVIDENCE:
--- [bill_chargeback] Bank Chargebacks and Disputes
If a customer raises a chargeback with their bank, the order is frozen and any parallel TechStore refund is suspended to prevent a double credit. Chargebacks take 45 to 90 days to resolve through the card network. Contacting support directly is almost always faster than a chargeback, and support can withdraw a chargeback by providing the bank with resolution evidence.
--- [bill_cod_refund] Refunds on Cash-on-Delivery Orders
Cash-on-delivery orders cannot be refunded to a payment method because none was used. Refunds are made by bank transfer after the customer submits account number and IFSC through the secure link sent by support. Transfers complete within 5 to 7 business days of verification. The ₹49 COD handling fee is refunded only if the order is cancelled before dispatch.
--- [bill_refund_to_closed_card] Refund to a Closed or Expired Card
Refunds are issued to the original payment method. If that card is closed or expired, the issuing bank still routes the credit to the underlying account in most cases. If the bank rejects the credit, the funds return to TechStore within 10 business days, after which support can arrange a bank transfer once account details and identity are verified. We cannot refund to a different card at the customer's request when the original card is still active.
--- [pol_refund_timeline] Refund Processing Time
Once a returned item is received and inspected at our warehouse, refunds are initiated within 2 business days. The money reaches the original payment method in 5 to 7 business days for cards and UPI, and up to 10 business days for net banking. Refunds are always issued to the original payment method; we cannot redirect a refund to a different card or account.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c04+c05+c06 turn 1 ==========
CUSTOMER: How do I reset my password?

--- version `classic`
1. Select **Forgot Password** on the TechStore sign-in page.
2. Follow the reset link emailed to you. It is valid for **30 minutes**.
3. If the email doesn’t arrive, check your spam folder and confirm you entered the email address registered to your account.

After three failed sign-in attempts, your account is locked for **15 minutes**.
   evidence docs: ['acc_password', 'acc_two_factor', 'bill_refund_to_closed_card', 'api_auth']  orders: []

--- version `cache`
1. Select **Forgot Password** on the TechStore sign-in page.
2. Enter your registered email address. You’ll receive a reset link “valid for 30 minutes.”
3. Open the link to reset your password.

If the email doesn’t arrive, check your spam folder and confirm you entered the email address registered to your account.
   evidence docs: ['acc_password', 'acc_two_factor', 'bill_refund_to_closed_card', 'api_auth']  orders: []

EVIDENCE:
--- [acc_password] Password Reset
Use Forgot Password on the sign-in page. A reset link valid for 30 minutes is emailed. If the email does not arrive, check spam and confirm the address matches the registered one; for privacy we do not disclose whether an address is registered. After three failed sign-in attempts the account is locked for 15 minutes.
--- [acc_two_factor] Two-Factor Authentication
Two-factor authentication can be enabled from Security in the account, using an authenticator app or SMS. Enabling 2FA signs out all other sessions. To disable 2FA, current authentication is required; if the device is lost, identity is verified with the last order details and a government ID, and removal takes up to 48 hours.
--- [api_auth] API Authentication and 401 Errors
Authenticate with Authorization: Bearer <token>. A 401 means the token is missing, malformed, expired or from the wrong environment; sandbox tokens rejected by production is the most common cause. Tokens expire 90 days after issue and can be rotated in the dashboard without downtime, since the previous token stays valid for 24 hours after rotation.
--- [bill_refund_to_closed_card] Refund to a Closed or Expired Card
Refunds are issued to the original payment method. If that card is closed or expired, the issuing bank still routes the credit to the underlying account in most cases. If the bank rejects the credit, the funds return to TechStore within 10 business days, after which support can arrange a bank transfer once account details and identity are verified. We cannot refund to a different card at the customer's request when the original card is still active.

========== c04+c05+c06 turn 2 ==========
CUSTOMER: The reset email never came

EARLIER CUSTOMER MESSAGES: How do I reset my password?

--- version `classic`
Sorry the reset email hasn’t arrived. Please try these steps:

1. Check your spam folder.
2. Confirm the email address you entered matches the one registered to your account. For privacy, we do not disclose whether an address is registered.
3. Use **Forgot Password** on the sign-in page again. The reset link is “valid for 30 minutes.”

If it still doesn’t arrive, I can connect you with a human agent to help.
   evidence docs: ['acc_password', 'acc_create', 'bill_refund_to_closed_card', 'api_auth']  orders: []

--- version `cache`
1. Check your spam folder for the reset email.
2. Confirm the email address you entered matches your registered address. For privacy, “we do not disclose whether an address is registered.”
3. Use **Forgot Password** on the sign-in page to request another link. Each reset link is “valid for 30 minutes.”
   evidence docs: ['acc_password', 'acc_create', 'bill_refund_to_closed_card', 'api_auth']  orders: []

EVIDENCE:
--- [acc_create] Creating and Verifying an Account
An account is created with an email address or an Indian mobile number and verified by a one-time password valid for 10 minutes. A maximum of five OTPs may be requested per hour. An account is required to place an order; guest checkout is not offered.
--- [acc_password] Password Reset
Use Forgot Password on the sign-in page. A reset link valid for 30 minutes is emailed. If the email does not arrive, check spam and confirm the address matches the registered one; for privacy we do not disclose whether an address is registered. After three failed sign-in attempts the account is locked for 15 minutes.
--- [api_auth] API Authentication and 401 Errors
Authenticate with Authorization: Bearer <token>. A 401 means the token is missing, malformed, expired or from the wrong environment; sandbox tokens rejected by production is the most common cause. Tokens expire 90 days after issue and can be rotated in the dashboard without downtime, since the previous token stays valid for 24 hours after rotation.
--- [bill_refund_to_closed_card] Refund to a Closed or Expired Card
Refunds are issued to the original payment method. If that card is closed or expired, the issuing bank still routes the credit to the underlying account in most cases. If the bank rejects the credit, the funds return to TechStore within 10 business days, after which support can arrange a bank transfer once account details and identity are verified. We cannot refund to a different card at the customer's request when the original card is still active.

========== c04+c05+c06 turn 3 ==========
CUSTOMER: I tried logging in 3 times and now it says locked

EARLIER CUSTOMER MESSAGES: How do I reset my password? | The reset email never came

--- version `classic`
After three failed sign-in attempts, your account is “locked for 15 minutes.”

1. Wait 15 minutes before trying to sign in again.
2. If you still need to reset your password, use **Forgot Password** on the sign-in page. Check spam and confirm you entered your registered email address.

Since the reset email hasn’t arrived, I can connect you with a human agent for help.
   evidence docs: ['acc_password', 'api_auth', 'api_timeouts', 'api_error_codes']  orders: []

--- version `cache`
1. Wait 15 minutes before trying to sign in again. After “three failed sign-in attempts,” your account is “locked for 15 minutes.”
2. If you’ve forgotten your password, use **Forgot Password** on the sign-in page. The reset link is emailed and is “valid for 30 minutes.”
   evidence docs: ['acc_password', 'api_auth', 'api_timeouts', 'api_error_codes']  orders: []

EVIDENCE:
--- [acc_password] Password Reset
Use Forgot Password on the sign-in page. A reset link valid for 30 minutes is emailed. If the email does not arrive, check spam and confirm the address matches the registered one; for privacy we do not disclose whether an address is registered. After three failed sign-in attempts the account is locked for 15 minutes.
--- [api_auth] API Authentication and 401 Errors
Authenticate with Authorization: Bearer <token>. A 401 means the token is missing, malformed, expired or from the wrong environment; sandbox tokens rejected by production is the most common cause. Tokens expire 90 days after issue and can be rotated in the dashboard without downtime, since the previous token stays valid for 24 hours after rotation.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_timeouts] API Timeouts and Retry Safety
Requests time out server side at 30 seconds. A timeout does not indicate whether the operation completed, so POST requests must be retried with the same Idempotency-Key to avoid duplicates. GET, PUT and DELETE are idempotent by design and safe to retry. Retries should use exponential backoff with jitter; retrying immediately in a tight loop triggers rate limiting.

========== c04+c05+c06 turn 4 ==========
CUSTOMER: How long until I can try again?

EARLIER CUSTOMER MESSAGES: How do I reset my password? | The reset email never came | I tried logging in 3 times and now it says locked

--- version `classic`
You can try again **15 minutes after the account was locked**. The lock lasts “15 minutes” after three failed sign-in attempts.
   evidence docs: ['acc_password', 'api_auth', 'api_timeouts', 'acc_two_factor']  orders: []

--- version `cache`
You can try signing in again 15 minutes after the lock began. After three failed sign-in attempts, your account is “locked for 15 minutes.”
   evidence docs: ['acc_password', 'api_auth', 'api_timeouts', 'acc_two_factor']  orders: []

EVIDENCE:
--- [acc_password] Password Reset
Use Forgot Password on the sign-in page. A reset link valid for 30 minutes is emailed. If the email does not arrive, check spam and confirm the address matches the registered one; for privacy we do not disclose whether an address is registered. After three failed sign-in attempts the account is locked for 15 minutes.
--- [acc_two_factor] Two-Factor Authentication
Two-factor authentication can be enabled from Security in the account, using an authenticator app or SMS. Enabling 2FA signs out all other sessions. To disable 2FA, current authentication is required; if the device is lost, identity is verified with the last order details and a government ID, and removal takes up to 48 hours.
--- [api_auth] API Authentication and 401 Errors
Authenticate with Authorization: Bearer <token>. A 401 means the token is missing, malformed, expired or from the wrong environment; sandbox tokens rejected by production is the most common cause. Tokens expire 90 days after issue and can be rotated in the dashboard without downtime, since the previous token stays valid for 24 hours after rotation.
--- [api_timeouts] API Timeouts and Retry Safety
Requests time out server side at 30 seconds. A timeout does not indicate whether the operation completed, so POST requests must be retried with the same Idempotency-Key to avoid duplicates. GET, PUT and DELETE are idempotent by design and safe to retry. Retries should use exponential backoff with jitter; retrying immediately in a tight loop triggers rate limiting.

========== c04+c05+c06 turn 5 ==========
CUSTOMER: I'm getting a 401 from the orders endpoint

EARLIER CUSTOMER MESSAGES: How do I reset my password? | The reset email never came | I tried logging in 3 times and now it says locked | How long until I can try again?

--- version `classic`
A **401** means “authentication failed.”

1. Confirm your request includes `Authorization: Bearer <token>`.
2. Check that the token matches the environment. Sandbox tokens being rejected by production is the most common cause.
3. Check the token’s age: tokens expire **90 days after issue**.
4. If needed, rotate the token in the dashboard. The previous token stays valid for **24 hours after rotation**, allowing you to update without downtime.
   evidence docs: ['ship_failed_delivery', 'api_auth', 'api_error_codes', 'api_rate_limits']  orders: []

--- version `cache`
A 401 means authentication failed. Try these checks:

1. Send your token using `Authorization: Bearer <token>`.
2. Confirm the token matches the environment. Sandbox tokens used in production are the most common cause.
3. Check that the token is present, correctly formatted and not expired. Tokens “expire 90 days after issue.”
4. If expired, rotate the token in the dashboard and use the new one. Rotation supports no downtime: the previous token “stays valid for 24 hours after rotation.”
   evidence docs: ['ship_failed_delivery', 'api_auth', 'api_error_codes', 'api_rate_limits']  orders: []

EVIDENCE:
--- [api_auth] API Authentication and 401 Errors
Authenticate with Authorization: Bearer <token>. A 401 means the token is missing, malformed, expired or from the wrong environment; sandbox tokens rejected by production is the most common cause. Tokens expire 90 days after issue and can be rotated in the dashboard without downtime, since the previous token stays valid for 24 hours after rotation.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_rate_limits] API Rate Limits and 429 Errors
The Partner API allows 600 requests per minute per token, and 60 per minute for the bulk export endpoints. Exceeding the limit returns 429 with a Retry-After header in seconds. Clients should honour Retry-After and use exponential backoff with jitter. Sustained violation for more than 15 minutes results in a temporary 1-hour block.
--- [ship_failed_delivery] Failed Delivery Attempts
The courier makes three delivery attempts on consecutive business days. After the third failed attempt the parcel is returned to our warehouse and the order is refunded in full, including any delivery charge paid, within 7 business days of the parcel being received back. A customer can reschedule delivery once through the tracking link.

========== c04+c05+c06 turn 6 ==========
CUSTOMER: I'm using my sandbox key against production

EARLIER CUSTOMER MESSAGES: How do I reset my password? | The reset email never came | I tried logging in 3 times and now it says locked | How long until I can try again? | I'm getting a 401 from the orders endpoint

--- version `classic`
That explains the **401**: production rejects sandbox tokens.

1. For production, use `https://api.techstore.example/v1` with a production token issued in the partner dashboard.
2. For sandbox testing, use `https://sandbox.techstore.example/v1` with your sandbox token.
3. Send the token as `Authorization: Bearer <token>` and retry your request.
   evidence docs: ['api_sandbox', 'api_auth', 'api_overview', 'api_error_codes']  orders: []

--- version `cache`
That explains the 401: sandbox and production use “separate credentials.”

1. For production, use a production bearer token issued in the partner dashboard with `https://api.techstore.example/v1`.
2. To keep using your sandbox key, send requests to `https://sandbox.techstore.example/v1`.
3. Include the header `Authorization: Bearer <token>`.
   evidence docs: ['api_sandbox', 'api_auth', 'api_overview', 'api_error_codes']  orders: []

EVIDENCE:
--- [api_auth] API Authentication and 401 Errors
Authenticate with Authorization: Bearer <token>. A 401 means the token is missing, malformed, expired or from the wrong environment; sandbox tokens rejected by production is the most common cause. Tokens expire 90 days after issue and can be rotated in the dashboard without downtime, since the previous token stays valid for 24 hours after rotation.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_overview] TechStore Partner API Overview
The Partner API is a REST API at https://api.techstore.example/v1. All requests require an Authorization header with a bearer token issued in the partner dashboard. Requests and responses are JSON. The API exposes orders, inventory, shipments and webhooks. Sandbox is available at https://sandbox.techstore.example/v1 with separate credentials and synthetic data.
--- [api_sandbox] Sandbox Environment
Sandbox runs at https://sandbox.techstore.example/v1 with separate credentials and synthetic data that resets nightly at 02:00 IST. Sandbox order IDs begin with a 9; production IDs do not. Webhooks fire in sandbox but use a separate signing secret. Sandbox has no rate limit but is not performance representative.

========== c04+c05+c06 turn 7 ==========
CUSTOMER: Where do I get the live key?

EARLIER CUSTOMER MESSAGES: How do I reset my password? | The reset email never came | I tried logging in 3 times and now it says locked | How long until I can try again? | I'm getting a 401 from the orders endpoint | I'm using my sandbox key against production

--- version `classic`
Get your production bearer token from the **TechStore partner dashboard**. Use it with `https://api.techstore.example/v1` in this header:

```http
Authorization: Bearer <token>
```

Your sandbox token won’t work in production.
   evidence docs: ['api_sandbox', 'api_overview', 'api_auth', 'api_error_codes']  orders: []

--- version `cache`
1. Go to the **TechStore partner dashboard**, where production bearer tokens are issued.
2. Use your production token with `https://api.techstore.example/v1` and the header `Authorization: Bearer <token>`.

Sandbox and production use “separate credentials,” so your sandbox key won’t work for live requests.
   evidence docs: ['api_sandbox', 'api_overview', 'api_auth', 'api_error_codes']  orders: []

EVIDENCE:
--- [api_auth] API Authentication and 401 Errors
Authenticate with Authorization: Bearer <token>. A 401 means the token is missing, malformed, expired or from the wrong environment; sandbox tokens rejected by production is the most common cause. Tokens expire 90 days after issue and can be rotated in the dashboard without downtime, since the previous token stays valid for 24 hours after rotation.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_overview] TechStore Partner API Overview
The Partner API is a REST API at https://api.techstore.example/v1. All requests require an Authorization header with a bearer token issued in the partner dashboard. Requests and responses are JSON. The API exposes orders, inventory, shipments and webhooks. Sandbox is available at https://sandbox.techstore.example/v1 with separate credentials and synthetic data.
--- [api_sandbox] Sandbox Environment
Sandbox runs at https://sandbox.techstore.example/v1 with separate credentials and synthetic data that resets nightly at 02:00 IST. Sandbox order IDs begin with a 9; production IDs do not. Webhooks fire in sandbox but use a separate signing secret. Sandbox has no rate limit but is not performance representative.

========== c04+c05+c06 turn 8 ==========
CUSTOMER: Do webhooks use the same key?

EARLIER CUSTOMER MESSAGES: How do I reset my password? | The reset email never came | I tried logging in 3 times and now it says locked | How long until I can try again? | I'm getting a 401 from the orders endpoint | I'm using my sandbox key against production | Where do I get the live key?

--- version `classic`
No. Webhooks use a **webhook secret**, not your API token. Sandbox webhooks also use a **separate signing secret**.

To verify a webhook, compute an HMAC-SHA256 over the **exact raw request body**, keyed with the webhook secret, and compare the hex-encoded result with the `X-TechStore-Signature` header. Do this before parsing the JSON.
   evidence docs: ['api_webhook_events', 'api_webhook_signature', 'api_webhook_retries', 'api_sandbox']  orders: []

--- version `cache`
No—webhooks use a **webhook secret**, not your API bearer token.

Verify `X-TechStore-Signature` using HMAC-SHA256 over the exact raw request body, keyed with the webhook secret and hex encoded. Sandbox webhooks also use a “separate signing secret” from production.
   evidence docs: ['api_webhook_events', 'api_webhook_signature', 'api_webhook_retries', 'api_sandbox']  orders: []

EVIDENCE:
--- [api_sandbox] Sandbox Environment
Sandbox runs at https://sandbox.techstore.example/v1 with separate credentials and synthetic data that resets nightly at 02:00 IST. Sandbox order IDs begin with a 9; production IDs do not. Webhooks fire in sandbox but use a separate signing secret. Sandbox has no rate limit but is not performance representative.
--- [api_webhook_events] Webhook Event Types
Available events: order.created, order.shipped, order.delivered, order.cancelled, order.returned, refund.initiated, refund.completed, inventory.low. Events are subscribed per endpoint in the dashboard. Payloads include the event type, a timestamp, and the affected resource. Event ordering is not guaranteed; use the timestamp rather than arrival order.
--- [api_webhook_retries] Webhook Delivery and Retries
Webhooks expect a 2xx response within 5 seconds. Non-2xx or timeout triggers retries at 1, 5, 25 and 125 minutes, then the endpoint is marked unhealthy and deliveries pause until reactivated in the dashboard. Handlers must be idempotent, because a duplicate delivery is possible even after a successful response. Each delivery carries an X-TechStore-Delivery-Id that is stable across retries.
--- [api_webhook_signature] Webhook Signature Verification and 403 Errors
Every webhook carries an X-TechStore-Signature header containing an HMAC-SHA256 of the raw request body, keyed with the webhook secret, hex encoded. A 403 returned by our delivery checker almost always means the signature was computed over a parsed and re-serialised body rather than the raw bytes; JSON re-serialisation changes key order and whitespace and therefore changes the HMAC. Compute the HMAC over the exact raw body before any JSON parsing. The second most common cause is using the API token instead of the webhook secret as the HMAC key.

========== c04+c05+c06 turn 9 ==========
CUSTOMER: How do I verify the webhook signature?

EARLIER CUSTOMER MESSAGES: How do I reset my password? | The reset email never came | I tried logging in 3 times and now it says locked | How long until I can try again? | I'm getting a 401 from the orders endpoint | I'm using my sandbox key against production | Where do I get the live key? | Do webhooks use the same key?

--- version `classic`
1. Read the **exact raw request body bytes**, before parsing JSON.
2. Compute an **HMAC-SHA256** over those bytes, using your **webhook secret** as the key—not your API token.
3. Hex-encode the result and compare it with the `X-TechStore-Signature` header.

Don’t compute the signature over parsed and re-serialised JSON: changes to whitespace or key order change the HMAC and are the most common cause of **403** errors from the delivery checker.
   evidence docs: ['api_webhook_signature', 'api_webhook_events', 'api_webhook_retries', 'api_idempotency']  orders: []

--- version `cache`
1. Capture the **exact raw request body before any JSON parsing**. Don’t parse and re-serialise it—changes to whitespace or key order change the signature.
2. Compute an **HMAC-SHA256** over those raw bytes, using your **webhook secret** as the key—not your API token.
3. Hex-encode the result and compare it with the `X-TechStore-Signature` header.

If the delivery checker returns 403, first check that you used the raw body and the correct webhook secret.
   evidence docs: ['api_webhook_signature', 'api_webhook_events', 'api_webhook_retries', 'api_idempotency']  orders: []

EVIDENCE:
--- [api_idempotency] API Idempotency
All POST endpoints accept an Idempotency-Key header. A repeated request with the same key and an identical payload returns the original response without creating a second resource. A repeated key with a different payload returns 409. Keys are retained for 24 hours. Clients should generate a UUID per logical operation, not per HTTP attempt, so that retries reuse the same key.
--- [api_webhook_events] Webhook Event Types
Available events: order.created, order.shipped, order.delivered, order.cancelled, order.returned, refund.initiated, refund.completed, inventory.low. Events are subscribed per endpoint in the dashboard. Payloads include the event type, a timestamp, and the affected resource. Event ordering is not guaranteed; use the timestamp rather than arrival order.
--- [api_webhook_retries] Webhook Delivery and Retries
Webhooks expect a 2xx response within 5 seconds. Non-2xx or timeout triggers retries at 1, 5, 25 and 125 minutes, then the endpoint is marked unhealthy and deliveries pause until reactivated in the dashboard. Handlers must be idempotent, because a duplicate delivery is possible even after a successful response. Each delivery carries an X-TechStore-Delivery-Id that is stable across retries.
--- [api_webhook_signature] Webhook Signature Verification and 403 Errors
Every webhook carries an X-TechStore-Signature header containing an HMAC-SHA256 of the raw request body, keyed with the webhook secret, hex encoded. A 403 returned by our delivery checker almost always means the signature was computed over a parsed and re-serialised body rather than the raw bytes; JSON re-serialisation changes key order and whitespace and therefore changes the HMAC. Compute the HMAC over the exact raw body before any JSON parsing. The second most common cause is using the API token instead of the webhook secret as the HMAC key.

========== c04+c05+c06 turn 10 ==========
CUSTOMER: Do you sell washing machines?

EARLIER CUSTOMER MESSAGES: How do I reset my password? | The reset email never came | I tried logging in 3 times and now it says locked | How long until I can try again? | I'm getting a 401 from the orders endpoint | I'm using my sandbox key against production | Where do I get the live key? | Do webhooks use the same key? | How do I verify the webhook signature?

--- version `classic`
I don't have that information. I can connect you with a human agent who can help.
   evidence docs: ['api_webhook_signature', 'api_webhook_events', 'api_webhook_retries', 'api_overview']  orders: []

--- version `cache`
I don't have that information. I can connect you with a human agent who can help.
   evidence docs: ['api_webhook_signature', 'api_webhook_events', 'api_webhook_retries', 'api_overview']  orders: []

EVIDENCE:
--- [api_overview] TechStore Partner API Overview
The Partner API is a REST API at https://api.techstore.example/v1. All requests require an Authorization header with a bearer token issued in the partner dashboard. Requests and responses are JSON. The API exposes orders, inventory, shipments and webhooks. Sandbox is available at https://sandbox.techstore.example/v1 with separate credentials and synthetic data.
--- [api_webhook_events] Webhook Event Types
Available events: order.created, order.shipped, order.delivered, order.cancelled, order.returned, refund.initiated, refund.completed, inventory.low. Events are subscribed per endpoint in the dashboard. Payloads include the event type, a timestamp, and the affected resource. Event ordering is not guaranteed; use the timestamp rather than arrival order.
--- [api_webhook_retries] Webhook Delivery and Retries
Webhooks expect a 2xx response within 5 seconds. Non-2xx or timeout triggers retries at 1, 5, 25 and 125 minutes, then the endpoint is marked unhealthy and deliveries pause until reactivated in the dashboard. Handlers must be idempotent, because a duplicate delivery is possible even after a successful response. Each delivery carries an X-TechStore-Delivery-Id that is stable across retries.
--- [api_webhook_signature] Webhook Signature Verification and 403 Errors
Every webhook carries an X-TechStore-Signature header containing an HMAC-SHA256 of the raw request body, keyed with the webhook secret, hex encoded. A 403 returned by our delivery checker almost always means the signature was computed over a parsed and re-serialised body rather than the raw bytes; JSON re-serialisation changes key order and whitespace and therefore changes the HMAC. Compute the HMAC over the exact raw body before any JSON parsing. The second most common cause is using the API token instead of the webhook secret as the HMAC key.

========== c04+c05+c06 turn 11 ==========
CUSTOMER: Okay, what laptops do you have then?

EARLIER CUSTOMER MESSAGES: How do I reset my password? | The reset email never came | I tried logging in 3 times and now it says locked | How long until I can try again? | I'm getting a 401 from the orders endpoint | I'm using my sandbox key against production | Where do I get the live key? | Do webhooks use the same key? | How do I verify the webhook signature? | Do you sell washing machines?

--- version `classic`
We have three laptops:

| Laptop | Price | Key specs |
|---|---:|---|
| **PulseBook Air 13** | ₹44,999 | 13.3-inch IPS display, Intel Core Ultra 3, 8 GB RAM, 256 GB SSD, 1.12 kg |
| **PulseBook 14** | ₹64,999 | 14-inch 2.8K OLED at 90 Hz, Intel Core Ultra 5, 16 GB RAM, 512 GB SSD, 1.29 kg |
| **PulseBook Pro 16** | ₹1,34,999 | 16-inch 3.2K OLED at 120 Hz, Intel Core Ultra 9, 32 GB RAM, 1 TB SSD, RTX 4060 graphics |

All three include a **“2-year manufacturer warranty”**. The PulseBook 14 and Pro 16 also include **“one year of accidental damage protection”**; the Air 13 does not.

What’s your budget, and what will you mainly use it for?
   evidence docs: ['about_techstore', 'prod_pulsebook_pro16', 'prod_pulsebook14', 'prod_pulsebook_air13', 'catalogue_summary']  orders: []

--- version `cache`
We have three laptops:

| Laptop | Price | Key specifications |
|---|---:|---|
| **PulseBook Air 13** | ₹44,999 | 13.3-inch IPS, Core Ultra 3, 8 GB RAM, 256 GB SSD, 1.12 kg |
| **PulseBook 14** | ₹64,999 | 14-inch 2.8K OLED at 90 Hz, Core Ultra 5, 16 GB RAM, 512 GB SSD, 1.29 kg |
| **PulseBook Pro 16** | ₹1,34,999 | 16-inch 3.2K OLED at 120 Hz, Core Ultra 9, 32 GB RAM, 1 TB SSD, RTX 4060, 1.95 kg |

All include a “2-year manufacturer warranty.” The PulseBook 14 and Pro 16 also include “one year of accidental damage protection”; the Air 13 does not.

What’s your budget, and what will you mainly use it for?
   evidence docs: ['about_techstore', 'prod_pulsebook_pro16', 'prod_pulsebook14', 'prod_pulsebook_air13', 'catalogue_summary']  orders: []

EVIDENCE:
--- [about_techstore] About TechStore
TechStore is an online-only consumer electronics retailer in India. It has no physical retail stores or showrooms, so there are no store opening hours; orders are placed only on the TechStore website and app. TechStore sells six product families: headphones and earbuds (SoundWave), laptops (PulseBook), tablets (NovaTab), smartwatches (AuraWatch), monitors (ClearView), and chargers and power banks (VoltCharge, VoltBank). TechStore does not sell mobile phones, televisions, cameras, gaming consoles, or home appliances such as washing machines, refrigerators, or air conditioners. Repairs are handled at authorised service centres in 48 cities. Customer support is available by chat and email from 9 AM to 9 PM IST, seven days a week.
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
--- [prod_pulsebook14] PulseBook 14 Laptop
14-inch ultrabook. Price ₹64,999. Intel Core Ultra 5, 16 GB LPDDR5 RAM, 512 GB NVMe SSD, 14-inch 2.8K OLED display at 90 Hz, 65 W USB-C charging, 1.29 kg, 12-hour rated battery. Ports: two USB-C Thunderbolt, one USB-A, HDMI 2.1, headphone jack. 2-year manufacturer warranty including one year of accidental damage protection.
--- [prod_pulsebook_air13] PulseBook Air 13 Laptop
13-inch entry ultrabook. Price ₹44,999. Intel Core Ultra 3, 8 GB LPDDR5 RAM, 256 GB NVMe SSD, 13.3-inch 1920x1200 IPS display at 60 Hz, 45 W USB-C charging, 1.12 kg, 10-hour rated battery. Ports: two USB-C, one USB-A, headphone jack. No HDMI port. 2-year manufacturer warranty. Accidental damage protection is not included on the Air 13; it is included only on the PulseBook 14 and Pro 16.
--- [prod_pulsebook_pro16] PulseBook Pro 16 Laptop
16-inch creator laptop. Price ₹1,34,999. Intel Core Ultra 9, 32 GB RAM, 1 TB NVMe SSD, discrete RTX 4060 graphics, 16-inch 3.2K OLED at 120 Hz, 100 W USB-C charging, 1.95 kg. 2-year manufacturer warranty including one year of accidental damage protection.

========== c04+c05+c06 turn 12 ==========
CUSTOMER: Which is the lightest one?

EARLIER CUSTOMER MESSAGES: How do I reset my password? | The reset email never came | I tried logging in 3 times and now it says locked | How long until I can try again? | I'm getting a 401 from the orders endpoint | I'm using my sandbox key against production | Where do I get the live key? | Do webhooks use the same key? | How do I verify the webhook signature? | Do you sell washing machines? | Okay, what laptops do you have then?

--- version `classic`
The **PulseBook Air 13** is the lightest at **1.12 kg**, priced at **₹44,999**. It has a 13.3-inch display, Intel Core Ultra 3, 8 GB RAM, and a 256 GB SSD.
   evidence docs: ['prod_pulsebook14', 'prod_pulsebook_pro16', 'prod_pulsebook_air13', 'prod_clearview32', 'catalogue_summary']  orders: []

--- version `cache`
The **PulseBook Air 13** is our lightest laptop at **1.12 kg**, priced at **₹44,999**. It has a 13.3-inch display, Intel Core Ultra 3, 8 GB RAM and a 256 GB SSD.
   evidence docs: ['prod_pulsebook14', 'prod_pulsebook_pro16', 'prod_pulsebook_air13', 'prod_clearview32', 'catalogue_summary']  orders: []

EVIDENCE:
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
--- [prod_clearview32] ClearView 32 Ultra Monitor
32-inch monitor. Price ₹39,999. 4K UHD IPS Black panel, 165 Hz refresh, 1 ms response, 99 percent DCI-P3, HDR600, USB-C with 140 W power delivery, built-in KVM switch, height and pivot adjustable stand, VESA 100. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.
--- [prod_pulsebook14] PulseBook 14 Laptop
14-inch ultrabook. Price ₹64,999. Intel Core Ultra 5, 16 GB LPDDR5 RAM, 512 GB NVMe SSD, 14-inch 2.8K OLED display at 90 Hz, 65 W USB-C charging, 1.29 kg, 12-hour rated battery. Ports: two USB-C Thunderbolt, one USB-A, HDMI 2.1, headphone jack. 2-year manufacturer warranty including one year of accidental damage protection.
--- [prod_pulsebook_air13] PulseBook Air 13 Laptop
13-inch entry ultrabook. Price ₹44,999. Intel Core Ultra 3, 8 GB LPDDR5 RAM, 256 GB NVMe SSD, 13.3-inch 1920x1200 IPS display at 60 Hz, 45 W USB-C charging, 1.12 kg, 10-hour rated battery. Ports: two USB-C, one USB-A, headphone jack. No HDMI port. 2-year manufacturer warranty. Accidental damage protection is not included on the Air 13; it is included only on the PulseBook 14 and Pro 16.
--- [prod_pulsebook_pro16] PulseBook Pro 16 Laptop
16-inch creator laptop. Price ₹1,34,999. Intel Core Ultra 9, 32 GB RAM, 1 TB NVMe SSD, discrete RTX 4060 graphics, 16-inch 3.2K OLED at 120 Hz, 100 W USB-C charging, 1.95 kg. 2-year manufacturer warranty including one year of accidental damage protection.

========== c04+c05+c06 turn 13 ==========
CUSTOMER: Can I pay for it in EMI?

EARLIER CUSTOMER MESSAGES: How do I reset my password? | The reset email never came | I tried logging in 3 times and now it says locked | How long until I can try again? | I'm getting a 401 from the orders endpoint | I'm using my sandbox key against production | Where do I get the live key? | Do webhooks use the same key? | How do I verify the webhook signature? | Do you sell washing machines? | Okay, what laptops do you have then? | Which is the lightest one?

--- version `classic`
Yes—EMI is available for orders “above ₹5,000” on credit cards from “12 partner banks,” over “3, 6, 9 or 12 months.” “No-cost EMI” is offered only on selected products.

I don't have information about the PulseBook Air 13’s price or EMI eligibility in the provided catalogue; my earlier laptop details were unsupported.
   evidence docs: ['bill_emi', 'prod_clearview32', 'prod_aurawatch3', 'prod_aurawatch_pro']  orders: []

--- version `cache`
Yes—the PulseBook Air 13 at ₹44,999 meets the EMI requirement of “orders above ₹5,000.” EMI is available on credit cards from “12 partner banks,” over “3, 6, 9 or 12 months.”

I don't have information about which banks participate or whether the PulseBook Air 13 qualifies for no-cost EMI.
   evidence docs: ['bill_emi', 'prod_clearview32', 'prod_aurawatch3', 'prod_aurawatch_pro']  orders: []

EVIDENCE:
--- [bill_emi] EMI and No-Cost EMI
EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount. If an order paid by no-cost EMI is returned, the discount is deducted from the refund and the bank may still charge interest already levied; the bank must be contacted to cancel the EMI plan.
--- [prod_aurawatch3] AuraWatch 3 Smartwatch
Fitness smartwatch. Price ₹8,999. 1.4-inch AMOLED display, 14-day battery, heart-rate and SpO2 sensors, built-in GPS, 5 ATM water resistance, sleep tracking. Compatible with Android 9 and above and iOS 14 and above. 1-year manufacturer warranty. Worn on the wrist, therefore non-returnable once used, under the hygiene policy.
--- [prod_aurawatch_pro] AuraWatch Pro Smartwatch
Premium fitness smartwatch. Price ₹15,999. 1.5-inch AMOLED always-on display, 18-day battery, ECG and SpO2 sensors, dual-band GPS, 10 ATM water resistance, offline maps, 100 sport modes. Compatible with Android 10 and above and iOS 15 and above. 2-year manufacturer warranty. Non-returnable once used, under the hygiene policy.
--- [prod_clearview32] ClearView 32 Ultra Monitor
32-inch monitor. Price ₹39,999. 4K UHD IPS Black panel, 165 Hz refresh, 1 ms response, 99 percent DCI-P3, HDR600, USB-C with 140 W power delivery, built-in KVM switch, height and pivot adjustable stand, VESA 100. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.
