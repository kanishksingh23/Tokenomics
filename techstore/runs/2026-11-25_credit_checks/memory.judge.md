# Conversation-memory answers to grade

Store date: 30 September 2026. For each turn, four versions of the agent answered the SAME customer message.
They differ only in how much of the earlier conversation they were shown (`off` = everything).
Grade each version against the conversation so far and the evidence it was given.

========== c01 turn 4 ==========
CONVERSATION SO FAR (as it really happened, `off` version):
  CUSTOMER: Hi, what's happening with order 48712?
  AGENT: Your order #48712 for the SoundWave X200 Wireless Headphones (₹12,999) is **Processing**, with an estimated delivery date of **1 October 2026**. As of today, 30 September, it isn’t overdue.

No courier or tracking number has been assigned yet. Once it’s marked Shipped, you’ll receive a tracking link by email and SMS; you can also find it under Orders in your account.
  CUSTOMER: Why do I see three charges on my card for it?
  AGENT: I’m sorry for the confusion. Only **one order was created**—order #48712. The other two entries were temporary authorisation holds caused by a duplicate payment-page submission.

Here’s every charge:
- **27 September 2026 — ₹12,999:** Settled payment for order #48712.
- **27 September 2026 — ₹12,999:** Duplicate hold, already reversed on **29 September 2026**.
- **27 September 2026 — ₹12,999:** Duplicate hold, pending reversal **by 4 October 2026**.

Resolution:
1. Keep the settled payment—it covers your order.
2. Check your card statement for the hold released on 29 September.
3. Allow the remaining hold to reverse automatically by 4 October. The stated reversal period is **“5 to 7 business days.”**
4. If either reversal is still missing after its expected date, I can connect you with a human agent to investigate.
  CUSTOMER: When will the extra money come back?
  AGENT: Of the three entries on your card:

- **27 September — ₹12,999:** Settled payment for order #48712; this stays charged.
- **27 September — ₹12,999:** Extra hold already reversed on **29 September 2026**.
- **27 September — ₹12,999:** Remaining extra hold is due to reverse **by 4 October 2026**.

Next steps:
1. Check your card statement for the reversal dated 29 September.
2. Allow until 4 October for the remaining hold to reverse automatically. The policy timeframe is **“5 to 7 business days.”**
3. If the first reversal isn’t showing, or the remaining hold hasn’t reversed by 4 October, I can connect you with a human agent to investigate.

THIS TURN, CUSTOMER: Can I still cancel the order?

--- version `off` (earlier turns trimmed: 0)
Yes. Order #48712 is still **Processing**, so it can be **“cancelled free of charge at any time before it is marked Shipped.”**

If cancelled, the settled payment of **₹12,999** will be refunded to your original credit card within **“5 to 7 business days.”** The remaining duplicate hold of **₹12,999** is separate and is due to reverse by **4 October 2026**.

I can connect you with a human agent to arrange the cancellation.
   evidence docs: ['pol_cancellation', 'bill_failed_payment', 'bill_cod_refund', 'bill_refund_to_closed_card']  orders: ['48712']

--- version `window` (earlier turns trimmed: 1)
Yes—order #48712 is still **Processing**, so it can be cancelled **“free of charge at any time before it is marked Shipped.”**

If cancelled, the settled **₹12,999** payment will be refunded to your original credit card **“within 5 to 7 business days.”** The remaining duplicate hold is separately scheduled to reverse by **4 October 2026**.

I can connect you with a human agent to request the cancellation.
   evidence docs: ['pol_cancellation', 'bill_failed_payment', 'bill_cod_refund', 'bill_refund_to_closed_card']  orders: ['48712']

--- version `facts` (earlier turns trimmed: 1)
Yes—order #48712 is still **Processing**, so it can be **“cancelled free of charge at any time before it is marked Shipped.”**

If cancelled, your settled payment of **₹12,999** will be refunded in full to your original credit card within **“5 to 7 business days.”** The remaining duplicate hold will reverse separately and is expected to release by **4 October 2026**.

I can connect you with a human agent to arrange the cancellation.
   evidence docs: ['pol_cancellation', 'bill_failed_payment', 'bill_cod_refund', 'bill_refund_to_closed_card']  orders: ['48712']

--- version `summary` (earlier turns trimmed: 1)
Yes—order #48712 is still **Processing**, so you can cancel it **“free of charge at any time before it is marked Shipped.”**

The settled payment of **₹12,999** would be refunded to your original credit card **“within 5 to 7 business days.”** The remaining duplicate hold is separate and is scheduled to reverse by **4 October 2026**.

I can connect you with a human agent to request the cancellation.
   evidence docs: ['pol_cancellation', 'bill_failed_payment', 'bill_cod_refund', 'bill_refund_to_closed_card']  orders: ['48712']

EVIDENCE (union of what the versions saw):
--- [bill_cod_refund] Refunds on Cash-on-Delivery Orders
Cash-on-delivery orders cannot be refunded to a payment method because none was used. Refunds are made by bank transfer after the customer submits account number and IFSC through the secure link sent by support. Transfers complete within 5 to 7 business days of verification. The ₹49 COD handling fee is refunded only if the order is cancelled before dispatch.
--- [bill_failed_payment] Payment Failed but Money Debited
If a payment fails but the amount is debited, the bank has placed a temporary hold that is released automatically. Card and UPI holds reverse within 5 to 7 business days; net banking can take up to 10. No order is created for a failed payment, so there is nothing to cancel. If the amount has not reversed after the stated period, contact support with the bank reference number and TechStore raises a chargeback trace with the payment gateway.
--- [bill_refund_to_closed_card] Refund to a Closed or Expired Card
Refunds are issued to the original payment method. If that card is closed or expired, the issuing bank still routes the credit to the underlying account in most cases. If the bank rejects the credit, the funds return to TechStore within 10 business days, after which support can arrange a bank transfer once account details and identity are verified. We cannot refund to a different card at the customer's request when the original card is still active.
--- [pol_cancellation] Order Cancellation
An order can be cancelled free of charge at any time before it is marked Shipped. Once shipped, cancellation is not possible; the customer should refuse delivery or raise a return after delivery. Cancelled orders are refunded in full, including any delivery charge paid, within 5 to 7 business days.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c01 turn 5 ==========
CONVERSATION SO FAR (as it really happened, `off` version):
  CUSTOMER: Hi, what's happening with order 48712?
  AGENT: Your order #48712 for the SoundWave X200 Wireless Headphones (₹12,999) is **Processing**, with an estimated delivery date of **1 October 2026**. As of today, 30 September, it isn’t overdue.

No courier or tracking number has been assigned yet. Once it’s marked Shipped, you’ll receive a tracking link by email and SMS; you can also find it under Orders in your account.
  CUSTOMER: Why do I see three charges on my card for it?
  AGENT: I’m sorry for the confusion. Only **one order was created**—order #48712. The other two entries were temporary authorisation holds caused by a duplicate payment-page submission.

Here’s every charge:
- **27 September 2026 — ₹12,999:** Settled payment for order #48712.
- **27 September 2026 — ₹12,999:** Duplicate hold, already reversed on **29 September 2026**.
- **27 September 2026 — ₹12,999:** Duplicate hold, pending reversal **by 4 October 2026**.

