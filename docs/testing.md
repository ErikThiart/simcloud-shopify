# Extension testing

Run `npm ci`, `npx playwright install chromium`, and `npm test`. The browser checks mount the actual extension JavaScript and stylesheet into a synthetic Shopify-shaped product form, verify quantity restrictions and field submission, and reject invalid recipient input. No live shop, payment or prepaid provider is contacted.

Run `python3 scripts/public_check.py` and `python3 scripts/package.py` to check the public boundary and explicit release contents. Build the theme extension with Shopify CLI.

Connected merchant acceptance is a separate private process. Passing these tests does not prove payment verification, provider fulfilment or App Store approval.
