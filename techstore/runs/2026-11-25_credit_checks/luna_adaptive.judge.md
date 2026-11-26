# Answers to grade

Grade each answer ONLY against the evidence shown with it. Store date: 30 September 2026.
Verdicts: correct / partial / wrong / hallucinated (rubric: Tokenomics.md §7, Grading Rubric).


========== q001 [simple_faq] ==========
QUESTION: How long do I have to return something?
NEEDED DOCS: ['pol_return_window']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
You can return an item within the **30-day return window**, counted from the delivery date shown on the tracking record—not the order date. It must be in its original packaging with all accessories, manuals, and free gifts included. A return raised on day 31 or later is rejected automatically.

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
Delivery is free on orders above ₹999. Orders below ₹999 have a ₹79 delivery charge; express next-day delivery costs ₹149 where available.

EVIDENCE THE MODEL WAS GIVEN:
--- [ship_charges] Delivery Charges
Delivery is free on all orders above ₹999. Below that a flat ₹79 delivery charge applies. Express next-day delivery costs ₹149 and is available in metro cities only for orders placed before 2 PM. Delivery charges are refunded if the order is cancelled before shipping or if the item arrives damaged.
--- [ship_open_box] Open-Box Delivery
Open-box delivery is available in 22 cities on orders above ₹20,000. The courier opens the package in the customer's presence for inspection before handover. Refusal at open-box inspection is free and refunds process within 5 to 7 business days. Open-box delivery adds 1 business day to the estimate.
--- [pol_damaged_in_transit] Damaged or Wrong Item Delivered
If an item arrives damaged, or the wrong item is delivered, report it within 48 hours of delivery with photographs of the package and product. TechStore arranges a free replacement pickup and dispatches the correct item immediately. No return shipping charge applies and the 30-day window does not limit this remedy.
--- [bill_payment_methods] Accepted Payment Methods
TechStore accepts UPI, credit and debit cards from all major Indian issuers, net banking from 40 partner banks, and cash on delivery for orders up to ₹20,000. Wallet payments and international cards are not accepted. Cash on delivery carries a ₹49 handling fee which is refunded if the order is cancelled before dispatch.

========== q007 [order_status] ==========
QUESTION: Has order 48390 shipped yet?
NEEDED DOCS: ['ship_tracking']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No. Order #48390 is still processing and has not shipped yet.

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
Order #48677 is estimated to arrive on 30 September 2026.

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

========== q015 [product_info] ==========
QUESTION: Is the NovaTab 11 stylus included?
NEEDED DOCS: ['prod_novatab11']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No. The NovaTab 11 stylus is sold separately for ₹4,999.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_novatab11] NovaTab 11 Tablet
11-inch Android tablet. Price ₹29,999. Snapdragon 7 Gen 3, 8 GB RAM, 256 GB storage expandable by microSD, 11-inch 2.5K LCD at 120 Hz, 8000 mAh battery, stylus supported and sold separately at ₹4,999. 1-year manufacturer warranty.
--- [prod_novatab_mini8] NovaTab Mini 8 Tablet
8-inch compact Android tablet. Price ₹17,999. Snapdragon 6 Gen 1, 6 GB RAM, 128 GB storage expandable by microSD, 8.4-inch 1920x1200 LCD at 90 Hz, 5500 mAh battery. Stylus is not supported on the Mini 8; stylus support is exclusive to the NovaTab 11. 1-year manufacturer warranty.

========== q016 [product_comparison] ==========
QUESTION: X200 or Y500 for a noisy open-plan office?
NEEDED DOCS: ['prod_x200', 'prod_y500']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
The SoundWave Y500 is the better choice for a noisy open-plan office. It has adaptive noise cancellation rated at 45 dB, compared with 35 dB on the X200, and is specifically recommended for noisy environments. The Y500 costs ₹24,999; the X200 costs ₹12,999.

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
For video editing, the **PulseBook Pro 16 has a stronger spec sheet**: 32 GB RAM, an Intel Core Ultra 9, discrete RTX 4060 graphics, and a 1 TB SSD. The PulseBook 14 has 16 GB RAM, an Intel Core Ultra 5, integrated graphics not specified in the listing, and a 512 GB SSD.

