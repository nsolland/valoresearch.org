import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { buildAccessRequest, firstQuestions, SOURCE_OPTIONS } from '../principal/discover/access-plan.mjs';

const now = new Date('2026-10-31T12:00:00.000Z');
const base = { mode: 'GOLD', company: 'Eksempel AS', goal: 'Vi vil oppdage prosessfriksjon i virksomheten.', now };
const html = readFileSync(new URL('../principal/discover/index.html', import.meta.url), 'utf8');

test('default public-only request grants nothing', () => {
  const req = buildAccessRequest(base);
  assert.equal(req.status, 'DRAFT_NOT_SUBMITTED_OR_AUTHORIZED');
  assert.deepEqual(req.requestedSources.map((s) => s.key), ['PUBLIC_MARKET']);
  assert.equal(req.approvals.customerAdministratorApprovalRequired, false);
  assert.ok(Object.values(req.guarantees).every((value) => value === false));
  assert.equal(req.draftedAt, now.toISOString());
});

test('customer systems require an explicit approval but do not give access', () => {
  const req = buildAccessRequest({ ...base, sources: ['WORKSPACE_FOLDER', 'CRM_REPORT'] });
  assert.equal(req.approvals.customerAdministratorApprovalRequired, true);
  assert.equal(req.approvals.customerMandateRequired, true);
  assert.equal(req.guarantees.customerConnectionEstablished, false);
  assert.equal(req.guarantees.accessAuthorized, false);
  assert.ok(req.requestedSources.every((s) => s.access === 'READ_ONLY_REQUESTED'));
});

test('public source is deduplicated', () => {
  assert.equal(buildAccessRequest({ ...base, sources: ['PUBLIC_MARKET', 'PUBLIC_MARKET'] }).requestedSources.length, 1);
});

test('unknown sources and modes reject rather than expand access', () => {
  assert.throws(() => buildAccessRequest({ ...base, sources: ['MAILBOX_ALL'] }), /Ukjent datakilde/);
  assert.throws(() => buildAccessRequest({ ...base, mode: 'CONNECT_ALL' }), /Ukjent inngang/);
  assert.throws(() => firstQuestions('CONNECT_ALL'), /Ukjent inngang/);
});

test('proposed access cannot be indefinite', () => {
  for (const days of [0, 31, -1, 12.5, Infinity]) {
    assert.throws(() => buildAccessRequest({ ...base, durationDays: days }), /1–30/);
  }
  assert.equal(buildAccessRequest({ ...base, durationDays: 30 }).proposedAccessDurationDays, 30);
});

test('user-provided text has bounded lengths', () => {
  assert.throws(() => buildAccessRequest({ ...base, goal: 'kort' }), /minst 10 tegn/);
  assert.throws(() => buildAccessRequest({ ...base, goal: 'a'.repeat(1501) }), /for lang/);
  assert.throws(() => buildAccessRequest({ ...base, company: 'a'.repeat(141) }), /for lang/);
  assert.throws(() => buildAccessRequest({ ...base, goal: null }), /må være tekst/);
});

test('source methods are explicit, public access does not need tenant admin', () => {
  assert.equal(Object.keys(SOURCE_OPTIONS).length, 6);
  assert.equal(SOURCE_OPTIONS.PUBLIC_MARKET.requiresCustomerAdmin, false);
  const req = buildAccessRequest({ ...base, sources: Object.keys(SOURCE_OPTIONS) });
  assert.equal(req.requestedSources.length, 6);
  assert.ok(req.requestedSources.every((s) => Boolean(s.method)));
});

test('all three modes have distinct opening questions', () => {
  assert.equal(firstQuestions('GOLD').length, 3);
  assert.equal(firstQuestions('NEED').length, 3);
  assert.equal(firstQuestions('OPPORTUNITY').length, 3);
  assert.notDeepEqual(firstQuestions('NEED'), firstQuestions('OPPORTUNITY'));
});

test('on-prem shadow is only a proposed mode', () => {
  const req = buildAccessRequest({ ...base, sources: ['CUSTOMER_HOSTED_SHADOW'] });
  assert.equal(req.requestedSources[1].method, 'CUSTOMER_HOSTED_READ_ONLY');
  assert.equal(req.guarantees.automaticIngestionEnabled, false);
  assert.equal(req.guarantees.dataCollectedOrTransmitted, false);
});

test('page exposes three modes and source selection without external submission', () => {
  assert.match(html, /id="discovery-form"/);
  assert.match(html, /id="questions"/);
  assert.equal((html.match(/<label class="mode">/g) || []).length, 3);
  assert.match(html, /name="source"/);
  assert.doesNotMatch(html, /<form[^>]+action=/i);
  assert.doesNotMatch(html, /fetch\s*\(|XMLHttpRequest|sendBeacon/i);
  assert.match(html, /Ingen passord eller API-nøkler/);
});

test('page calls exactly the tested request contract and uses textContent', () => {
  assert.match(html, /import \{ buildAccessRequest, firstQuestions \} from '\.\/access-plan\.mjs'/);
  assert.match(html, /preview\.textContent = JSON\.stringify\(currentDraft/);
  assert.match(html, /item\.textContent = question/);
  assert.match(html, /result\.hidden = true/);
});
