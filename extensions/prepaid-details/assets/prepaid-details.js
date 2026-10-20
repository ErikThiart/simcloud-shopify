/* GPL-2.0-or-later. Customer fields are untrusted and are checked again by the worker. */
(() => {
  function attach(root = document) {
    root.querySelectorAll('[data-simcloud-details]').forEach((block) => {
      if (block.dataset.attached) return;
      const section = block.closest('.shopify-section') || block.parentElement;
      const forms = [...section.querySelectorAll('form[action*="/cart/add"]')].filter((form) => form.querySelector('[name="id"]'));
      const form = forms.find((candidate) => candidate.getAttribute('id') === `product-form-${section.id.replace('shopify-section-', '')}`) || forms[0];
      const error = block.querySelector('[data-simcloud-error]');
      if (!form) {
        error.hidden = false;
        error.textContent = 'Delivery details could not connect to the product form. Please contact the store before ordering.';
        return;
      }
      // Shopify's input[name=id] shadows the form.id property in browser DOM APIs.
      const formId = form.getAttribute('id') || `simcloud-product-form-${block.dataset.productId}`;
      form.setAttribute('id', formId);
      block.dataset.attached = 'true';
      const inputs = [...block.querySelectorAll('[data-simcloud-input]')];
      inputs.forEach((input) => input.setAttribute('form', formId));
      // Dawn and themes using a normal product form or FormData(form) include associated inputs.
      // Custom AJAX carts require the documented compatibility test before enabling fulfillment.
      const quantity = section.querySelector('[name="quantity"]');
      if (quantity) { quantity.value = '1'; quantity.min = '1'; quantity.max = '1'; }
      form.addEventListener('submit', (event) => {
        error.hidden = true;
        const phone = inputs.find((input) => input.type === 'tel');
        if (phone) {
          const normalized = phone.value.replace(/[\s()-]/g, '');
          phone.setCustomValidity(/^(?:0|\+?27)[6-8]\d{8}$/.test(normalized) ? '' : 'Enter a valid South African mobile number.');
        }
        if (inputs.some((input) => !input.reportValidity()) || (quantity && quantity.value !== '1')) {
          event.preventDefault(); event.stopImmediatePropagation();
          error.hidden = false; error.textContent = 'Check your recipient details. Each prepaid item must have quantity one.';
        }
      }, true);
      inputs.forEach((input) => input.addEventListener('input', () => input.setCustomValidity('')));
      // Accelerated checkout can bypass required properties. Use the regular add-to-cart path.
      section.querySelectorAll('.shopify-payment-button').forEach((button) => { button.hidden = true; });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => attach());
  else attach();
  document.addEventListener('shopify:section:load', (event) => attach(event.target));
})();
