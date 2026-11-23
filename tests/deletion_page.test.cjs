const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const path = require('node:path');
const {test} = require('node:test');
const vm = require('node:vm');

const source = readFileSync(path.join(__dirname, '../static/account-deletion/deletion.js'), 'utf8');
const tick = () => new Promise(resolve => setImmediate(resolve));

async function page() {
  const nodes = new Map();
  class Element extends EventTarget {
    hidden = false;
    value = '';
    focus() {}
    reset() { this.value = ''; }
  }
  function el(id) {
    if (!nodes.has(id)) nodes.set(id, new Element());
    return nodes.get(id);
  }
  const window = new EventTarget();
  const pending = [];
  async function fetch(url) {
    const data = url.endsWith('/config')
      ? {available: true, email_required: false, reauthentication_methods: ['password', 'access_key']}
      : await new Promise(resolve => pending.push(resolve));
    return {ok: Boolean(data), status: data ? 200 : 401, json: async () => data};
  }
  vm.runInNewContext(source, {
    window, document: {getElementById: el, querySelectorAll: () => []}, fetch,
    location: {hash: ''}, URLSearchParams, setTimeout, clearTimeout, AbortController,
  });
  await tick();
  return {el, window, pending};
}

const proof = {request_id: 'daw_' + 'a'.repeat(39), proof: 'b'.repeat(43), expires_in_seconds: 300};

test('a new verification starts with an empty confirmation even if verification fails', async () => {
  const {el, pending} = await page();
  el('password-form').dispatchEvent(new Event('submit'));
  pending.shift()(proof);
  await tick();
  assert.equal(el('confirm-form').hidden, false);
  el('confirmation').value = 'DELETE';
  el('access-key-form').dispatchEvent(new Event('submit'));
  assert.equal(el('confirm-form').hidden, true);
  assert.equal(el('confirmation').value, '');
  pending.shift()(null);
  await tick();
  assert.equal(el('confirm-form').hidden, true);
});

for (const event of ['input', 'pagehide']) {
  test('a verification finishing after ' + event + ' leaves confirmation closed', async () => {
    const {el, window, pending} = await page();
    el('password-form').dispatchEvent(new Event('submit'));
    const target = event === 'input' ? el('email') : window;
    target.dispatchEvent(new Event(event));
    pending.shift()(proof);
    await tick();
    assert.equal(el('confirm-form').hidden, true);
    assert.equal(el('confirmation').value, '');
  });
}

test('a second verified account requires its own explicit confirmation', async () => {
  const {el, pending} = await page();
  el('password-form').dispatchEvent(new Event('submit'));
  pending.shift()(proof);
  await tick();
  el('confirmation').value = 'DELETE';
  el('email').dispatchEvent(new Event('input'));
  assert.equal(el('confirm-form').hidden, true);
  el('password-form').dispatchEvent(new Event('submit'));
  pending.shift()({...proof, request_id: 'daw_' + 'z'.repeat(39)});
  await tick();
  assert.equal(el('confirm-form').hidden, false);
  assert.equal(el('confirmation').value, '');
});