The Pro 16 costs ₹1,34,999 versus ₹64,999—about 2.08 times as much—and is heavier at 1.95 kg versus 1.29 kg. If you edit demanding projects, its extra memory, graphics hardware, and storage may make the price worthwhile; for lighter editing, the PulseBook 14 may be the better value.

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
No. The VoltCharge 65W is not sufficient to charge the PulseBook Pro 16 properly; it may charge very slowly or not at all. The laptop needs a 100W charger for full-speed charging. The VoltCharge 100W is ₹3,999.

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
The SoundWave X200 is lighter at 250 g, compared with 268 g for the Y500—a difference of 18 g. For long flights, the Y500 is recommended for noisy environments and offers stronger ANC (45 dB vs. 35 dB) and longer battery life (60 vs. 40 hours), so the extra weight may be a worthwhile trade-off.

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
For a lightweight college setup under ₹1 lakh, I’d recommend:

- **NovaTab Mini 8** — ₹17,999; its compact 8.4-inch screen makes it easy to carry for reading.
- **PulseBook Air 13** — ₹44,999; it weighs 1.12 kg and has a 10-hour rated battery.

**Total: ₹62,998.**

If you’d prefer a larger tablet screen, the **NovaTab 11** plus the Air 13 would total **₹74,998**. The NovaTab 11 also supports a separately sold stylus, but the Mini 8 does not.

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

1. Hold the power button for 7 seconds, until the LED flashes blue and white.
2. In your phone’s Bluetooth settings, forget any existing SoundWave entry.
3. Turn Bluetooth off for 10 seconds, turn it back on, then select the headphones.
4. If multipoint is active, disconnect the headphones from any other device first.
5. If the LED doesn’t flash, charge the headphones for 30 minutes and retry.

I don't have information about your headphone brand or model, so these steps may not apply to your headphones.

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_headphone_pairing] Headphones Will Not Pair
If SoundWave headphones will not pair: 1) Hold the power button for 7 seconds until the LED flashes blue and white, which puts the unit in pairing mode. 2) On the phone, forget any existing SoundWave entry in Bluetooth settings. 3) Disable Bluetooth for 10 seconds, re-enable, and select the device. 4) If multipoint is active the headphones may already be connected to another device; disconnect there first. 5) If the LED does not flash at all, charge for 30 minutes and retry.

========== q025 [troubleshooting] ==========
QUESTION: My headphone battery drains much faster than advertised.
NEEDED DOCS: ['tsg_headphone_battery', 'pol_warranty_terms']   MISSING FROM WHAT THE MODEL SAW: ['pol_warranty_terms']

ANSWER:
Sorry—that’s frustrating. If these are SoundWave headphones, try:

1. Turn off active noise cancellation (ANC); it can reduce rated battery life by roughly 30%.
2. Check for firmware updates in the SoundWave app.
3. Disable multipoint if you don’t need two devices connected.
4. Confirm the headphones power off when removed rather than staying idle.
5. With ANC off, if runtime is below 50% of the rated figure, the battery is considered defective and covered under warranty.

I don't have information about your headphone model or its rated battery life.

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_headphone_battery] Headphone Battery Draining Fast
Rapid battery drain on SoundWave headphones is usually caused by active noise cancellation combined with high volume. ANC reduces rated battery life by roughly 30 percent. Check for firmware updates in the SoundWave app, disable multipoint if two devices are not needed, and confirm the unit powers off rather than idling when removed. If runtime is below 50 percent of the rated figure with ANC off, the battery is considered defective and covered under warranty.