Resolution:
1. Keep the settled payment—it covers your order.
2. Check your card statement for the hold released on 29 September.
3. Allow the remaining hold to reverse automatically by 4 October. The stated reversal period is **“5 to 7 business days.”**
4. If either reversal is still missing after its expected date, I can connect you with a human agent to investigate.
  CUSTOMER: When will the extra money come back?
  AGENT: Of the three entries on your card:

- **27 September — ₹12,999:** Settled payment for order #48712; this stays charged.
- **27 September — ₹12,999:** Extra hold already reversed on **29 September 2026**.
- **27 September — ₹12,999:** Remaining extra hold is due to reverse **by 4 October 2026**.

Next steps:
1. Check your card statement for the reversal dated 29 September.
2. Allow until 4 October for the remaining hold to reverse automatically. The policy timeframe is **“5 to 7 business days.”**
3. If the first reversal isn’t showing, or the remaining hold hasn’t reversed by 4 October, I can connect you with a human agent to investigate.
  CUSTOMER: Can I still cancel the order?
  AGENT: Yes. Order #48712 is still **Processing**, so it can be **“cancelled free of charge at any time before it is marked Shipped.”**

If cancelled, the settled payment of **₹12,999** will be refunded to your original credit card within **“5 to 7 business days.”** The remaining duplicate hold of **₹12,999** is separate and is due to reverse by **4 October 2026**.

I can connect you with a human agent to arrange the cancellation.

THIS TURN, CUSTOMER: If I cancel, how long until I get the refund?

--- version `off` (earlier turns trimmed: 0)
If you cancel order #48712 while it’s still Processing, your full payment will be refunded to your original credit card within **“5 to 7 business days”** of cancellation.

Here’s how each card entry is handled:
- **₹12,999 settled payment:** Refunded after cancellation.
- **₹12,999 duplicate hold:** Already reversed on **29 September 2026**.
- **₹12,999 duplicate hold:** Scheduled to reverse by **4 October 2026**, separately from the cancellation refund.

Next steps:
1. I can connect you with a human agent to arrange cancellation before the order is marked Shipped.
2. Once cancelled, allow **5 to 7 business days** for the refund.

To clarify my earlier message: that refund timeframe applies to cancellation refunds, not duplicate holds; your remaining hold has its own reversal date above.
   evidence docs: ['pol_cancellation', 'bill_refund_to_closed_card', 'bill_cod_refund', 'bill_chargeback']  orders: ['48712']

--- version `window` (earlier turns trimmed: 2)
If you cancel order #48712 before it is marked Shipped, your **₹12,999** payment will be refunded in full to your original credit card **“within 5 to 7 business days.”**

The duplicate **₹12,999** hold is separate and is scheduled to reverse by **4 October 2026**.
   evidence docs: ['pol_cancellation', 'bill_refund_to_closed_card', 'bill_cod_refund', 'bill_chargeback']  orders: ['48712']

--- version `facts` (earlier turns trimmed: 2)
If you cancel order #48712 before it’s marked Shipped, your **₹12,999** payment will be refunded in full to your original credit card within **“5 to 7 business days”** of cancellation.

The duplicate holds are separate: one was reversed on **29 September**, and the remaining **₹12,999** hold is due to reverse by **4 October 2026**—that date isn’t the cancellation refund deadline.
   evidence docs: ['pol_cancellation', 'bill_refund_to_closed_card', 'bill_cod_refund', 'bill_chargeback']  orders: ['48712']

--- version `summary` (earlier turns trimmed: 2)
If you cancel order #48712 before it is marked Shipped, your **₹12,999** payment will be refunded in full to your original credit card **“within 5 to 7 business days”** of cancellation.

The separate duplicate hold of **₹12,999** is already scheduled to reverse by **4 October 2026**; cancellation isn’t needed for that release.
   evidence docs: ['pol_cancellation', 'bill_refund_to_closed_card', 'bill_cod_refund', 'bill_chargeback']  orders: ['48712']

EVIDENCE (union of what the versions saw):
--- [bill_chargeback] Bank Chargebacks and Disputes
If a customer raises a chargeback with their bank, the order is frozen and any parallel TechStore refund is suspended to prevent a double credit. Chargebacks take 45 to 90 days to resolve through the card network. Contacting support directly is almost always faster than a chargeback, and support can withdraw a chargeback by providing the bank with resolution evidence.
--- [bill_cod_refund] Refunds on Cash-on-Delivery Orders
Cash-on-delivery orders cannot be refunded to a payment method because none was used. Refunds are made by bank transfer after the customer submits account number and IFSC through the secure link sent by support. Transfers complete within 5 to 7 business days of verification. The ₹49 COD handling fee is refunded only if the order is cancelled before dispatch.
--- [bill_refund_to_closed_card] Refund to a Closed or Expired Card
Refunds are issued to the original payment method. If that card is closed or expired, the issuing bank still routes the credit to the underlying account in most cases. If the bank rejects the credit, the funds return to TechStore within 10 business days, after which support can arrange a bank transfer once account details and identity are verified. We cannot refund to a different card at the customer's request when the original card is still active.
--- [pol_cancellation] Order Cancellation
An order can be cancelled free of charge at any time before it is marked Shipped. Once shipped, cancellation is not possible; the customer should refuse delivery or raise a return after delivery. Cancelled orders are refunded in full, including any delivery charge paid, within 5 to 7 business days.
--- order 48712: {"order_id": "48712", "customer_id": "cust_7788", "email": "meera.p@example.com", "placed_at": "2026-09-27", "status": "Processing", "items": [{"sku": "prod_x200", "name": "SoundWave X200 Wireless Headphones", "qty": 1, "unit_price": 12999}], "total": 12999, "payment_method": "Credit Card", "delivery_pin": "380015", "courier": null, "tracking_id": null, "eta": "2026-10-01", "charges": [{"date": "2026-09-27", "amount": 12999, "type": "capture", "status": "settled"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "reversed", "note": "duplicate submission, hold released automatically", "reversed_at": "2026-09-29"}, {"date": "2026-09-27", "amount": 12999, "type": "authorization", "status": "pending_reversal", "note": "duplicate submission, reverses by 2026-10-04"}]}

========== c02 turn 4 ==========
CONVERSATION SO FAR (as it really happened, `off` version):
  CUSTOMER: Is the X200 good for the gym?
  AGENT: The SoundWave X200 has some useful gym features: wireless connectivity, a 250 g weight, and “hybrid active noise cancellation rated at 35 dB.”

I don't have information about its sweat or water resistance or how securely it stays on during exercise, so I can’t confidently recommend it for gym use.
  CUSTOMER: What about the Y500?
  AGENT: The SoundWave Y500 has wireless connectivity, 60-hour battery life, and memory-foam earcups, and weighs 268 g. It’s recommended for noisy environments such as offices and flights—not specifically for workouts.

I don't have information about its sweat or water resistance or how securely it stays on during exercise, so I can’t confidently recommend it for gym use.
  CUSTOMER: Which one has the longer battery?
  AGENT: The **Y500** has the longer battery life: **60 hours**, compared with **40 hours** for the X200—20 hours more.

