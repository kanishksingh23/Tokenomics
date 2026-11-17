# Answers to grade

Grade each answer ONLY against the evidence shown with it. Store date: 30 September 2026.
Verdicts: correct / partial / wrong / hallucinated (rubric: Tokenomics.md §7, Grading Rubric).


========== q001 [simple_faq] ==========
QUESTION: How long do I have to return something?
NEEDED DOCS: ['pol_return_window']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
You can return an item within **30 days of delivery**, counted from the delivery date shown on the tracking record—not the order date. A return raised on day 31 or later is rejected automatically.

Items must be returned in their **“original packaging with all accessories, manuals and free gifts included.”**

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
Delivery is free on “all orders above ₹999.” Below ₹999, a flat ₹79 delivery charge applies.

Express next-day delivery costs ₹149 and is available in metro cities only for orders placed before 2 PM.

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
Your order #48213 has shipped via BlueDart and is due today, 30 September 2026.

- **Tracking ID:** BD4471920381
- **Track it:** Check **Orders** in your TechStore account, or use the tracking link sent by email and SMS.

If tracking has not updated for more than 48 hours, contact support so a courier trace can be raised.

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

========== q014 [product_info] ==========
QUESTION: Does the ClearView 27 support USB-C?
NEEDED DOCS: ['prod_clearview27']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Yes, the ClearView 27 supports USB-C with video input and up to 90 W power delivery, so it can display video and charge a compatible laptop through one cable.

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
No, the NovaTab 11 stylus is sold separately for ₹4,999.

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
For a noisy open-plan office, **the Y500 is the better choice**—it’s specifically recommended over the X200 for that environment.

| Feature | X200 | Y500 |
|---|---|---|
| Price | ₹12,999 | ₹24,999 |
| Noise cancellation | 35 dB hybrid ANC | 45 dB adaptive ANC, plus transparency mode |
| Battery life | 40 hours | 60 hours |
| Multipoint pairing | Two devices | Three devices |
| Weight | 250 g | 268 g |

Choose the **Y500 for stronger noise cancellation** and memory-foam earcups; choose the **X200 if budget is your priority**.

Both have a **“2-year manufacturer warranty”** and are **“Non-returnable once the seal is opened, under the hygiene policy.”**

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
**For demanding video editing, I’d lean toward the Pro 16; for budget-conscious editing, the PulseBook 14 is better value.** The Pro costs slightly more than twice as much—not exactly double.

| Specification | PulseBook 14 | PulseBook Pro 16 |
|---|---|---|
| Price | ₹64,999 | ₹1,34,999 |
| Processor | Intel Core Ultra 5 | Intel Core Ultra 9 |
| RAM | 16 GB | 32 GB |
| Storage | 512 GB NVMe SSD | 1 TB NVMe SSD |
| Discrete graphics | Not listed | RTX 4060 |
| Display | 14-inch 2.8K OLED, 90 Hz | 16-inch 3.2K OLED, 120 Hz |
| Weight | 1.29 kg | 1.95 kg |

The **₹70,000 premium** gets you a higher-tier processor, double the RAM and storage, discrete RTX 4060 graphics, and a larger, higher-resolution display. Those are the main reasons to choose it for video editing; the 14 is considerably cheaper and lighter.