========== q026 [billing_dispute] ==========
QUESTION: I was charged 12,999 three times for order 48712. Two were supposed to be cancelled but I only see one refund. Where is my money?
NEEDED DOCS: ['bill_duplicate_charge', 'pol_refund_timeline']   MISSING FROM WHAT THE MODEL SAW: ['pol_refund_timeline']

ANSWER:
I’m sorry for the confusion. For order #48712, the three ₹12,999 entries are:

- **27 September 2026 — ₹12,999, settled:** This is the charge for the order.
- **27 September 2026 — ₹12,999, authorization reversed:** This duplicate hold was released on **29 September 2026**.
- **27 September 2026 — ₹12,999, authorization pending reversal:** This duplicate hold is due to reverse by **4 October 2026**.

So, only one charge is for the order; the other two are duplicate authorization holds, not separate order charges. One has been reversed, and the remaining hold is still pending.

1. Allow until **4 October 2026** for the pending reversal.
2. If it hasn’t reversed by then, contact support so they can investigate.

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

========== q028 [billing_dispute] ==========
QUESTION: I returned one item from a two-item order but my refund is less than the item price. Why?
NEEDED DOCS: ['bill_refund_partial']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
For a partial return, the refund covers the returned item’s value, but the delivery charge is refunded only if you return the entire order. Also, if your order had a minimum-basket promotional discount and the remaining item(s) fall below that minimum, the discount is recalculated and the difference is deducted from your refund.

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
When a no-cost EMI order is returned, the no-cost EMI discount is deducted from your refund, and the bank may still charge interest already levied. Contact your bank to cancel the EMI plan. I don't have information about who ultimately pays interest already charged by the bank.

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
I’m sorry, but TechStore cannot add a GSTIN to an invoice afterwards and does not issue a fresh invoice for a completed order. You can download the existing invoice from Orders; invoices remain available for 8 years.

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
Your code signs a re-serialized JSON body, not the exact raw request bytes. JSON key order and whitespace can change during re-serialization, which changes the HMAC.

1. Compute the HMAC over the exact raw request body **before** parsing it as JSON.
2. Use the webhook secret as the HMAC key, not your API token.

EVIDENCE THE MODEL WAS GIVEN:
--- [api_webhook_signature] Webhook Signature Verification and 403 Errors
Every webhook carries an X-TechStore-Signature header containing an HMAC-SHA256 of the raw request body, keyed with the webhook secret, hex encoded. A 403 returned by our delivery checker almost always means the signature was computed over a parsed and re-serialised body rather than the raw bytes; JSON re-serialisation changes key order and whitespace and therefore changes the HMAC. Compute the HMAC over the exact raw body before any JSON parsing. The second most common cause is using the API token instead of the webhook secret as the HMAC key.

========== q032 [technical_api] ==========
QUESTION: I am getting 409 on order creation when I retry after a timeout. What am I doing wrong?
NEEDED DOCS: ['api_idempotency', 'api_error_codes']   MISSING FROM WHAT THE MODEL SAW: ['api_idempotency']

ANSWER:
A timeout doesn’t tell you whether the order was created. Retry the POST with the **same Idempotency-Key and the exact same payload**. A 409 means that key was reused with a different payload. Don’t retry with a modified request under the same key.

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
Sandbox and production use separate credentials. A sandbox token is rejected by production—the most common cause of this 401.

Check that your production request uses `Authorization: Bearer <token>` with a production-issued token, and that it isn’t missing, malformed, or expired. Tokens expire 90 days after issue.

