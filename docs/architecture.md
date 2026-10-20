# Public extension boundary

| Component | Responsibility | Source location |
|---|---|---|
| Theme app block | Recipient and meter fields | This repository |
| Browser JavaScript | Form validation and cart properties | This repository |
| Shopify | Products, cart, checkout and orders | Shopify platform |
| Hosted SIMcloud service | Merchant authorization, product imports and fulfilment | Private service |

The extension contains no server runtime or merchant credentials. A browser cannot authorize wallet spending. Hosted processing independently verifies Shopify order/payment state and SIMcloud account authorization. Server internals and deployment instructions are intentionally excluded from public source and packages.