I don't have information about editing benchmarks or performance in your particular video-editing software, so I can’t say the Pro delivers twice the performance.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_pulsebook14] PulseBook 14 Laptop
14-inch ultrabook. Price ₹64,999. Intel Core Ultra 5, 16 GB LPDDR5 RAM, 512 GB NVMe SSD, 14-inch 2.8K OLED display at 90 Hz, 65 W USB-C charging, 1.29 kg, 12-hour rated battery. Ports: two USB-C Thunderbolt, one USB-A, HDMI 2.1, headphone jack. 2-year manufacturer warranty including one year of accidental damage protection.
--- [prod_pulsebook_pro16] PulseBook Pro 16 Laptop
16-inch creator laptop. Price ₹1,34,999. Intel Core Ultra 9, 32 GB RAM, 1 TB NVMe SSD, discrete RTX 4060 graphics, 16-inch 3.2K OLED at 120 Hz, 100 W USB-C charging, 1.95 kg. 2-year manufacturer warranty including one year of accidental damage protection.
--- [prod_pulsebook_air13] PulseBook Air 13 Laptop
13-inch entry ultrabook. Price ₹44,999. Intel Core Ultra 3, 8 GB LPDDR5 RAM, 256 GB NVMe SSD, 13.3-inch 1920x1200 IPS display at 60 Hz, 45 W USB-C charging, 1.12 kg, 10-hour rated battery. Ports: two USB-C, one USB-A, headphone jack. No HDMI port. 2-year manufacturer warranty. Accidental damage protection is not included on the Air 13; it is included only on the PulseBook 14 and Pro 16.
--- [svc_accidental_damage] Accidental Damage Protection
PulseBook 14 and PulseBook Pro 16 include one year of accidental damage protection from the delivery date, covering drops and liquid spills. One claim is permitted in the coverage year, with a customer contribution of 10 percent of the product price. Accidental damage protection does not cover theft, loss, or cosmetic damage that does not affect function.

========== q020 [product_comparison] ==========
QUESTION: I want a tablet for reading and a laptop for college. What should I buy under 1 lakh total?
NEEDED DOCS: ['prod_novatab11', 'prod_pulsebook14']   MISSING FROM WHAT THE MODEL SAW: ['prod_pulsebook14']

ANSWER:
I’d recommend this pair for reading and college:

| Product | Why it fits | Price |
|---|---|---:|
| **NovaTab Mini 8** | Compact 8.4-inch display at 90 Hz for reading; 6 GB RAM and 128 GB expandable storage | ₹17,999 |
| **PulseBook 14** | A balanced college option with Core Ultra 5, 16 GB RAM, 512 GB SSD, and a portable 1.29 kg design | ₹64,999 |
| **Total** | **₹17,002 under your ₹1,00,000 budget** | **₹82,998** |

**One caveat:** the Mini 8 does not support a stylus. If handwritten tablet notes matter, choose the **NovaTab 11 + stylus + PulseBook 14** instead, totalling **₹99,997**.

For reading rather than handwritten notes, I’d pick the first pair and save the difference.

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
If you have an **AuraWatch 3**, try these steps:

1. Allow Bluetooth and background activity for the companion app.
2. Confirm your phone runs Android 9 or later, or iOS 14 or later.
3. On Android, exclude the app from battery optimisation—this is the most common cause of syncing problems.
4. Force-close and reopen the app.
5. Ensure the watch firmware is current.

Is your watch an AuraWatch 3 or AuraWatch Pro?

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_watch_sync] Smartwatch Not Syncing
If AuraWatch 3 will not sync: confirm the companion app has Bluetooth and background-activity permission, confirm the phone runs Android 9 or later or iOS 14 or later, force-close and reopen the app, and ensure the watch firmware is current. Battery optimisation settings on some Android phones stop the app in the background and are the most common cause; exclude the app from optimisation.
--- [tsg_watch_inaccurate_hr] Heart Rate Readings Inaccurate
Optical heart-rate sensors need firm skin contact. Wear the watch one finger-width above the wrist bone, snug but not tight. Tattoos, very cold skin and loose fits all reduce accuracy. If readings remain implausible when stationary after adjusting fit, the sensor is a warranty defect.
--- [prod_aurawatch3] AuraWatch 3 Smartwatch
Fitness smartwatch. Price ₹8,999. 1.4-inch AMOLED display, 14-day battery, heart-rate and SpO2 sensors, built-in GPS, 5 ATM water resistance, sleep tracking. Compatible with Android 9 and above and iOS 14 and above. 1-year manufacturer warranty. Worn on the wrist, therefore non-returnable once used, under the hygiene policy.
--- [prod_aurawatch_pro] AuraWatch Pro Smartwatch
Premium fitness smartwatch. Price ₹15,999. 1.5-inch AMOLED always-on display, 18-day battery, ECG and SpO2 sensors, dual-band GPS, 10 ATM water resistance, offline maps, 100 sport modes. Compatible with Android 10 and above and iOS 15 and above. 2-year manufacturer warranty. Non-returnable once used, under the hygiene policy.

