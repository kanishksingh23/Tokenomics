# FAQ answers to approve

These answers reach customers **with no model checking them**. For each one, check:
every fact is in the source text below it; nothing important from the source is missing
for this question; the tone is right. Then approve, e.g.:

```
python faq_shortcut.py --approve faq_cancel,faq_emi --by Kanishk
```

To change an answer, edit it in `data/faq.jsonl` first (keep `sources` accurate).

## faq_return_window: What is your return window?  (draft)

**Answer:** You can return an item within 30 days of delivery. The 30 days count from the delivery date on the tracking record, not the order date. Return it in its original packaging with all accessories, manuals and free gifts; a return raised on day 31 or later is rejected automatically. Some items, such as headphones and earbuds, can't be returned once the seal is broken.

*Also matches:* what is your return policy; how many days do i get to send a product back; is there a deadline for returns; return period?

> **Source `pol_return_window`: Return Window**  
> TechStore accepts returns within 30 days of delivery. The 30 days are counted from the delivery date shown on the tracking record, not the order date. Items must be returned in their original packaging with all accessories, manuals and free gifts included. A return raised on day 31 or later is rejected automatically by the returns system.

> **Source `pol_return_exclusions`: Non-Returnable Items**  
> For hygiene reasons the following are non-returnable once the seal is broken: headphones of every type (over-ear, on-ear and in-ear), earbuds, fitness bands worn on the wrist, and any personal grooming device. Opened software licences and redeemed digital gift cards are also non-returnable. These items remain covered by warranty if they are faulty; a hygiene exclusion never removes warranty rights.

## faq_non_returnable: Which items can't be returned?  (draft)

**Answer:** For hygiene reasons, these can't be returned once the seal is broken: headphones of every type (over-ear, on-ear and in-ear), earbuds, fitness bands worn on the wrist, and personal grooming devices. Opened software licences and redeemed digital gift cards can't be returned either. If any of these is faulty, it is still covered by warranty.

*Also matches:* what products are non returnable; are headphones returnable after opening; can i send back a fitness band i have worn; which things cant be returned once opened

> **Source `pol_return_exclusions`: Non-Returnable Items**  
> For hygiene reasons the following are non-returnable once the seal is broken: headphones of every type (over-ear, on-ear and in-ear), earbuds, fitness bands worn on the wrist, and any personal grooming device. Opened software licences and redeemed digital gift cards are also non-returnable. These items remain covered by warranty if they are faulty; a hygiene exclusion never removes warranty rights.

## faq_refund_time: How long does a refund take?  (draft)

**Answer:** Once your returned item reaches our warehouse and is inspected, the refund is started within 2 business days. It then reaches your original payment method in 5 to 7 business days for cards and UPI, or up to 10 business days for net banking. Refunds always go back to the original payment method; they can't be sent to a different card or account.

*Also matches:* when will i get my money back after returning; how many days for refund to reach my account; refund timeline for upi; can my refund go to a different card

> **Source `pol_refund_timeline`: Refund Processing Time**  
> Once a returned item is received and inspected at our warehouse, refunds are initiated within 2 business days. The money reaches the original payment method in 5 to 7 business days for cards and UPI, and up to 10 business days for net banking. Refunds are always issued to the original payment method; we cannot redirect a refund to a different card or account.

## faq_exchange: Can I exchange a product for a different colour or size?  (draft)

**Answer:** Yes. Within 30 days of delivery you can exchange for a different size, colour or variant of the same product line, if it's in stock. If the new variant costs more, the difference is charged before dispatch; if it costs less, the difference is refunded. One exchange is allowed per order line.

*Also matches:* can i swap my item for another colour; exchange policy; i want a different variant of the same product; how do exchanges work

> **Source `pol_exchange`: Exchange Policy**  
> An exchange can be requested within 30 days of delivery for a different size, colour or variant of the same product line, subject to stock. If the new variant costs more, the difference is charged before dispatch. If it costs less, the difference is refunded. Only one exchange is permitted per order line.

## faq_cancel: Can I cancel my order?  (draft)

**Answer:** You can cancel free of charge any time before the order is marked Shipped, and you get a full refund, including any delivery charge paid, within 5 to 7 business days. Once the order has shipped it can't be cancelled; you can refuse the delivery or raise a return after it arrives.

*Also matches:* how do i cancel an order; is there a fee to cancel; can i cancel after it has shipped; cancellation policy