EVIDENCE THE MODEL WAS GIVEN:
--- [api_auth] API Authentication and 401 Errors
Authenticate with Authorization: Bearer <token>. A 401 means the token is missing, malformed, expired or from the wrong environment; sandbox tokens rejected by production is the most common cause. Tokens expire 90 days after issue and can be rotated in the dashboard without downtime, since the previous token stays valid for 24 hours after rotation.
--- [api_sandbox] Sandbox Environment
Sandbox runs at https://sandbox.techstore.example/v1 with separate credentials and synthetic data that resets nightly at 02:00 IST. Sandbox order IDs begin with a 9; production IDs do not. Webhooks fire in sandbox but use a separate signing secret. Sandbox has no rate limit but is not performance representative.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_overview] TechStore Partner API Overview
The Partner API is a REST API at https://api.techstore.example/v1. All requests require an Authorization header with a bearer token issued in the partner dashboard. Requests and responses are JSON. The API exposes orders, inventory, shipments and webhooks. Sandbox is available at https://sandbox.techstore.example/v1 with separate credentials and synthetic data.

========== q035 [technical_api] ==========
QUESTION: A valid order ID returns 404 for my token but works in the dashboard. What is happening?
NEEDED DOCS: ['api_error_codes', 'api_auth']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
A 404 can mean the order belongs to a different partner, even if the order ID is valid. I don't have information about why the dashboard can access it while your token cannot.

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
The **30-day return window** is counted from the delivery date on your tracking record, not the purchase date. A return raised on day 31 or later is rejected automatically.

The warranty is separate from the return window. It covers manufacturing defects and component failure under normal use for the period stated on the product page, counted from delivery—even if the return window has passed.

I don't have information about whether your PulseBook’s manufacturer warranty is 2 years; the warranty duration is the one stated on its product page.

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
I’m sorry your Y500 headphones are defective. Although they’re **“non-returnable once the seal is broken,”** the hygiene exclusion does not remove your warranty rights; faulty headphones remain covered by the 2-year manufacturer warranty.

I don't have information about how to start a warranty claim.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_y500] SoundWave Y500 Premium Headphones
Flagship over-ear wireless headphones. Price ₹24,999. 60-hour battery life, Bluetooth 5.4, adaptive active noise cancellation rated at 45 dB with transparency mode, LDAC and aptX Lossless support, USB-C and wireless charging, multipoint pairing with three devices, 268 g, memory-foam earcups. Available in Graphite and Sand. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy. Recommended over the X200 for noisy environments such as open-plan offices and flights.
--- [pol_return_exclusions] Non-Returnable Items
For hygiene reasons the following are non-returnable once the seal is broken: headphones of every type (over-ear, on-ear and in-ear), earbuds, fitness bands worn on the wrist, and any personal grooming device. Opened software licences and redeemed digital gift cards are also non-returnable. These items remain covered by warranty if they are faulty; a hygiene exclusion never removes warranty rights.
--- [tsg_headphone_pairing] Headphones Will Not Pair
If SoundWave headphones will not pair: 1) Hold the power button for 7 seconds until the LED flashes blue and white, which puts the unit in pairing mode. 2) On the phone, forget any existing SoundWave entry in Bluetooth settings. 3) Disable Bluetooth for 10 seconds, re-enable, and select the device. 4) If multipoint is active the headphones may already be connected to another device; disconnect there first. 5) If the LED does not flash at all, charge for 30 minutes and retry.
--- [tsg_earbuds_one_side] Only One Earbud Working
If only one SoundWave earbud plays: 1) Place both buds in the case, close the lid for 10 seconds and reopen. 2) Forget the device in phone Bluetooth settings and re-pair. 3) Reset the buds by holding both touch panels for 15 seconds until the LED flashes red and white. 4) Clean the charging contacts on the silent bud with a dry cloth; contact dirt is the most common cause. 5) If the silent bud still does not charge, it is a warranty defect.

========== q039 [policy_edge_case] ==========
QUESTION: The courier failed three delivery attempts while I was travelling and the order was returned. I was not told. Do I get a full refund including the delivery charge?
NEEDED DOCS: ['ship_failed_delivery', 'ship_charges']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
Yes. After the third failed attempt, the parcel is returned to the warehouse, and the order is refunded in full, including any delivery charge paid, **within 7 business days of the parcel being received back**.

I don't have information about whether you should have been notified about the failed attempts or return.

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
No. The **Price Match Guarantee** applies within the “7 days” after purchase, but excludes competing prices during clearance events.