THIS TURN, CUSTOMER: Can I return it if I open the box and don't like it?

--- version `off` (earlier turns trimmed: 0)
I don't have that information. I can connect you with a human agent who can help.
   evidence docs: ['prod_voltbank20k', 'pol_damaged_in_transit', 'pol_exchange', 'prod_voltcharge65']  orders: []

--- version `window` (earlier turns trimmed: 1)
I don't have that information. I can connect you with a human agent who can help. My earlier statement about an opened-box hygiene policy wasn’t supported by the available TechStore documents.
   evidence docs: ['prod_voltbank20k', 'pol_damaged_in_transit', 'pol_exchange', 'prod_voltcharge65']  orders: []

--- version `facts` (earlier turns trimmed: 1)
I don't have that information. I can connect you with a human agent who can help.
   evidence docs: ['prod_voltbank20k', 'pol_damaged_in_transit', 'pol_exchange', 'prod_voltcharge65']  orders: []

--- version `summary` (earlier turns trimmed: 1)
I don't have that information. I can connect you with a human agent who can help. They can confirm whether opening the box and simply not liking the headphones qualifies for a return.
   evidence docs: ['prod_voltbank20k', 'pol_damaged_in_transit', 'pol_exchange', 'prod_voltcharge65']  orders: []

EVIDENCE (union of what the versions saw):
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [pol_exchange] Exchange Policy
An exchange can be requested within 30 days of delivery for a different size, colour or variant of the same product line, subject to stock. If the new variant costs more, the difference is charged before dispatch. If it costs less, the difference is refunded. Only one exchange is permitted per order line.
--- [prod_voltbank20k] VoltBank 20000mAh Power Bank
20000 mAh power bank. Price ₹2,999. 65 W USB-C output, 20 W USB-A output, pass-through charging, LED capacity display, 389 g. Its capacity is under 100 Wh; check your airline's rules before carrying it on a flight. Can charge the PulseBook Air 13 once or the NovaTab 11 twice. 1-year manufacturer warranty.
--- [prod_voltcharge65] VoltCharge 65W GaN Charger
65 W GaN fast charger. Price ₹2,499. Two USB-C ports and one USB-A, supports Power Delivery 3.1 and Quick Charge 5, foldable pins. Compatible with PulseBook 14, NovaTab 11 and all SoundWave headphones. Not sufficient to charge the PulseBook Pro 16 at full speed, which requires 100 W. 1-year manufacturer warranty.

========== c03 turn 4 ==========
CONVERSATION SO FAR (as it really happened, `off` version):
  CUSTOMER: I want to return my PulseBook 14, it was delivered 20 days ago
  AGENT: I don't have that information. I can connect you with a human agent who can help. They can confirm return eligibility for your PulseBook 14, delivered 20 days ago.
  CUSTOMER: Do I need the original box?
  AGENT: I don't have that information. I can connect you with a human agent who can help. They can confirm whether the original box is required for your PulseBook 14 return.
  CUSTOMER: How long will the refund take?
  AGENT: Once your return is received and inspected at our warehouse, your refund is “initiated within 2 business days.” It then reaches your original payment method in:

- **Cards or UPI:** “5 to 7 business days”
- **Net banking:** “up to 10 business days”

Also, to correct my earlier replies: delivery 20 days ago is within the return period of “30 days of delivery.” The original box is required: items must be returned in their “original packaging with all accessories, manuals and free gifts included.”

THIS TURN, CUSTOMER: And if I paid with net banking?

--- version `off` (earlier turns trimmed: 0)
For net banking, your refund is “initiated within 2 business days” after the return is received and inspected at our warehouse. The money then reaches your original payment method in “up to 10 business days.”

I also need to correct my earlier message: I don't have information about return eligibility or original-box requirements for your PulseBook 14.
   evidence docs: ['pol_refund_timeline', 'bill_chargeback', 'bill_refund_to_closed_card', 'bill_cod_refund']  orders: []

--- version `window` (earlier turns trimmed: 1)
For net banking, your refund is initiated “within 2 business days” after the returned item is received and inspected, then reaches your original account in “up to 10 business days.”

Correction: my earlier claims about a return window and original packaging weren’t supported by the available policies. I don't have information about return eligibility or whether the original box is required.
   evidence docs: ['pol_refund_timeline', 'bill_chargeback', 'bill_refund_to_closed_card', 'bill_cod_refund']  orders: []

--- version `facts` (earlier turns trimmed: 1)
For net banking, your refund is initiated **“within 2 business days”** after the returned item is received and inspected at our warehouse. The money then takes **“up to 10 business days”** to reach your original payment method.

I also need to correct my previous message: I don't have information about your return eligibility or whether the original box is required.
   evidence docs: ['pol_refund_timeline', 'bill_chargeback', 'bill_refund_to_closed_card', 'bill_cod_refund']  orders: []

--- version `summary` (earlier turns trimmed: 1)
For net banking, once your return is received and inspected, your refund is “initiated within 2 business days.” It then takes “up to 10 business days” to reach your original bank account.

I also need to correct my previous message: I don't have information about your return eligibility or whether the original box is required.
   evidence docs: ['pol_refund_timeline', 'bill_chargeback', 'bill_refund_to_closed_card', 'bill_cod_refund']  orders: []

EVIDENCE (union of what the versions saw):
--- [bill_chargeback] Bank Chargebacks and Disputes
If a customer raises a chargeback with their bank, the order is frozen and any parallel TechStore refund is suspended to prevent a double credit. Chargebacks take 45 to 90 days to resolve through the card network. Contacting support directly is almost always faster than a chargeback, and support can withdraw a chargeback by providing the bank with resolution evidence.
--- [bill_cod_refund] Refunds on Cash-on-Delivery Orders
Cash-on-delivery orders cannot be refunded to a payment method because none was used. Refunds are made by bank transfer after the customer submits account number and IFSC through the secure link sent by support. Transfers complete within 5 to 7 business days of verification. The ₹49 COD handling fee is refunded only if the order is cancelled before dispatch.
--- [bill_refund_to_closed_card] Refund to a Closed or Expired Card
Refunds are issued to the original payment method. If that card is closed or expired, the issuing bank still routes the credit to the underlying account in most cases. If the bank rejects the credit, the funds return to TechStore within 10 business days, after which support can arrange a bank transfer once account details and identity are verified. We cannot refund to a different card at the customer's request when the original card is still active.
--- [pol_refund_timeline] Refund Processing Time
Once a returned item is received and inspected at our warehouse, refunds are initiated within 2 business days. The money reaches the original payment method in 5 to 7 business days for cards and UPI, and up to 10 business days for net banking. Refunds are always issued to the original payment method; we cannot redirect a refund to a different card or account.

========== c04 turn 4 ==========
CONVERSATION SO FAR (as it really happened, `off` version):
  CUSTOMER: How do I reset my password?
  AGENT: 1. Select **Forgot Password** on the TechStore sign-in page.
2. Follow the reset link emailed to you. The link is “valid for 30 minutes.”
3. If the email doesn’t arrive, check your spam folder and confirm you entered the email address registered to your account.
  CUSTOMER: The reset email never came
  AGENT: Sorry the reset email hasn’t arrived.

