# Merchant setup

1. Install the SIMcloud Shopify app through an approved installation route when available. App Store review is still pending; there is no public marketplace install listing yet.
2. Connect your SIMcloud account through the app's private merchant interface. Never put an API token in theme code, a product field or a public GitHub issue.
3. Import the available catalogue through the app. Review product names, prices and images before opening sales.
4. Open **Online Store → Themes → Customize**, choose the prepaid product template, add the **SIMcloud prepaid details** app block and save.
5. Confirm airtime/data products collect a recipient number and electricity products collect both recipient and meter. Verify those values appear in the cart and order.
6. Complete the operator's connected-store acceptance process before authorizing live fulfilment.

This repository supplies the storefront block. The hosted app supplies merchant configuration, catalogue import and fulfilment. Merchant instructions must never expose server configuration or operational evidence.
