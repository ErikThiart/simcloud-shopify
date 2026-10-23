# Merchant setup

1. Install the SIMcloud Shopify app through an approved installation route when available. App Store review is still pending; there is no public marketplace install listing yet.
2. Connect your SIMcloud account through the app's private merchant interface. Never put an API token in theme code, a product field or a public GitHub issue.
3. Import the available catalogue through the app. Review product names, prices and images before opening sales.
4. Open **Online Store → Themes → Customize**, choose the prepaid product template, add the **SIMcloud prepaid details** app block and save.
5. Confirm airtime/data products collect a recipient number and electricity products collect both recipient and meter. Verify those values appear in the cart and order.
6. Complete the operator's connected-store acceptance process before authorizing live fulfilment.

This repository supplies the storefront block. The hosted app supplies merchant configuration, catalogue import and fulfilment. Merchant instructions must never expose server configuration or operational evidence.

## Add the recipient fields without editing theme code

Use an Online Store 2.0 theme that supports app blocks. Vintage themes are unsupported.

1. Open **Online Store → Themes → Edit theme** (or **Customize**).
2. Select **Products → Default product**, or the template assigned to your prepaid products.
3. Expand **Product information**. In Horizon, also expand **Details**.
4. Above **Buy buttons**, choose **Add block → Apps → SIMcloud prepaid details**.
5. Save. The block has no settings: airtime/data ask for a recipient, electricity asks for a recipient and meter, and vouchers use the checkout email.
6. Repeat for every template used by prepaid products.

Drag the block to change its position. To remove it, select it and choose **Remove block**, then save.

## Check every route to checkout

Disable any quick-add, sticky purchase bar or accelerated-checkout path that bypasses the recipient fields. In Horizon, turn off **Product information → Sticky add to cart bar**, hide **Buy buttons → Accelerated checkout**, and turn off **Theme settings → Product cards → Quick add**. Check mobile quick add as well.

Preview a mobile product and an electricity product. Empty required fields must block **Add to cart**. Enter test details and check that **SIMcloud recipient** and, for electricity, **SIMcloud meter** appear in the cart and checkout. Check quantity remains one per prepaid line. Voucher products show a notice that private delivery goes to the checkout email.

Repeat these checks after changing your theme, cart app or product templates. A successful cart test does not establish provider delivery. Shopify test orders cannot spend a real SIMcloud wallet; keep fulfilment paused until the operator's connected acceptance checks are complete.