> **Source `pol_cancellation`: Order Cancellation**  
> An order can be cancelled free of charge at any time before it is marked Shipped. Once shipped, cancellation is not possible; the customer should refuse delivery or raise a return after delivery. Cancelled orders are refunded in full, including any delivery charge paid, within 5 to 7 business days.

## faq_delivery_time: How long does delivery take?  (draft)

**Answer:** Metro cities: 1 to 2 business days. Tier-2 cities: 2 to 4 business days. Remote and north-eastern pin codes: 5 to 7 business days. Orders placed after 2 PM are processed the next business day, and estimates exclude Sundays and national holidays.

*Also matches:* when will my order arrive; delivery time to my city; how many days for shipping; do you deliver on sundays

> **Source `ship_delivery_times`: Delivery Timelines**  
> Metro cities: 1 to 2 business days. Tier-2 cities: 2 to 4 business days. Remote and north-eastern pin codes: 5 to 7 business days. Orders placed after 2 PM are processed the following business day. Delivery estimates exclude Sundays and national holidays.

## faq_delivery_charges: What are the delivery charges?  (draft)

**Answer:** Delivery is free on orders above ₹999; below that, a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149 and is available in metro cities only, for orders placed before 2 PM.

*Also matches:* how much does shipping cost; do you charge for delivery; is there express delivery; shipping fee?

> **Source `ship_charges`: Delivery Charges**  
> Delivery is free on all orders above ₹999. Below that a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149 and is available in metro cities only for orders placed before 2 PM. Delivery charges are refunded if the order is cancelled before shipping or if the item arrives damaged.

## faq_tracking: How do I track my order?  (draft)

**Answer:** When your order is marked Shipped, a tracking link is sent by email and SMS. You can also see tracking under Orders in your account. Tracking can take up to 12 hours after dispatch to become active with the courier; if it hasn't updated for more than 48 hours, contact support so a courier trace can be raised.

*Also matches:* where can i see my tracking link; how to check where my parcel is; tracking not updating; order tracking

> **Source `ship_tracking`: Tracking an Order**  
> A tracking link is emailed and sent by SMS when the order is marked Shipped. Tracking can also be seen under Orders in the account. Tracking information can take up to 12 hours after dispatch to become active with the courier. If tracking has not updated for more than 48 hours, contact support so a courier trace can be raised.

## faq_international: Do you ship internationally?  (draft)

**Answer:** No, TechStore ships within India only. We can't deliver to international addresses or to APO or diplomatic addresses. An order with an international billing address but an Indian delivery address is accepted.

*Also matches:* can you deliver abroad; do you ship to other countries; can i order from outside india; international delivery

> **Source `ship_international`: International Shipping**  
> TechStore ships within India only. We do not ship to international addresses and cannot deliver to APO or diplomatic addresses. Orders placed with an international billing address but an Indian delivery address are accepted.

## faq_payment_methods: Which payment methods do you accept?  (draft)

**Answer:** We accept UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000 (with a ₹49 handling fee, refunded if the order is cancelled before dispatch). Wallet payments and international cards are not accepted.

*Also matches:* can i pay by upi; do you take cash on delivery; can i use a wallet to pay; do you accept foreign credit cards

> **Source `bill_payment_methods`: Accepted Payment Methods**  
> TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.

## faq_emi: Do you offer EMI?  (draft)

**Answer:** Yes. EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount.

*Also matches:* can i pay in instalments; is no cost emi available; which banks offer emi; monthly payment options

> **Source `bill_emi`: EMI and No-Cost EMI**  
> EMI is available on credit cards from 12 partner banks for orders above ₹5,000, over 3, 6, 9 or 12 months. No-cost EMI is offered on selected products, where TechStore absorbs the interest as an upfront discount. If an order paid by no-cost EMI is returned, the discount is deducted from the refund and the bank may still charge interest already levied; the bank must be contacted to cancel the EMI plan.

## faq_gst_invoice: How do I get a GST invoice?  (draft)

**Answer:** A tax invoice is emailed within 24 hours of dispatch and can be downloaded from Orders. If you need your GSTIN on the invoice, enter it at checkout before placing the order: it can't be added afterwards, and a fresh invoice isn't issued for a completed order. Invoices remain downloadable for 8 years.

*Also matches:* where is my tax invoice; can you add my gstin to the bill; download invoice; invoice for my business purchase

> **Source `bill_invoice_gst`: Invoice and GST**  
> A tax invoice is emailed within 24 hours of dispatch and is downloadable from Orders. Business customers who need their GSTIN on the invoice must enter it at checkout, before placing the order. TechStore cannot add a GSTIN to an invoice afterwards and does not issue a fresh invoice for a completed order. Invoices remain downloadable for 8 years.