1. Check your spam folder.
2. Confirm the email address you entered matches the one registered to your account. For privacy, we don’t disclose whether an address is registered.
3. Use **Forgot Password** again. The reset link is “valid for 30 minutes.”

If it still doesn’t arrive, I can connect you with a human agent for further help.
  CUSTOMER: I tried logging in 3 times and now it says locked
  AGENT: After three failed sign-in attempts, your account is “locked for 15 minutes.”

1. Wait 15 minutes before trying to sign in again.
2. If you don’t remember your password, use **Forgot Password** on the sign-in page. Check spam if the reset email doesn’t arrive.

THIS TURN, CUSTOMER: How long until I can try again?

--- version `off` (earlier turns trimmed: 0)
You can try again **15 minutes after the account was locked**. The lock lasts “15 minutes” after three failed sign-in attempts.
   evidence docs: ['acc_password', 'api_auth', 'api_timeouts', 'acc_two_factor']  orders: []

--- version `window` (earlier turns trimmed: 1)
The account is “locked for 15 minutes” after three failed sign-in attempts. You can try again once 15 minutes have passed since the lock began.
   evidence docs: ['acc_password', 'api_auth', 'api_timeouts', 'acc_two_factor']  orders: []

--- version `facts` (earlier turns trimmed: 1)
You can try again **15 minutes after the lock started**. Your account is “locked for 15 minutes” after three failed sign-in attempts.
   evidence docs: ['acc_password', 'api_auth', 'api_timeouts', 'acc_two_factor']  orders: []

--- version `summary` (earlier turns trimmed: 1)
You can try again **15 minutes after the account was locked**. The lock lasts “15 minutes” after three failed sign-in attempts.
   evidence docs: ['acc_password', 'api_auth', 'api_timeouts', 'acc_two_factor']  orders: []

EVIDENCE (union of what the versions saw):
--- [acc_password] Password Reset
Use Forgot Password on the sign-in page. A reset link valid for 30 minutes is emailed. If the email does not arrive, check spam and confirm the address matches the registered one; for privacy we do not disclose whether an address is registered. After three failed sign-in attempts the account is locked for 15 minutes.
--- [acc_two_factor] Two-Factor Authentication
Two-factor authentication can be enabled from Security in the account, using an authenticator app or SMS. Enabling 2FA signs out all other sessions. To disable 2FA, current authentication is required; if the device is lost, identity is verified with the last order details and a government ID, and removal takes up to 48 hours.
--- [api_auth] API Authentication and 401 Errors
Authenticate with Authorization: Bearer <token>. A 401 means the token is missing, malformed, expired or from the wrong environment; sandbox tokens rejected by production is the most common cause. Tokens expire 90 days after issue and can be rotated in the dashboard without downtime, since the previous token stays valid for 24 hours after rotation.
--- [api_timeouts] API Timeouts and Retry Safety
Requests time out server side at 30 seconds. A timeout does not indicate whether the operation completed, so POST requests must be retried with the same Idempotency-Key to avoid duplicates. GET, PUT and DELETE are idempotent by design and safe to retry. Retries should use exponential backoff with jitter; retrying immediately in a tight loop triggers rate limiting.

========== c05 turn 4 ==========
CONVERSATION SO FAR (as it really happened, `off` version):
  CUSTOMER: I'm getting a 401 from the orders endpoint
  AGENT: A 401 means your token is missing, malformed, expired, or from the wrong environment. The most common cause is using a sandbox token in production.

1. Check that your request includes `Authorization: Bearer <token>`.
2. Match the token to the environment:
   - Production: `https://api.techstore.example/v1`
   - Sandbox: `https://sandbox.techstore.example/v1` — requires separate credentials.
3. Check the token’s age: “Tokens expire 90 days after issue”.
4. If needed, rotate it in the partner dashboard. The previous token stays valid for 24 hours after rotation, allowing rotation without downtime.

Are you calling production or sandbox? Please don’t share your token.
  CUSTOMER: I'm using my sandbox key against production
  AGENT: That explains the 401: sandbox tokens are rejected by production.

1. For sandbox testing, use `https://sandbox.techstore.example/v1` with your sandbox token.
2. For production, use `https://api.techstore.example/v1` with a production bearer token issued in the partner dashboard.

Sandbox uses synthetic data, so use production credentials when accessing production orders.
  CUSTOMER: Where do I get the live key?
  AGENT: Get your production bearer token from the **TechStore partner dashboard**. Use it with the production API in this header:

```http
Authorization: Bearer <token>
```

I don't have information about the exact dashboard page or menu where production tokens are issued.

THIS TURN, CUSTOMER: Do webhooks use the same key?

--- version `off` (earlier turns trimmed: 0)
No. Webhooks use a **webhook secret**, not your API key. Sandbox webhooks also use a separate signing secret from production.

To verify a webhook:
1. Read the exact raw request body before parsing JSON.
2. Compute its HMAC-SHA256 using the webhook secret as the key, and hex-encode the result.
3. Compare it with the `X-TechStore-Signature` header.
   evidence docs: ['api_webhook_events', 'api_webhook_signature', 'api_webhook_retries', 'api_sandbox']  orders: []

--- version `window` (earlier turns trimmed: 1)
No. Webhooks use a **webhook signing secret**, not your API key. Sandbox webhooks use a separate signing secret from production.

To verify a webhook, compute an HMAC-SHA256 over the **exact raw request body** using the webhook secret, hex-encode it, and compare it with the `X-TechStore-Signature` header. Do this before parsing the JSON.
   evidence docs: ['api_webhook_events', 'api_webhook_signature', 'api_webhook_retries', 'api_sandbox']  orders: []

--- version `facts` (earlier turns trimmed: 1)
No—webhooks use a **webhook secret**, not your API key.

To verify a webhook, compute an HMAC-SHA256 over the **exact raw request body**, using the webhook secret as the key, and compare the hex-encoded result with the `X-TechStore-Signature` header. Do this before parsing JSON.

Sandbox webhooks use a **separate signing secret**.
   evidence docs: ['api_webhook_events', 'api_webhook_signature', 'api_webhook_retries', 'api_sandbox']  orders: []

--- version `summary` (earlier turns trimmed: 1)
No—webhooks use a **webhook secret**, not your API token, to sign requests.

Verify the `X-TechStore-Signature` header against an HMAC-SHA256 of the **exact raw request body**, keyed with the webhook secret and hex encoded. Do this before parsing JSON.

Sandbox webhooks also use a **separate signing secret** from production.
   evidence docs: ['api_webhook_events', 'api_webhook_signature', 'api_webhook_retries', 'api_sandbox']  orders: []

