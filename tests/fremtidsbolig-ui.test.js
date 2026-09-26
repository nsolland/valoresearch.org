const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const html = fs.readFileSync(path.join(__dirname, '..', 'fremtidsbolig', 'index.html'), 'utf8');

test('fremtidsbolig uses the VALO visual dashboard structure', () => {
  for (const token of [
    'class="site-nav"',
    'class="hero-shell"',
    'class="kpi-grid"',
    'class="dashboard-grid"',
    'id="historyChart"',
    'class="scenario-tabs"',
    'id="generationCompare"',
    'id="returnCard"'
  ]) assert.ok(html.includes(token), `missing ${token}`);
});

test('fremtidsbolig keeps the model interactive rather than replacing it with an image', () => {
  assert.ok(html.includes('<script src="./model.js"></script>'));
  assert.ok(html.includes('type="range"'));
  assert.ok(html.includes('Fremtidsbolig.calculateFremtidsbolig'));
  assert.ok(!html.includes('bolig_som_sparemodell_valo_dashboard.png'));
});

test('scenario presets and alternative return remain available', () => {
  for (const label of ['Forsiktig', 'Basis', 'Optimistisk', 'Alternativ nominell avkastning']) {
    assert.ok(html.includes(label), `missing ${label}`);
  }
});