## faq_warranty: What does the warranty cover?  (draft)

**Answer:** Every product carries the manufacturer warranty stated on its product page, counted from the delivery date. It covers manufacturing defects and component failure under normal use. It does not cover physical damage, liquid ingress, unauthorised repair, or normal battery capacity decline above 80% of the rated capacity. Warranty is independent of the 30-day return window, so a product outside the return window may still be repaired or replaced under warranty.

*Also matches:* is my product under warranty; what is not covered by warranty; does warranty cover water damage; warranty after the return window

> **Source `pol_warranty_terms`: Standard Warranty Terms**  
> All products carry the manufacturer warranty stated on the product page, counted from the delivery date. Warranty covers manufacturing defects and component failure under normal use. It does not cover physical damage, liquid ingress, unauthorised repair, or normal battery capacity decline above 80 percent of the rated capacity. Warranty is independent of the 30-day return window: a product outside the return window may still be repaired or replaced under warranty.

## faq_warranty_claim: How do I make a warranty claim?  (draft)

**Answer:** Raise a service request from Orders in your account, or contact support with your order ID. TechStore arranges a free pickup for products above ₹5,000; smaller items are shipped by you and reimbursed up to ₹200. Diagnosis takes 3 to 5 business days at the service centre. If the unit is defective it is repaired or replaced; if no fault is found it is returned at no charge.

*Also matches:* how to get a faulty product repaired; raise a service request; warranty claim process; do you pick up items for repair

> **Source `pol_warranty_claim`: How to Raise a Warranty Claim**  
> To claim warranty, raise a service request from Orders in the account, or contact support with the order ID. TechStore arranges a free pickup for products above ₹5,000; smaller items are shipped by the customer and reimbursed up to ₹200. Diagnosis takes 3 to 5 business days at the service centre. If the unit is found defective it is repaired or replaced; if no fault is found it is returned at no charge.

## faq_password: How do I reset my password?  (draft)

**Answer:** Use Forgot Password on the sign-in page and a reset link, valid for 30 minutes, is emailed to you. If it doesn't arrive, check your spam folder and confirm you're using the email address you registered with. After three failed sign-in attempts the account is locked for 15 minutes.

*Also matches:* forgot my password; reset link not received; my account is locked; cant sign in

> **Source `acc_password`: Password Reset**  
> Use Forgot Password on the sign-in page. A reset link valid for 30 minutes is emailed. If the email does not arrive, check spam and confirm the address matches the registered one; for privacy we do not disclose whether an address is registered. After three failed sign-in attempts the account is locked for 15 minutes.

## faq_two_factor: How do I turn on two-factor authentication?  (draft)

**Answer:** Enable it from Security in your account, using an authenticator app or SMS. Turning it on signs out all your other sessions. To turn it off you need to sign in with it; if you've lost the device, we verify your identity with your last order details and a government ID, and removal takes up to 48 hours.

*Also matches:* enable 2fa; set up an authenticator app; lost my phone with 2fa; how to switch off two factor

> **Source `acc_two_factor`: Two-Factor Authentication**  
> Two-factor authentication can be enabled from Security in the account, using an authenticator app or SMS. Enabling 2FA signs out all other sessions. To disable 2FA, current authentication is required; if the device is lost, identity is verified with the last order details and a government ID, and removal takes up to 48 hours.

## faq_stores: Do you have a physical store?  (draft)

**Answer:** No. TechStore is online-only, with no physical stores or showrooms, so there are no store opening hours. Orders are placed only on the TechStore website and app.

*Also matches:* where is your showroom; what are your store timings; can i visit a store to see a laptop; is there an offline shop

> **Source `about_techstore`: About TechStore**  
> TechStore is an online-only consumer electronics retailer in India. It has no physical retail stores or showrooms, so there are no store opening hours; orders are placed only on the TechStore website and app. TechStore sells six product families: headphones and earbuds (SoundWave), laptops (PulseBook), tablets (NovaTab), smartwatches (AuraWatch), monitors (ClearView), and chargers and power banks (VoltCharge, VoltBank). TechStore does not sell mobile phones, televisions, cameras, gaming consoles, or home appliances such as washing machines, refrigerators, or air conditioners. Repairs are handled at authorised service centres in 48 cities. Customer support is available by chat and email from 9 AM to 9 PM IST, seven days a week.

## faq_support_hours: When is customer support available?  (draft)