EVIDENCE (union of what the versions saw):
--- [api_sandbox] Sandbox Environment
Sandbox runs at https://sandbox.techstore.example/v1 with separate credentials and synthetic data that resets nightly at 02:00 IST. Sandbox order IDs begin with a 9; production IDs do not. Webhooks fire in sandbox but use a separate signing secret. Sandbox has no rate limit but is not performance representative.
--- [api_webhook_events] Webhook Event Types
Available events: order.created, order.shipped, order.delivered, order.cancelled, order.returned, refund.initiated, refund.completed, inventory.low. Events are subscribed per endpoint in the dashboard. Payloads include the event type, a timestamp, and the affected resource. Event ordering is not guaranteed; use the timestamp rather than arrival order.
--- [api_webhook_retries] Webhook Delivery and Retries
Webhooks expect a 2xx response within 5 seconds. Non-2xx or timeout triggers retries at 1, 5, 25 and 125 minutes, then the endpoint is marked unhealthy and deliveries pause until reactivated in the dashboard. Handlers must be idempotent, because a duplicate delivery is possible even after a successful response. Each delivery carries an X-TechStore-Delivery-Id that is stable across retries.
--- [api_webhook_signature] Webhook Signature Verification and 403 Errors
Every webhook carries an X-TechStore-Signature header containing an HMAC-SHA256 of the raw request body, keyed with the webhook secret, hex encoded. A 403 returned by our delivery checker almost always means the signature was computed over a parsed and re-serialised body rather than the raw bytes; JSON re-serialisation changes key order and whitespace and therefore changes the HMAC. Compute the HMAC over the exact raw body before any JSON parsing. The second most common cause is using the API token instead of the webhook secret as the HMAC key.

========== c05 turn 5 ==========
CONVERSATION SO FAR (as it really happened, `off` version):
  CUSTOMER: I'm getting a 401 from the orders endpoint
  AGENT: A 401 means your token is missing, malformed, expired, or from the wrong environment. The most common cause is using a sandbox token in production.

1. Check that your request includes `Authorization: Bearer <token>`.
2. Match the token to the environment:
   - Production: `https://api.techstore.example/v1`
   - Sandbox: `https://sandbox.techstore.example/v1` — requires separate credentials.
3. Check the token’s age: “Tokens expire 90 days after issue”.
4. If needed, rotate it in the partner dashboard. The previous token stays valid for 24 hours after rotation, allowing rotation without downtime.

Are you calling production or sandbox? Please don’t share your token.
  CUSTOMER: I'm using my sandbox key against production
  AGENT: That explains the 401: sandbox tokens are rejected by production.

1. For sandbox testing, use `https://sandbox.techstore.example/v1` with your sandbox token.
2. For production, use `https://api.techstore.example/v1` with a production bearer token issued in the partner dashboard.

Sandbox uses synthetic data, so use production credentials when accessing production orders.
  CUSTOMER: Where do I get the live key?
  AGENT: Get your production bearer token from the **TechStore partner dashboard**. Use it with the production API in this header:

```http
Authorization: Bearer <token>
```

I don't have information about the exact dashboard page or menu where production tokens are issued.
  CUSTOMER: Do webhooks use the same key?
  AGENT: No. Webhooks use a **webhook secret**, not your API key. Sandbox webhooks also use a separate signing secret from production.

To verify a webhook:
1. Read the exact raw request body before parsing JSON.
2. Compute its HMAC-SHA256 using the webhook secret as the key, and hex-encode the result.
3. Compare it with the `X-TechStore-Signature` header.

THIS TURN, CUSTOMER: How do I verify the webhook signature?

--- version `off` (earlier turns trimmed: 0)
1. Read the **exact raw request body before any JSON parsing**. Don’t parse and re-serialise it—changes to whitespace or key order change the signature.
2. Compute an **HMAC-SHA256** over those raw bytes, using your **webhook secret**, not your API token, as the key.
3. Hex-encode the result.
4. Compare it with the value in the `X-TechStore-Signature` header.

If verification fails, check the raw-body handling first, then confirm you’re using the webhook secret.
   evidence docs: ['api_webhook_signature', 'api_webhook_events', 'api_webhook_retries', 'api_idempotency']  orders: []

--- version `window` (earlier turns trimmed: 2)
1. Read the **exact raw request body before parsing JSON**.
2. Compute an **HMAC-SHA256** over those raw bytes, using your **webhook secret** as the key—not your API token.
3. Hex-encode the result.
4. Compare it with the value in the `X-TechStore-Signature` header.

If verification fails with a 403, check that you haven’t parsed and re-serialised the JSON before hashing. Changes to whitespace or key order change the signature.
   evidence docs: ['api_webhook_signature', 'api_webhook_events', 'api_webhook_retries', 'api_idempotency']  orders: []

--- version `facts` (earlier turns trimmed: 2)
1. Read the **exact raw request body before any JSON parsing**.
2. Compute its **HMAC-SHA256**, using your **webhook secret** as the key—not your API token.
3. Hex-encode the result and compare it with the `X-TechStore-Signature` header.

Do not parse and re-serialise the JSON before hashing: changes to whitespace or key order change the signature and are the most common cause of a **403** from TechStore’s delivery checker.
   evidence docs: ['api_webhook_signature', 'api_webhook_events', 'api_webhook_retries', 'api_idempotency']  orders: []

--- version `summary` (earlier turns trimmed: 2)
1. Read the **raw request body bytes before parsing JSON**. Don’t parse and re-serialise the body—changes to whitespace or key order will change the signature.
2. Compute an **HMAC-SHA256** over those exact bytes, using your **webhook secret**, not your API token, as the key.
3. Hex-encode the result and compare it with the `X-TechStore-Signature` header.

If you’re seeing a 403, the two most common causes are signing a re-serialised body or using the API token instead of the webhook secret.
   evidence docs: ['api_webhook_signature', 'api_webhook_events', 'api_webhook_retries', 'api_idempotency']  orders: []

EVIDENCE (union of what the versions saw):
--- [api_idempotency] API Idempotency
All POST endpoints accept an Idempotency-Key header. A repeated request with the same key and an identical payload returns the original response without creating a second resource. A repeated key with a different payload returns 409. Keys are retained for 24 hours. Clients should generate a UUID per logical operation, not per HTTP attempt, so that retries reuse the same key.
--- [api_webhook_events] Webhook Event Types
Available events: order.created, order.shipped, order.delivered, order.cancelled, order.returned, refund.initiated, refund.completed, inventory.low. Events are subscribed per endpoint in the dashboard. Payloads include the event type, a timestamp, and the affected resource. Event ordering is not guaranteed; use the timestamp rather than arrival order.
--- [api_webhook_retries] Webhook Delivery and Retries
Webhooks expect a 2xx response within 5 seconds. Non-2xx or timeout triggers retries at 1, 5, 25 and 125 minutes, then the endpoint is marked unhealthy and deliveries pause until reactivated in the dashboard. Handlers must be idempotent, because a duplicate delivery is possible even after a successful response. Each delivery carries an X-TechStore-Delivery-Id that is stable across retries.
--- [api_webhook_signature] Webhook Signature Verification and 403 Errors
Every webhook carries an X-TechStore-Signature header containing an HMAC-SHA256 of the raw request body, keyed with the webhook secret, hex encoded. A 403 returned by our delivery checker almost always means the signature was computed over a parsed and re-serialised body rather than the raw bytes; JSON re-serialisation changes key order and whitespace and therefore changes the HMAC. Compute the HMAC over the exact raw body before any JSON parsing. The second most common cause is using the API token instead of the webhook secret as the HMAC key.

