import assert from 'node:assert/strict';
import { after, before, test } from 'node:test';
import { createApp } from '../src/app.js';
import { readConfig } from '../src/config.js';

let server;
let baseUrl;
before(async () => {
  server = createApp().listen(0, '127.0.0.1');
  await new Promise(resolve => server.once('listening', resolve));
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});
after(() => new Promise(resolve => server.close(resolve)));

test('health is available without Firebase or Stripe credentials', async () => {
  const response = await fetch(`${baseUrl}/health`);
  assert.equal(response.status, 200);
  assert.match(response.headers.get('content-type'), /application\/json/);
  assert.deepEqual(await response.json(), {
    status: 'ok', service: 'respawn-api', version: '0.1.0',
  });
});

test('unimplemented checkout cannot be mistaken for a working purchase', async () => {
  const response = await fetch(`${baseUrl}/v1/checkout`, { method: 'POST' });
  assert.equal(response.status, 404);
  assert.deepEqual(await response.json(), { error: 'not_found' });
});

test('invalid ports fail early instead of silently binding another port', () => {
  for (const value of ['abc', '', '0', '-1', '1.2', '65536']) {
    assert.throws(() => readConfig({ PORT: value }), /PORT/);
  }
  assert.deepEqual(readConfig({}), { host: '127.0.0.1', port: 3000 });
});
