const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
(async () => {
  const root = path.resolve(__dirname, '..');
  const browser = await chromium.launch({ headless: true, ...(process.env.SC_BROWSER_PATH ? { executablePath: process.env.SC_BROWSER_PATH } : {}) });
  let checks = 0;
  try {
    const page = await browser.newPage({ viewport: { width: 1100, height: 900 } });
    const failures = []; page.on('pageerror', error => failures.push(error.message));
    // Mount the actual extension JS in a synthetic Dawn-shaped product form.
    await page.setContent(`<html><head><style>body{font:16px system-ui;max-width:720px;margin:40px auto;padding:20px}h1{color:#20392f}button{padding:12px 20px;background:#376b50;color:white;border:0;border-radius:5px}</style></head><body><p>DEMONSTRATION · SYNTHETIC PRODUCT</p><h1>Prepaid electricity — R100.00</h1><div class="shopify-section" id="shopify-section-demo"><form action="/cart/add" id="product-form-demo"><input name="id" value="1" type="hidden"><label>Quantity <input name="quantity" value="2" type="number"></label><button type="submit">Add to cart</button></form><div class="shopify-payment-button">Accelerated checkout</div><div class="simcloud-details" data-simcloud-details data-product-id="1"><strong>Prepaid delivery details</strong><label for="phone">South African recipient number</label><input id="phone" type="tel" name="properties[SIMcloud recipient]" required data-simcloud-input placeholder="082 123 4567"><label for="meter">Prepaid electricity meter number</label><input id="meter" name="properties[SIMcloud meter]" required pattern="[a-zA-Z0-9]{1,50}" data-simcloud-input><p>One prepaid item per line. Check your details before paying. Delivery details are sent to your checkout email.</p><p hidden role="alert" data-simcloud-error></p></div></div></body></html>`);
    await page.addStyleTag({ content: fs.readFileSync(path.join(root, 'extensions/prepaid-details/assets/prepaid-details.css'), 'utf8') });
    await page.addScriptTag({ content: fs.readFileSync(path.join(root, 'extensions/prepaid-details/assets/prepaid-details.js'), 'utf8') });
    assert.equal(await page.locator('[name=quantity]').inputValue(), '1'); checks++;
    assert.equal(await page.locator('.shopify-payment-button').isVisible(), false); checks++;
    await page.locator('#phone').fill('082 123 4567'); await page.locator('#meter').fill('00123456789');
    const data = await page.locator('form').evaluate((form) => Object.fromEntries(new FormData(form)));
    assert.equal(data['properties[SIMcloud recipient]'], '082 123 4567', JSON.stringify(data));
    assert.equal(data['properties[SIMcloud meter]'], '00123456789'); checks += 2;
    await page.locator('form').evaluate((form) => form.addEventListener('submit', (event) => { event.preventDefault(); window.validSubmitReached = true; }));
    await page.locator('#phone').fill('invalid-number'); await page.getByRole('button', { name: 'Add to cart' }).click();
    assert.equal(await page.evaluate(() => window.validSubmitReached === true), false); checks++;
    await page.locator('#phone').fill('082 123 4567'); await page.getByRole('button', { name: 'Add to cart' }).click();
    assert.equal(await page.evaluate(() => window.validSubmitReached), true); checks++;
    assert.deepEqual(failures, []); checks++;
    console.log(`${checks} storefront checks passed with synthetic content and no provider calls.`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