========== c06 turn 4 ==========
CONVERSATION SO FAR (as it really happened, `off` version):
  CUSTOMER: Do you sell washing machines?
  AGENT: No, TechStore does not sell washing machines or other home appliances.
  CUSTOMER: Okay, what laptops do you have then?
  AGENT: We have three laptops:

| Laptop | Price | Key specifications |
|---|---:|---|
| **PulseBook Air 13** | ₹44,999 | 13.3-inch IPS display, Intel Core Ultra 3, 8 GB RAM, 256 GB SSD, 1.12 kg |
| **PulseBook 14** | ₹64,999 | 14-inch 2.8K OLED display, Intel Core Ultra 5, 16 GB RAM, 512 GB SSD, 1.29 kg |
| **PulseBook Pro 16** | ₹1,34,999 | 16-inch 3.2K OLED display, Intel Core Ultra 9, 32 GB RAM, 1 TB SSD, RTX 4060 graphics |

All include a **“2-year manufacturer warranty”**. The PulseBook 14 and Pro 16 also include **“one year of accidental damage protection”**; the Air 13 does not.

What’s your budget, and what will you mainly use it for?
  CUSTOMER: Which is the lightest one?
  AGENT: The **PulseBook Air 13** is our lightest laptop at **1.12 kg**, priced at **₹44,999**.

THIS TURN, CUSTOMER: Can I pay for it in EMI?

--- version `off` (earlier turns trimmed: 0)
EMI is available on credit cards from **12 partner banks** for **“orders above ₹5,000”**, over **3, 6, 9 or 12 months**.

I don't have information about EMI eligibility for the previously mentioned laptop; its details were not verified in TechStore’s reference documents.
   evidence docs: ['bill_emi', 'prod_clearview32', 'prod_aurawatch3', 'prod_aurawatch_pro']  orders: []

--- version `window` (earlier turns trimmed: 1)
Sorry, my earlier laptop details weren’t supported by TechStore’s product records, so I can’t confirm that model or its price.

TechStore offers EMI on credit cards from **“12 partner banks”** for **“orders above ₹5,000”**, over **“3, 6, 9 or 12 months”**. **“No-cost EMI is offered on selected products”**.

I don't have information about EMI eligibility for the PulseBook Air 13.
   evidence docs: ['bill_emi', 'prod_clearview32', 'prod_aurawatch3', 'prod_aurawatch_pro']  orders: []

--- version `facts` (earlier turns trimmed: 1)
Yes—EMI is available on credit cards from 12 partner banks for **“orders above ₹5,000”**, over **3, 6, 9 or 12 months**. “No-cost EMI” is offered on selected products.

I’m sorry—the laptop details I gave earlier weren’t supported by TechStore’s records. I don't have information about the PulseBook Air 13’s availability, price or no-cost EMI eligibility.
   evidence docs: ['bill_emi', 'prod_clearview32', 'prod_aurawatch3', 'prod_aurawatch_pro']  orders: []

--- version `summary` (earlier turns trimmed: 1)
Yes—EMI is available on credit cards from **12 partner banks** for **“orders above ₹5,000”**, with **3, 6, 9 or 12 months** repayment options.

I don't have information about whether the PulseBook Air 13 qualifies for no-cost EMI or which banks are partners.
   evidence docs: ['bill_emi', 'prod_clearview32', 'prod_aurawatch3', 'prod_aurawatch_pro']  orders: []

EVIDENCE (union of what the versions saw):
--- [bill_emi] EMI and No-Cost EMI
EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount. If an order paid by no-cost EMI is returned, the discount is deducted from the refund and the bank may still charge interest already levied; the bank must be contacted to cancel the EMI plan.
--- [prod_aurawatch3] AuraWatch 3 Smartwatch
Fitness smartwatch. Price ₹8,999. 1.4-inch AMOLED display, 14-day battery, heart-rate and SpO2 sensors, built-in GPS, 5 ATM water resistance, sleep tracking. Compatible with Android 9 and above and iOS 14 and above. 1-year manufacturer warranty. Worn on the wrist, therefore non-returnable once used, under the hygiene policy.
--- [prod_aurawatch_pro] AuraWatch Pro Smartwatch
Premium fitness smartwatch. Price ₹15,999. 1.5-inch AMOLED always-on display, 18-day battery, ECG and SpO2 sensors, dual-band GPS, 10 ATM water resistance, offline maps, 100 sport modes. Compatible with Android 10 and above and iOS 15 and above. 2-year manufacturer warranty. Non-returnable once used, under the hygiene policy.
--- [prod_clearview32] ClearView 32 Ultra Monitor
32-inch monitor. Price ₹39,999. 4K UHD IPS Black panel, 165 Hz refresh, 1 ms response, 99 percent DCI-P3, HDR600, USB-C with 140 W power delivery, built-in KVM switch, height and pivot adjustable stand, VESA 100. 3-year manufacturer warranty including a zero-bright-dot pixel guarantee.

========== c07 turn 4 ==========
CONVERSATION SO FAR (as it really happened, `off` version):
  CUSTOMER: My payment failed but money got debited
  AGENT: I’m sorry—that can be worrying. A failed payment with money debited means your bank has placed a temporary hold.

1. Allow the hold to reverse automatically: card and UPI payments take **“5 to 7 business days”**; net banking can take **“up to 10” business days**.
2. No order is created for a failed payment, so there’s nothing to cancel.
3. If that period has passed, contact support with your bank reference number so TechStore can raise a chargeback trace with the payment gateway.

How much was debited, which payment method did you use, and when did you pay?
  CUSTOMER: It was UPI
  AGENT: For UPI, the temporary hold reverses automatically within **“5 to 7 business days”**. No order was created, so there’s nothing to cancel.

How much was debited, and on what date? If the reversal period has passed, support can raise a chargeback trace with the payment gateway using your bank reference number.
  CUSTOMER: It's been 8 days already
  AGENT: I’m sorry the money hasn’t returned yet. UPI holds reverse within **“5 to 7 business days”**, so 8 calendar days may still be within that period.

1. Please share the debited amount and exact payment date so we can check the timeline.
2. If more than 7 business days have passed, contact support with your bank reference number. TechStore will raise a chargeback trace with the payment gateway.

No order was created for the failed payment, so there’s nothing to cancel.

THIS TURN, CUSTOMER: Who should I contact now?

--- version `off` (earlier turns trimmed: 0)
I don't have that information. I can connect you with a human agent who can help.

I’m sorry—my earlier claims about UPI reversal timelines and chargeback traces weren’t supported by TechStore’s reference information.
   evidence docs: ['pol_damaged_in_transit', 'pol_preorder', 'ship_tracking', 'pol_exchange']  orders: []

--- version `window` (earlier turns trimmed: 1)
I don't have that information. I can connect you with a human agent who can help.

I’m sorry—my earlier claims about UPI reversal timelines and chargeback traces weren’t supported by TechStore’s available policies.
   evidence docs: ['pol_damaged_in_transit', 'pol_preorder', 'ship_tracking', 'pol_exchange']  orders: []

--- version `facts` (earlier turns trimmed: 1)
I don't have that information. I can connect you with a human agent who can help.

I’m sorry—my earlier statements about a “5 to 7 business days” reversal window and a chargeback trace were not supported by TechStore’s reference information.
   evidence docs: ['pol_damaged_in_transit', 'pol_preorder', 'ship_tracking', 'pol_exchange']  orders: []

