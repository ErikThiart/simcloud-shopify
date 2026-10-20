# Extension development

The theme extension lives in `extensions/prepaid-details/`. Liquid reads the `simcloud.service` product metafield to show the relevant fields. The supported service values are `airtime`, `data`, `vas`, and `electricity`.

The recipient is stored as `properties[SIMcloud recipient]`; the meter uses `properties[SIMcloud meter]`. Preserve those property names. A private fulfilment service consumes the resulting order details and validates them independently.

Use your own Shopify development app and store. `shopify.app.toml` is an unbound example for extension builds, not the production service configuration. Keep actual app bindings in ignored local TOML files. Never upload private service code to this repository.

Build with Shopify CLI using `shopify app build`. Deploy only to an app you control after reviewing its configuration. An extension build is not a full application installation or marketplace approval.