========== q025 [troubleshooting] ==========
QUESTION: My headphone battery drains much faster than advertised.
NEEDED DOCS: ['tsg_headphone_battery', 'pol_warranty_terms']   MISSING FROM WHAT THE MODEL SAW: ['pol_warranty_terms']

ANSWER:
Sorry your headphones aren’t lasting as expected. Which SoundWave model do you have, how many hours does a full charge last, and is active noise cancellation (ANC) on?

1. Test with ANC off and at a lower volume. ANC reduces rated battery life by roughly 30%.
2. Check for firmware updates in the SoundWave app.
3. Disable multipoint if you don’t need multiple devices connected.
4. Confirm the headphones power off rather than idle when removed.

If runtime with ANC off is below 50% of the rated battery life—under 20 hours for the X200 or 30 hours for the Y500—the battery is considered defective and covered by the “2-year manufacturer warranty”.

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
I understand why seeing three charges is worrying. For order #48712, only one payment was collected; the other two were duplicate authorisation holds, not separate orders.

Here’s the breakdown:
- **27 September — ₹12,999:** Settled payment for order #48712, which is still Processing.
- **27 September — ₹12,999:** Duplicate hold, reversed on **29 September**. This matches the one reversal you’ve seen.
- **27 September — ₹12,999:** Duplicate hold, still pending reversal and expected to reverse **by 4 October**.

**What happens next:**
1. No separate cancellations are needed for the two duplicate holds. They reverse automatically within **“5 to 7 business days.”**
2. The remaining ₹12,999 hold is not overdue as of 30 September; its expected reversal date is 4 October.
3. If it still hasn’t reversed after 4 October, I can connect you with a human agent to investigate.

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
The debited amount is a temporary bank hold and will be released automatically. Since the payment failed, no order was created, so there’s nothing to cancel.

**Amount involved:** The failed-payment debit; you haven’t provided the amount.

1. Allow “5 to 7 business days” for a card or UPI hold to reverse. Net banking can take “up to 10” business days.
2. If it hasn’t reversed after that period, contact TechStore support with your bank reference number. TechStore will raise a chargeback trace with the payment gateway.

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
I understand why that’s frustrating. Under the “No-Cost EMI” terms, TechStore absorbs the interest as an upfront discount. If you return the order, that discount is deducted from your refund, and “the bank may still charge interest already levied”—so you may still have to pay that interest.

You must contact your bank to cancel the EMI plan.

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
Sorry, we can’t reissue the invoice for order #48750 to add your GSTIN. The policy states: “TechStore cannot add a GSTIN to an invoice afterwards and does not issue a fresh invoice for a completed order.”

Your existing invoice is downloadable from Orders. For future purchases, enter your GSTIN at checkout before placing the order.

I don't have information about your eligibility to claim input credit without the GSTIN on this invoice.

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

========== q035 [technical_api] ==========
QUESTION: A valid order ID returns 404 for my token but works in the dashboard. What is happening?
NEEDED DOCS: ['api_error_codes', 'api_auth']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
A **404** can mean “resource not found, including a valid order ID belonging to a different partner.” So the order may exist in the dashboard but belong to a different partner than the one associated with your token. A valid order ID alone doesn’t rule out a 404.

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
A faulty PulseBook may still qualify for warranty support even if its return window has ended.

- **Returns:** The **“30-day return window”** starts on the delivery date shown in tracking—not the purchase date. A return raised on day 31 or later is rejected automatically.
- **Warranty:** Warranty also starts from delivery and is **“independent of the 30-day return window.”** Manufacturing defects and component failure under normal use may qualify for repair or replacement even after returns close.
- **Exclusions:** Standard warranty does not cover physical damage, liquid ingress, unauthorised repair, or normal battery capacity decline above 80 percent of rated capacity.

I don't have information about your specific PulseBook’s warranty duration, delivery date, or fault, so I can’t confirm the two-year coverage or eligibility.

