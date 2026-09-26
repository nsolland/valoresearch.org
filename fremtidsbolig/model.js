(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.Fremtidsbolig = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  function monthlyPayment(principal, annualRatePct, years) {
    if (principal <= 0 || years <= 0) return 0;
    const n = Math.round(years * 12);
    const r = annualRatePct / 100 / 12;
    if (r === 0) return principal / n;
    return principal * r / (1 - Math.pow(1 + r, -n));
  }

  function mortgageState(principal, annualRatePct, mortgageYears, elapsedYears) {
    if (principal <= 0) return { remaining: 0, payment: 0, totalInterest: 0 };
    const termMonths = Math.max(1, Math.round(mortgageYears * 12));
    const elapsedMonths = Math.min(termMonths, Math.max(0, Math.round(elapsedYears * 12)));
    const payment = monthlyPayment(principal, annualRatePct, mortgageYears);
    const r = annualRatePct / 100 / 12;
    let remaining;
    if (elapsedMonths >= termMonths) remaining = 0;
    else if (r === 0) remaining = principal * (1 - elapsedMonths / termMonths);
    else remaining = principal * Math.pow(1 + r, elapsedMonths) - payment * ((Math.pow(1 + r, elapsedMonths) - 1) / r);
    remaining = Math.max(0, remaining);
    const principalRepaid = principal - remaining;
    const totalPaid = payment * elapsedMonths;
    return { remaining, payment, totalInterest: Math.max(0, totalPaid - principalRepaid) };
  }

  function geometricMaintenance(homePrice, annualGrowth, annualMaintenance, years) {
    if (years <= 0 || annualMaintenance <= 0) return 0;
    const g = annualGrowth / 100;
    const m = annualMaintenance / 100;
    if (Math.abs(g) < 1e-12) return homePrice * m * years;
    return homePrice * m * ((Math.pow(1 + g, years) - 1) / g);
  }

  function calculateFremtidsbolig(input) {
    const homePrice = Math.max(0, Number(input.homePrice) || 0);
    const equityPct = Math.min(100, Math.max(0, Number(input.equityPct) || 0));
    const years = Math.max(0, Number(input.years) || 0);
    const homeGrowthPct = Number(input.homeGrowthPct) || 0;
    const inflationPct = Number(input.inflationPct) || 0;
    const mortgageRatePct = Math.max(0, Number(input.mortgageRatePct) || 0);
    const maintenancePct = Math.max(0, Number(input.maintenancePct) || 0);
    const alternativeReturnPct = Number(input.alternativeReturnPct) || 0;
    const fxChangePct = Number(input.fxChangePct) || 0;
    const mortgageYears = Math.max(1, Number(input.mortgageYears) || 30);

    const initialEquity = homePrice * equityPct / 100;
    const initialLoan = homePrice - initialEquity;
    const nominalHomeValue = homePrice * Math.pow(1 + homeGrowthPct / 100, years);
    const inflationFactor = Math.pow(1 + inflationPct / 100, years);
    const realHomeValue = inflationFactor === 0 ? nominalHomeValue : nominalHomeValue / inflationFactor;
    const mortgage = mortgageState(initialLoan, mortgageRatePct, mortgageYears, years);
    const totalMaintenance = geometricMaintenance(homePrice, homeGrowthPct, maintenancePct, years);
    const netHousingOutcome = nominalHomeValue - mortgage.remaining - mortgage.totalInterest - totalMaintenance;
    const realNetHousingOutcome = inflationFactor === 0 ? netHousingOutcome : netHousingOutcome / inflationFactor;
    const alternativeNominal = initialEquity * Math.pow(1 + alternativeReturnPct / 100, years) * (1 + fxChangePct / 100);
    const alternativeReal = inflationFactor === 0 ? alternativeNominal : alternativeNominal / inflationFactor;

    return {
      initialEquity,
      initialLoan,
      nominalHomeValue,
      realHomeValue,
      remainingLoan: mortgage.remaining,
      monthlyPayment: mortgage.payment,
      totalInterest: mortgage.totalInterest,
      totalMaintenance,
      netHousingOutcome,
      realNetHousingOutcome,
      alternativeNominal,
      alternativeReal,
      realHousingGrowthPct: homePrice > 0 ? (realHomeValue / homePrice - 1) * 100 : 0,
      realAlternativeGrowthPct: initialEquity > 0 ? (alternativeReal / initialEquity - 1) * 100 : 0
    };
  }

  return { calculateFremtidsbolig, monthlyPayment, mortgageState };
});