--- version `summary` (earlier turns trimmed: 1)
I don't have that information. I can connect you with a human agent who can help.
   evidence docs: ['pol_damaged_in_transit', 'pol_preorder', 'ship_tracking', 'pol_exchange']  orders: []

EVIDENCE (union of what the versions saw):
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [pol_exchange] Exchange Policy
An exchange can be requested within 30 days of delivery for a different size, colour or variant of the same product line, subject to stock. If the new variant costs more, the difference is charged before dispatch. If it costs less, the difference is refunded. Only one exchange is permitted per order line.
--- [pol_preorder] Pre-Orders
Pre-ordered items are charged at the time of order, not at dispatch. The estimated dispatch date on the product page is indicative; if it slips by more than 14 days the customer may cancel for a full refund. The 30-day return window begins at delivery, not at the order date.
--- [ship_tracking] Tracking an Order
A tracking link is emailed and sent by SMS when the order is marked Shipped. Tracking can also be seen under Orders in the account. Tracking information can take up to 12 hours after dispatch to become active with the courier. If tracking has not updated for more than 48 hours, contact support so a courier trace can be raised.

========== c08 turn 4 ==========
CONVERSATION SO FAR (as it really happened, `off` version):
  CUSTOMER: My AuraWatch 3 stopped charging after 4 months
  AGENT: I’m sorry your AuraWatch 3 has stopped charging after just 4 months. It comes with a “1-year manufacturer warranty,” so it is still within the warranty period.

I don't have information about charging troubleshooting for the AuraWatch 3 or whether this fault qualifies for warranty coverage. I can connect you with a human agent to help assess the issue.
  CUSTOMER: Is that covered under warranty?
  AGENT: It may be covered. Your AuraWatch 3 has a “1-year manufacturer warranty,” counted from the delivery date, so at 4 months it is within that period.

The warranty covers “manufacturing defects and component failure under normal use.” It excludes “physical damage, liquid ingress, unauthorised repair, or normal battery capacity decline above 80 percent of the rated capacity.”

I don't have information about the cause of your charging fault, so I can’t confirm coverage. I can connect you with a human agent to help assess it.
  CUSTOMER: How do I send it in?
  AGENT: 1. Raise a service request from **Orders** in your TechStore account, or contact support with your order ID.
2. TechStore arranges a “free pickup for products above ₹5,000”; smaller items are shipped by you and “reimbursed up to ₹200.”
3. Diagnosis takes “3 to 5 business days” at the service centre. If found defective, the watch is repaired or replaced; if no fault is found, it is returned at no charge.

I also need to correct my earlier reply: I don't have information about the AuraWatch 3’s specific warranty duration or price, so I can’t confirm its warranty period or which shipping option applies.

THIS TURN, CUSTOMER: Will you pick it up from my home?

--- version `off` (earlier turns trimmed: 0)
TechStore arranges a “free pickup for products above ₹5,000.” For smaller items, you ship the product yourself and are “reimbursed up to ₹200.”

I don't have information about your watch’s purchase price or whether pickup is available from your home address.
   evidence docs: ['pol_damaged_in_transit', 'ship_open_box', 'pol_warranty_claim', 'ship_tracking']  orders: []

--- version `window` (earlier turns trimmed: 1)
TechStore arranges a “free pickup for products above ₹5,000.” For smaller items, you ship it yourself and are “reimbursed up to ₹200.”

I don't have information about your watch’s price or whether pickup is available from your home address.
   evidence docs: ['pol_damaged_in_transit', 'ship_open_box', 'pol_warranty_claim', 'ship_tracking']  orders: []

--- version `facts` (earlier turns trimmed: 1)
TechStore arranges a “free pickup for products above ₹5,000.” For smaller items, you ship the product yourself, and shipping is “reimbursed up to ₹200.”

I don't have information about your AuraWatch 3’s purchase price or whether pickup is available from your home address.
   evidence docs: ['pol_damaged_in_transit', 'ship_open_box', 'pol_warranty_claim', 'ship_tracking']  orders: []

--- version `summary` (earlier turns trimmed: 1)
TechStore arranges a “free pickup for products above ₹5,000.” For smaller items, you ship the product yourself and are reimbursed “up to ₹200.”

I don't have information about your watch’s purchase price or whether pickup is specifically from your home. A human agent can help confirm those details.
   evidence docs: ['pol_damaged_in_transit', 'ship_open_box', 'pol_warranty_claim', 'ship_tracking']  orders: []

EVIDENCE (union of what the versions saw):
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [pol_warranty_claim] How to Raise a Warranty Claim
To claim warranty, raise a service request from Orders in the account, or contact support with the order ID. TechStore arranges a free pickup for products above ₹5,000; smaller items are shipped by the customer and reimbursed up to ₹200. Diagnosis takes 3 to 5 business days at the service centre. If the unit is found defective it is repaired or replaced; if no fault is found it is returned at no charge.
--- [ship_open_box] Open-Box Delivery
Open-box delivery is available in 22 cities on orders above ₹20,000. The courier opens the package in the customer's presence for inspection before handover. Refusal at open-box inspection is free and refunds process within 5 to 7 business days. Open-box delivery adds 1 business day to the estimate.
--- [ship_tracking] Tracking an Order
A tracking link is emailed and sent by SMS when the order is marked Shipped. Tracking can also be seen under Orders in the account. Tracking information can take up to 12 hours after dispatch to become active with the courier. If tracking has not updated for more than 48 hours, contact support so a courier trace can be raised.

========== c08 turn 5 ==========
CONVERSATION SO FAR (as it really happened, `off` version):
  CUSTOMER: My AuraWatch 3 stopped charging after 4 months
  AGENT: I’m sorry your AuraWatch 3 has stopped charging after just 4 months. It comes with a “1-year manufacturer warranty,” so it is still within the warranty period.

I don't have information about charging troubleshooting for the AuraWatch 3 or whether this fault qualifies for warranty coverage. I can connect you with a human agent to help assess the issue.
  CUSTOMER: Is that covered under warranty?
  AGENT: It may be covered. Your AuraWatch 3 has a “1-year manufacturer warranty,” counted from the delivery date, so at 4 months it is within that period.

The warranty covers “manufacturing defects and component failure under normal use.” It excludes “physical damage, liquid ingress, unauthorised repair, or normal battery capacity decline above 80 percent of the rated capacity.”

I don't have information about the cause of your charging fault, so I can’t confirm coverage. I can connect you with a human agent to help assess it.
  CUSTOMER: How do I send it in?
  AGENT: 1. Raise a service request from **Orders** in your TechStore account, or contact support with your order ID.
2. TechStore arranges a “free pickup for products above ₹5,000”; smaller items are shipped by you and “reimbursed up to ₹200.”
3. Diagnosis takes “3 to 5 business days” at the service centre. If found defective, the watch is repaired or replaced; if no fault is found, it is returned at no charge.

I also need to correct my earlier reply: I don't have information about the AuraWatch 3’s specific warranty duration or price, so I can’t confirm its warranty period or which shipping option applies.
  CUSTOMER: Will you pick it up from my home?
  AGENT: TechStore arranges a “free pickup for products above ₹5,000.” For smaller items, you ship the product yourself and are “reimbursed up to ₹200.”