EVIDENCE THE MODEL WAS GIVEN:
--- [prod_x200] SoundWave X200 Wireless Headphones
Over-ear wireless headphones. Price ₹12,999. 40-hour battery life, Bluetooth 5.3, hybrid active noise cancellation rated at 35 dB, USB-C fast charge giving 5 hours from a 10-minute charge, multipoint pairing with two devices, 250 g. Available in Midnight Black and Arctic White. 2-year manufacturer warranty. Non-returnable once the seal is opened, under the hygiene policy.
--- [pol_price_match] Price Match Guarantee
If a customer finds the identical product cheaper on a competing authorised Indian retailer within 7 days of their purchase, TechStore refunds the difference. The competing listing must be for a new, sealed unit sold and shipped by the retailer itself, not a marketplace seller. Price matching does not apply during flash sales or clearance events.
--- [bill_price_drop] Price Drop After Purchase
If a product's TechStore price drops within 7 days of purchase, the difference is refunded on request. This applies once per order line and does not apply during flash sales, festive events or clearance. This is distinct from the price match guarantee, which covers competitor pricing.

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
I don't have that information. I can connect you with a human agent who can help. I can also help with TechStore products, orders, and support.

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
No. TechStore does not sell washing machines.

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
I can only help with TechStore orders, products, and support. TechStore is online-only and has no physical stores or showrooms. Support is available by chat and email from 9 AM to 9 PM IST, seven days a week.

EVIDENCE THE MODEL WAS GIVEN:
--- [about_techstore] About TechStore
TechStore is an online-only consumer electronics retailer in India. It has no physical retail stores or showrooms, so there are no store opening hours; orders are placed only on the TechStore website and app. TechStore sells six product families: headphones and earbuds (SoundWave), laptops (PulseBook), tablets (NovaTab), smartwatches (AuraWatch), monitors (ClearView), and chargers and power banks (VoltCharge, VoltBank). TechStore does not sell mobile phones, televisions, cameras, gaming consoles, or home appliances such as washing machines, refrigerators, or air conditioners. Repairs are handled at authorised service centres in 48 cities. Customer support is available by chat and email from 9 AM to 9 PM IST, seven days a week.
--- [pol_bulk_orders] Bulk and Business Orders
Orders above 10 units of a single SKU are treated as business orders and require a GSTIN. Bulk pricing is quoted by the business desk and is not available at checkout. Business orders ship in 5 to 10 business days and carry a 15-day return window rather than 30 days.
--- [ship_open_box] Open-Box Delivery
Open-box delivery is available in 22 cities on orders above ₹20,000. The courier opens the package in the customer's presence for inspection before handover. Refusal at open-box inspection is free and refunds process within 5 to 7 business days. Open-box delivery adds 1 business day to the estimate.
--- [svc_centres] Service Centre Network
TechStore operates authorised service centres in 48 Indian cities. The nearest centre can be found by pin code on the Support page. Walk-in service is available for laptops and monitors; headphones, watches and tablets are handled by courier pickup only. Carry the invoice or order ID for any walk-in visit.

========== q051 [simple_faq] ==========
QUESTION: What's the last day I can send an item back?
NEEDED DOCS: ['pol_return_window']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
TechStore accepts returns within the **“30-day return window,”** counted from the delivery date shown in the tracking record—not the order date. A return raised on day 31 or later is rejected automatically. I don't have information about your delivery date, so I can’t calculate the calendar deadline.

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
If they’re earbuds, they’re non-returnable once the seal is broken for hygiene reasons. If they’re faulty, they remain covered by warranty. I don't have information about whether your specific type of earphones is classified as earbuds.

EVIDENCE THE MODEL WAS GIVEN:
--- [pol_return_exclusions] Non-Returnable Items
For hygiene reasons the following are non-returnable once the seal is broken: headphones of every type (over-ear, on-ear and in-ear), earbuds, fitness bands worn on the wrist, and any personal grooming device. Opened software licences and redeemed digital gift cards are also non-returnable. These items remain covered by warranty if they are faulty; a hygiene exclusion never removes warranty rights.