Please share your order number and describe the fault so we can clarify the next step.

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
No—the price match doesn’t apply to the X200 listing you found. Although 6 days is within the “within 7 days of their purchase” requirement, the policy states: “Price matching does not apply during flash sales or clearance events.”

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [pol_price_match] Price Match Guarantee
If a customer finds the identical product cheaper on a competing authorised Indian retailer within 7 days of their purchase, TechStore refunds the difference. The competing listing must be for a new, sealed unit sold and shipped by the retailer itself, not a marketplace seller. Price matching does not apply during flash sales or clearance events.
--- [bill_price_drop] Price Drop After Purchase
If a product's TechStore price drops within 7 days of purchase, the difference is refunded on request. This applies once per order line and does not apply during flash sales, festive events or clearance. This is distinct from the price match guarantee, which covers competitor pricing.
--- [pol_exchange] Exchange Policy
An exchange can be requested within 30 days of delivery for a different size, colour or variant of the same product line, subject to stock. If the new variant costs more, the difference is charged before dispatch. If it costs less, the difference is refunded. Only one exchange is permitted per order line.

========== q054 [simple_faq] ==========
QUESTION: How much is shipping on a ₹500 order?
NEEDED DOCS: ['ship_charges']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Shipping on a ₹500 order is ₹79, under the “Below that a flat ₹79 delivery charge applies” policy.

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
Try these steps to improve your smartwatch’s pulse readings:

1. Wear it one finger-width above your wrist bone, snug but not tight, so the sensor has firm skin contact.
2. Check whether the sensor sits over a tattoo or your skin is very cold—both can reduce accuracy.
3. After adjusting the fit, stay stationary and check the readings again.

If the readings remain implausible while stationary after adjusting the fit, this is a “warranty defect.” Which smartwatch model do you have?

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_watch_inaccurate_hr] Heart Rate Readings Inaccurate
Optical heart-rate sensors need firm skin contact. Wear the watch one finger-width above the wrist bone, snug but not tight. Tattoos, very cold skin and loose fits all reduce accuracy. If readings remain implausible when stationary after adjusting fit, the sensor is a warranty defect.
--- [prod_aurawatch_pro] AuraWatch Pro Smartwatch
Premium fitness smartwatch. Price ₹15,999. 1.5-inch AMOLED always-on display, 18-day battery, ECG and SpO2 sensors, dual-band GPS, 10 ATM water resistance, offline maps, 100 sport modes. Compatible with Android 10 and above and iOS 15 and above. 2-year manufacturer warranty. Non-returnable once used, under the hygiene policy.
--- [prod_aurawatch3] AuraWatch 3 Smartwatch
Fitness smartwatch. Price ₹8,999. 1.4-inch AMOLED display, 14-day battery, heart-rate and SpO2 sensors, built-in GPS, 5 ATM water resistance, sleep tracking. Compatible with Android 9 and above and iOS 14 and above. 1-year manufacturer warranty. Worn on the wrist, therefore non-returnable once used, under the hygiene policy.
--- [tsg_watch_sync] Smartwatch Not Syncing
If AuraWatch 3 will not sync: confirm the companion app has Bluetooth and background-activity permission, confirm the phone runs Android 9 or later or iOS 14 or later, force-close and reopen the app, and ensure the watch firmware is current. Battery optimisation settings on some Android phones stop the app in the background and are the most common cause; exclude the app from optimisation.

========== q057 [billing_dispute] ==========
QUESTION: I paid twice by mistake for the same thing
NEEDED DOCS: ['bill_duplicate_charge']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
I’m sorry about the double payment. If you submitted the payment page twice, only one order is created; the extra authorisation is a hold that reverses automatically within **“5 to 7 business days.”** If two separate orders were created, each must be cancelled and refunded separately.

To identify which applies and work out the reversal dates, please share:
- The date and amount of each charge.
- Any order numbers you received.