I don't have information about your watch’s purchase price or whether pickup is available from your home address.

THIS TURN, CUSTOMER: How long will the repair take?

--- version `off` (earlier turns trimmed: 0)
Diagnosis takes “3 to 5 business days” at the service centre. If the watch is found defective, it will be repaired or replaced.

I don't have information about the total repair time or return-delivery timeframe.
   evidence docs: ['pol_damaged_in_transit', 'pol_warranty_claim', 'ship_open_box', 'svc_out_of_warranty']  orders: []

--- version `window` (earlier turns trimmed: 2)
Diagnosis takes “3 to 5 business days” at the service centre. If the unit is found defective, it is repaired or replaced.

I don't have information about the repair time after diagnosis or the total turnaround time, including shipping.
   evidence docs: ['pol_damaged_in_transit', 'pol_warranty_claim', 'ship_open_box', 'svc_out_of_warranty']  orders: []

--- version `facts` (earlier turns trimmed: 2)
Diagnosis takes “3 to 5 business days” at the service centre. If the watch is found defective, it is repaired or replaced.

I don't have information about the repair time after diagnosis or the total turnaround including shipping.
   evidence docs: ['pol_damaged_in_transit', 'pol_warranty_claim', 'ship_open_box', 'svc_out_of_warranty']  orders: []

--- version `summary` (earlier turns trimmed: 2)
Diagnosis takes “3 to 5 business days” at the service centre. If the watch is found defective, it will be repaired or replaced.

I don't have information about how long the repair or return delivery will take after diagnosis.
   evidence docs: ['pol_damaged_in_transit', 'pol_warranty_claim', 'ship_open_box', 'svc_out_of_warranty']  orders: []

EVIDENCE (union of what the versions saw):
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [pol_warranty_claim] How to Raise a Warranty Claim
To claim warranty, raise a service request from Orders in the account, or contact support with the order ID. TechStore arranges a free pickup for products above ₹5,000; smaller items are shipped by the customer and reimbursed up to ₹200. Diagnosis takes 3 to 5 business days at the service centre. If the unit is found defective it is repaired or replaced; if no fault is found it is returned at no charge.
--- [ship_open_box] Open-Box Delivery
Open-box delivery is available in 22 cities on orders above ₹20,000. The courier opens the package in the customer's presence for inspection before handover. Refusal at open-box inspection is free and refunds process within 5 to 7 business days. Open-box delivery adds 1 business day to the estimate.
--- [svc_out_of_warranty] Out-of-Warranty Repair
Out-of-warranty repairs are chargeable. A diagnosis fee of ₹499 applies and is waived if the repair is approved. A quotation is shared before any work begins and no work proceeds without approval. Repaired parts carry a 90-day warranty on the replaced component only.

========== c08 turn 6 ==========
CONVERSATION SO FAR (as it really happened, `off` version):
  CUSTOMER: My AuraWatch 3 stopped charging after 4 months
  AGENT: I’m sorry your AuraWatch 3 has stopped charging after just 4 months. It comes with a “1-year manufacturer warranty,” so it is still within the warranty period.

I don't have information about charging troubleshooting for the AuraWatch 3 or whether this fault qualifies for warranty coverage. I can connect you with a human agent to help assess the issue.
  CUSTOMER: Is that covered under warranty?
  AGENT: It may be covered. Your AuraWatch 3 has a “1-year manufacturer warranty,” counted from the delivery date, so at 4 months it is within that period.

The warranty covers “manufacturing defects and component failure under normal use.” It excludes “physical damage, liquid ingress, unauthorised repair, or normal battery capacity decline above 80 percent of the rated capacity.”

I don't have information about the cause of your charging fault, so I can’t confirm coverage. I can connect you with a human agent to help assess it.
  CUSTOMER: How do I send it in?
  AGENT: 1. Raise a service request from **Orders** in your TechStore account, or contact support with your order ID.
2. TechStore arranges a “free pickup for products above ₹5,000”; smaller items are shipped by you and “reimbursed up to ₹200.”
3. Diagnosis takes “3 to 5 business days” at the service centre. If found defective, the watch is repaired or replaced; if no fault is found, it is returned at no charge.

I also need to correct my earlier reply: I don't have information about the AuraWatch 3’s specific warranty duration or price, so I can’t confirm its warranty period or which shipping option applies.
  CUSTOMER: Will you pick it up from my home?
  AGENT: TechStore arranges a “free pickup for products above ₹5,000.” For smaller items, you ship the product yourself and are “reimbursed up to ₹200.”

I don't have information about your watch’s purchase price or whether pickup is available from your home address.
  CUSTOMER: How long will the repair take?
  AGENT: Diagnosis takes “3 to 5 business days” at the service centre. If the watch is found defective, it will be repaired or replaced.

I don't have information about the total repair time or return-delivery timeframe.

THIS TURN, CUSTOMER: What if they find no fault?

--- version `off` (earlier turns trimmed: 0)
If the service centre finds no fault, your watch will be “returned at no charge.”
   evidence docs: ['pol_damaged_in_transit', 'svc_out_of_warranty', 'pol_warranty_claim', 'pol_replacement_warranty']  orders: []

--- version `window` (earlier turns trimmed: 3)
If no fault is found, your item is “returned at no charge.”
   evidence docs: ['pol_damaged_in_transit', 'svc_out_of_warranty', 'pol_warranty_claim', 'pol_replacement_warranty']  orders: []

--- version `facts` (earlier turns trimmed: 3)
If no fault is found with your AuraWatch 3 during warranty diagnosis, “it is returned at no charge.”
   evidence docs: ['pol_damaged_in_transit', 'svc_out_of_warranty', 'pol_warranty_claim', 'pol_replacement_warranty']  orders: []

--- version `summary` (earlier turns trimmed: 3)
If no fault is found, your watch will be “returned at no charge.”
   evidence docs: ['pol_damaged_in_transit', 'svc_out_of_warranty', 'pol_warranty_claim', 'pol_replacement_warranty']  orders: []

EVIDENCE (union of what the versions saw):
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [pol_replacement_warranty] Warranty on Replaced Units
When a unit is replaced under warranty, the replacement inherits the remaining warranty of the original; it does not start a fresh term. If fewer than 90 days remain, the replacement carries 90 days from the replacement date. Replacement units may be factory refurbished and are functionally equivalent with matching cosmetic grade.
--- [pol_warranty_claim] How to Raise a Warranty Claim
To claim warranty, raise a service request from Orders in the account, or contact support with the order ID. TechStore arranges a free pickup for products above ₹5,000; smaller items are shipped by the customer and reimbursed up to ₹200. Diagnosis takes 3 to 5 business days at the service centre. If the unit is found defective it is repaired or replaced; if no fault is found it is returned at no charge.
--- [svc_out_of_warranty] Out-of-Warranty Repair
Out-of-warranty repairs are chargeable. A diagnosis fee of ₹499 applies and is waived if the repair is approved. A quotation is shared before any work begins and no work proceeds without approval. Repaired parts carry a 90-day warranty on the replaced component only.