========== q057 [billing_dispute] ==========
QUESTION: I paid twice by mistake for the same thing
NEEDED DOCS: ['bill_duplicate_charge']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
If the payment page was submitted more than once, only one order is created; the extra authorisations are holds that reverse automatically within 5 to 7 business days. If two separate orders were created, each must be cancelled separately, and the refunds may arrive on different days.

I don't have information about your charge dates, amounts, or whether one or two orders were created. Please share those details so I can guide you.

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
Your company’s GSTIN must be entered at checkout before placing the order. TechStore cannot add a GSTIN to an invoice afterwards and does not issue a fresh invoice for a completed order.

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
TechStore ships within India only, so we can’t deliver to Dubai.

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
1. Make sure the vents are unobstructed, and don’t use the laptop on fabric.
2. Clean the intake grilles with compressed air.
3. Update the BIOS.

Surface temperatures up to 45°C under sustained load are within specification. If it shuts down under light load, a fan or sensor fault may be covered by warranty.

EVIDENCE THE MODEL WAS GIVEN:
--- [tsg_laptop_overheating] Laptop Overheating
Surface temperatures up to 45 C under sustained load are within specification. If the machine thermally throttles or shuts down: ensure the vents are unobstructed and not used on fabric, clean the intake grilles with compressed air, and update the BIOS. Shutdowns under light load indicate a fan or sensor fault and are covered by warranty.

========== q062 [policy_edge_case] ==========
QUESTION: If my headphones get replaced, does the 2 year cover restart?
NEEDED DOCS: ['pol_replacement_warranty']   MISSING FROM WHAT THE MODEL SAW: []

ANSWER:
No. A replacement inherits the remaining warranty of the original; it doesn’t restart the full term. If fewer than 90 days remain, the replacement gets 90 days from the replacement date.

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
You’re hitting the API rate limit. It allows **600 requests per minute per token**, or **60 per minute for bulk export endpoints**.

When you receive a **429**, wait for the number of seconds in the `Retry-After` header, then retry using **exponential backoff with jitter**. Avoid retrying immediately in a tight loop. If the limit is exceeded for more than 15 minutes, the token is temporarily blocked for 1 hour.

EVIDENCE THE MODEL WAS GIVEN:
--- [api_rate_limits] API Rate Limits and 429 Errors
The Partner API allows 600 requests per minute per token, and 60 per minute for the bulk export endpoints. Exceeding the limit returns 429 with a Retry-After header in seconds. Clients should honour Retry-After and use exponential backoff with jitter. Sustained violation for more than 15 minutes results in a temporary 1-hour block.
--- [api_timeouts] API Timeouts and Retry Safety
Requests time out server side at 30 seconds. A timeout does not indicate whether the operation completed, so POST requests must be retried with the same Idempotency-Key to avoid duplicates. GET, PUT and DELETE are idempotent by design and safe to retry. Retries should use exponential backoff with jitter; retrying immediately in a tight loop triggers rate limiting.
--- [api_error_codes] API Error Codes
400 invalid request body or missing required field. 401 authentication failed. 403 signature verification failed or the token lacks the required scope. 404 resource not found, including a valid order ID belonging to a different partner. 409 idempotency conflict, meaning the same Idempotency-Key was reused with a different payload. 422 the request was well formed but semantically rejected, such as shipping to an unsupported pin code. 429 rate limited. 5xx a server error; retry with backoff.
--- [api_idempotency] API Idempotency
All POST endpoints accept an Idempotency-Key header. A repeated request with the same key and an identical payload returns the original response without creating a second resource. A repeated key with a different payload returns 409. Keys are retained for 24 hours. Clients should generate a UUID per logical operation, not per HTTP attempt, so that retries reuse the same key.