EVIDENCE THE MODEL WAS GIVEN:
--- [bill_duplicate_charge] Duplicate or Multiple Charges
A duplicate charge occurs when a payment page is submitted more than once. Only one order is created; the additional authorisations are holds that reverse automatically within 5 to 7 business days. If two or more distinct orders were created, each must be cancelled separately and each refund is processed separately, so a customer may see refunds arrive on different days. When resolving a multi-charge dispute, list every charge with its date and amount, state which one corresponds to the surviving order, and give the expected reversal date for each of the others.
--- [bill_chargeback] Bank Chargebacks and Disputes
If a customer raises a chargeback with their bank, the order is frozen and any parallel TechStore refund is suspended to prevent a double credit. Chargebacks take 45 to 90 days to resolve through the card network. Contacting support directly is almost always faster than a chargeback, and support can withdraw a chargeback by providing the bank with resolution evidence.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [bill_failed_payment] Payment Failed but Money Debited
If a payment fails but the amount is debited, the bank has placed a temporary hold that is released automatically. Card and UPI holds reverse within 5 to 7 business days; net banking can take up to 10. No order is created for a failed payment, so there is nothing to cancel. If the amount has not reversed after the stated period, contact support with the bank reference number and TechStore raises a chargeback trace with the payment gateway.

========== q059 [simple_faq] ==========
QUESTION: Do you deliver to Dubai?
NEEDED DOCS: ['ship_international']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No. TechStore “ships within India only,” so we can’t deliver to Dubai.

EVIDENCE THE MODEL WAS GIVEN:
--- [ship_international] International Shipping
TechStore ships within India only. We do not ship to international addresses and cannot deliver to APO or diplomatic addresses. Orders placed with an international billing address but an Indian delivery address are accepted.
--- [ship_open_box] Open-Box Delivery
Open-box delivery is available in 22 cities on orders above ₹20,000. The courier opens the package in the customer's presence for inspection before handover. Refusal at open-box inspection is free and refunds process within 5 to 7 business days. Open-box delivery adds 1 business day to the estimate.
--- [ship_charges] Delivery Charges
Delivery is free on all orders above ₹999. Below that a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149 and is available in metro cities only for orders placed before 2 PM. Delivery charges are refunded if the order is cancelled before shipping or if the item arrives damaged.
--- [acc_address] Changing a Delivery Address
The delivery address can be changed from Orders until the order is marked Shipped. After dispatch the address cannot be changed, but delivery can be rescheduled once through the courier tracking link. Changing the address to a different pin code after dispatch is not possible; the order must be refused and reordered.

========== q061 [simple_faq] ==========
QUESTION: How can I make my login safer with a code on my phone?
NEEDED DOCS: ['acc_two_factor']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
You can enable **two-factor authentication (2FA)** to add a code from your phone when signing in:

1. Open **Security** in your TechStore account.
2. Enable 2FA using an **authenticator app or SMS**.

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
No—the 2-year warranty does not restart. Under “Warranty on Replaced Units,” the replacement “inherits the remaining warranty of the original.”

If fewer than 90 days remain, the replacement carries “90 days from the replacement date.”

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
That sounds like a **429 rate-limit error**. TechStore’s Partner API limits are “600 requests per minute per token” and “60 per minute for the bulk export endpoints.”

1. Check the response’s `Retry-After` header and wait the specified number of seconds before retrying.
2. Use exponential backoff with jitter for subsequent retries—avoid retrying immediately in a tight loop.
3. Reduce your request rate to stay within the applicable limit. “Sustained violation for more than 15 minutes” results in a “temporary 1-hour block.”

Are you using the bulk export endpoints, and what `Retry-After` value are you receiving?

EVIDENCE THE MODEL WAS GIVEN:
--- [api_rate_limits] API Rate Limits and 429 Errors
The Partner API allows 600 requests per minute per token, and 60 per minute for the bulk export endpoints. Exceeding the limit returns 429 with a Retry-After header in seconds. Clients should honour Retry-After and use exponential backoff with jitter. Sustained violation for more than 15 minutes results in a temporary 1-hour block.
--- [api_timeouts] API Timeouts and Retry Safety
Requests time out server side at 30 seconds. A timeout does not indicate whether the operation completed, so POST requests must be retried with the same Idempotency-Key to avoid duplicates. GET, PUT and DELETE are idempotent by design and safe to retry. Retries should use exponential backoff with jitter; retrying immediately in a tight loop triggers rate limiting.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_idempotency] API Idempotency
All POST endpoints accept an Idempotency-Key header. A repeated request with the same key and an identical payload returns the original response without creating a second resource. A repeated key with a different payload returns 409. Keys are retained for 24 hours. Clients should generate a UUID per logical operation, not per HTTP attempt, so that retries reuse the same key.