**Answer:** Customer support is available by chat and email from 9 AM to 9 PM IST, seven days a week.

*Also matches:* how can i contact customer care; support timings; is support open on weekends; how do i reach you

> **Source `about_techstore`: About TechStore**  
> TechStore is an online-only consumer electronics retailer in India. It has no physical retail stores or showrooms, so there are no store opening hours; orders are placed only on the TechStore website and app. TechStore sells six product families: headphones and earbuds (SoundWave), laptops (PulseBook), tablets (NovaTab), smartwatches (AuraWatch), monitors (ClearView), and chargers and power banks (VoltCharge, VoltBank). TechStore does not sell mobile phones, televisions, cameras, gaming consoles, or home appliances such as washing machines, refrigerators, or air conditioners. Repairs are handled at authorised service centres in 48 cities. Customer support is available by chat and email from 9 AM to 9 PM IST, seven days a week.

## faq_what_we_sell: What products do you sell?  (draft)

**Answer:** TechStore sells six product families: headphones and earbuds (SoundWave), laptops (PulseBook), tablets (NovaTab), smartwatches (AuraWatch), monitors (ClearView), and chargers and power banks (VoltCharge, VoltBank). We don't sell mobile phones, televisions, cameras, gaming consoles, or home appliances such as washing machines, refrigerators or air conditioners.

*Also matches:* do you sell phones; what kind of electronics do you have; do you sell tvs; which brands do you carry

> **Source `about_techstore`: About TechStore**  
> TechStore is an online-only consumer electronics retailer in India. It has no physical retail stores or showrooms, so there are no store opening hours; orders are placed only on the TechStore website and app. TechStore sells six product families: headphones and earbuds (SoundWave), laptops (PulseBook), tablets (NovaTab), smartwatches (AuraWatch), monitors (ClearView), and chargers and power banks (VoltCharge, VoltBank). TechStore does not sell mobile phones, televisions, cameras, gaming consoles, or home appliances such as washing machines, refrigerators, or air conditioners. Repairs are handled at authorised service centres in 48 cities. Customer support is available by chat and email from 9 AM to 9 PM IST, seven days a week.

## faq_price_match: Do you match competitors' prices?  (draft)

**Answer:** Yes. If you find the identical product cheaper on a competing authorised Indian retailer within 7 days of your purchase, TechStore refunds the difference. The listing must be for a new, sealed unit sold and shipped by that retailer itself, not a marketplace seller. Price matching doesn't apply during flash sales or clearance events.

*Also matches:* price match guarantee; i found it cheaper on another site; will you refund the price difference if its cheaper elsewhere; price matching rules

> **Source `pol_price_match`: Price Match Guarantee**  
> If a customer finds the identical product cheaper on a competing authorised Indian retailer within 7 days of their purchase, TechStore refunds the difference. The competing listing must be for a new, sealed unit sold and shipped by the retailer itself, not a marketplace seller. Price matching does not apply during flash sales or clearance events.

## faq_gift_cards: How do gift cards work?  (draft)

**Answer:** Gift cards are valid for 12 months from issue and can be used across multiple orders, but they can't be exchanged for cash. If an order paid partly by gift card is returned, the gift-card portion is refunded as store credit and the rest to the original payment method. Redeemed gift cards are non-returnable.

*Also matches:* how long is a gift card valid; can i get cash for my gift card; gift card expiry; returning something i paid for with a gift card

> **Source `bill_gift_card`: Gift Cards and Store Credit**  
> Gift cards are valid for 12 months from issue and can be used across multiple orders. They cannot be exchanged for cash. If an order paid partly by gift card is returned, the gift-card portion is refunded as store credit and the remainder to the original payment method. Redeemed gift cards are non-returnable.

## faq_promo_codes: Can I use more than one promo code?  (draft)

**Answer:** No. One promotional code applies per order, and codes can't be combined with each other or with no-cost EMI unless the code explicitly says so. A code can't be applied after an order is placed; a replacement order is needed. If a code requires a minimum basket value and a return takes the order below it, the discount is recovered from the refund.

*Also matches:* can i combine coupons; apply a coupon after ordering; promo code with no cost emi; coupon rules

> **Source `bill_promo_codes`: Promotional Codes and Stacking**  
> One promotional code applies per order. Codes cannot be combined with each other or with no-cost EMI unless the code explicitly states otherwise. A code cannot be applied after an order is placed and a replacement order is required. Codes tied to a minimum basket value are void if returns take the order below that value, and the discount is recovered from the refund.
