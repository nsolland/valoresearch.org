const test = require('node:test');
const assert = require('node:assert/strict');
const { calculateFremtidsbolig } = require('../fremtidsbolig/model.js');

test('inflation removes nominal housing growth when rates are equal', () => {
  const r = calculateFremtidsbolig({
    homePrice: 5_000_000, equityPct: 15, years: 10,
    homeGrowthPct: 3, inflationPct: 3, mortgageRatePct: 4,
    maintenancePct: 1, alternativeReturnPct: 5, fxChangePct: 0,
    mortgageYears: 30
  });
  assert.ok(Math.abs(r.realHomeValue - 5_000_000) < 1);
});

test('weakening krone increases NOK value of a foreign alternative investment', () => {
  const base = calculateFremtidsbolig({
    homePrice: 5_000_000, equityPct: 15, years: 10,
    homeGrowthPct: 3, inflationPct: 3, mortgageRatePct: 4,
    maintenancePct: 1, alternativeReturnPct: 5, fxChangePct: 0,
    mortgageYears: 30
  });
  const weak = calculateFremtidsbolig({
    homePrice: 5_000_000, equityPct: 15, years: 10,
    homeGrowthPct: 3, inflationPct: 3, mortgageRatePct: 4,
    maintenancePct: 1, alternativeReturnPct: 5, fxChangePct: 20,
    mortgageYears: 30
  });
  assert.ok(weak.alternativeNominal > base.alternativeNominal);
  assert.ok(Math.abs(weak.alternativeNominal / base.alternativeNominal - 1.2) < 1e-12);
});

test('mortgage balance reaches zero after the amortization term', () => {
  const r = calculateFremtidsbolig({
    homePrice: 4_000_000, equityPct: 25, years: 36,
    homeGrowthPct: 3, inflationPct: 2.5, mortgageRatePct: 4,
    maintenancePct: 1, alternativeReturnPct: 5, fxChangePct: 0,
    mortgageYears: 30
  });
  assert.equal(r.remainingLoan, 0);
  assert.ok(r.totalInterest > 0);
});

test('higher maintenance reduces net housing outcome', () => {
  const common = {
    homePrice: 5_000_000, equityPct: 15, years: 20,
    homeGrowthPct: 3, inflationPct: 2.5, mortgageRatePct: 4,
    alternativeReturnPct: 5, fxChangePct: 0, mortgageYears: 30
  };
  const low = calculateFremtidsbolig({ ...common, maintenancePct: 0.5 });
  const high = calculateFremtidsbolig({ ...common, maintenancePct: 2 });
  assert.ok(high.netHousingOutcome < low.netHousingOutcome);
});
