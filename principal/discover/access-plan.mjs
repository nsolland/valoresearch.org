// Browser-only request builder; this file does not connect to customer systems.
export const ENTRY_MODES = Object.freeze(['GOLD', 'NEED', 'OPPORTUNITY']);

export const SOURCE_OPTIONS = Object.freeze({
  PUBLIC_MARKET: { label: 'Åpne markeds- og selskapskilder', method: 'PUBLIC_SOURCE_REVIEW', requiresCustomerAdmin: false },
  CUSTOMER_FILES: { label: 'Utvalgte dokumenter eller eksportfiler', method: 'CUSTOMER_SELECTED_TRANSFER', requiresCustomerAdmin: true },
  WORKSPACE_FOLDER: { label: 'Avgrenset Microsoft 365-område eller Google Drive-mappe', method: 'SCOPED_DELEGATED_READ', requiresCustomerAdmin: true },
  CRM_REPORT: { label: 'Eksplisitt valgte CRM-rapporter', method: 'SCOPED_DELEGATED_READ', requiresCustomerAdmin: true },
  ATS_REPORT: { label: 'Eksplisitt valgte ATS-/rekrutteringsrapporter', method: 'SCOPED_DELEGATED_READ', requiresCustomerAdmin: true },
  CUSTOMER_HOSTED_SHADOW: { label: 'Shadow-analyse i kundens eget miljø', method: 'CUSTOMER_HOSTED_READ_ONLY', requiresCustomerAdmin: true }
});

function normalize(value, limit, field) {
  if (typeof value !== 'string') throw new TypeError(field + ' må være tekst');
  const clean = value.trim();
  if (clean.length > limit) throw new RangeError(field + ' er for lang');
  return clean;
}

export function firstQuestions(mode) {
  if (!ENTRY_MODES.includes(mode)) throw new TypeError('Ukjent inngang');
  if (mode === 'NEED') return [
    'Hva skal faktisk være levert når behovet er løst?',
    'Hvor ofte trengs kompetansen – for eksempel 10 timer per måned?',
    'Hvilken beslutning eller oppgave kan ikke vente?'
  ];
  if (mode === 'OPPORTUNITY') return [
    'Er målet vekst, oppkjøp, partnerskap eller finansiering?',
    'Hvilket geografisk eller faglig marked er relevant?',
    'Hva må være dokumentert før dere åpner et nytt spor?'
  ];
  return [
    'Hva ønsker dere skal fungere bedre om seks måneder?',
    'Hvor oppstår det friksjon, venting eller kompetansegap?',
    'Hva vet dere sikkert, og hva er fortsatt bare en hypotese?'
  ];
}

export function buildAccessRequest({
  mode = 'GOLD', company = '', goal, sponsor = '', sources = ['PUBLIC_MARKET'],
  durationDays = 14, now = new Date()
}) {
  if (!ENTRY_MODES.includes(mode)) throw new TypeError('Ukjent inngang');
  const companyName = normalize(company, 140, 'Bedriftsnavn');
  const statedGoal = normalize(goal, 1500, 'Situasjonen');
  const customerSponsor = normalize(sponsor, 140, 'Kontaktperson');
  if (statedGoal.length < 10) throw new TypeError('Beskriv situasjonen med minst 10 tegn');
  if (!Array.isArray(sources)) throw new TypeError('Kilder må være en liste');
  if (!Number.isInteger(durationDays) || durationDays < 1 || durationDays > 30) {
    throw new RangeError('Forslag til tilgangsperiode må være 1–30 dager');
  }
  const keys = [...new Set(['PUBLIC_MARKET', ...sources])];
  if (keys.some((key) => !Object.hasOwn(SOURCE_OPTIONS, key))) throw new TypeError('Ukjent datakilde');
  if (!(now instanceof Date) || !Number.isFinite(now.getTime())) throw new TypeError('Gyldig tidspunkt påkrevd');
  const customerSources = keys.filter((key) => SOURCE_OPTIONS[key].requiresCustomerAdmin);
  return {
    schemaVersion: 'principal.discover.access-request.v1',
    status: 'DRAFT_NOT_SUBMITTED_OR_AUTHORIZED',
    draftedAt: now.toISOString(),
    companyName,
    entryMode: mode,
    statedGoal,
    firstQuestions: firstQuestions(mode),
    customerSponsor,
    purpose: 'QUESTION_DISCOVERY_AND_NON_BINDING_SCOPE_PROPOSALS',
    requestedSources: keys.map((key) => ({ key, ...SOURCE_OPTIONS[key], access: 'READ_ONLY_REQUESTED' })),
    proposedAccessDurationDays: durationDays,
    approvals: {
      customerMandateRequired: customerSources.length > 0,
      customerAdministratorApprovalRequired: customerSources.length > 0,
      tenantAndSourceScopeMustBeVerified: true,
      customerCanRevoke: true,
      credentialsMustNotBePastedOrShared: true
    },
    guarantees: {
      customerConnectionEstablished: false,
      dataCollectedOrTransmitted: false,
      accessAuthorized: false,
      automaticIngestionEnabled: false,
      contactAuthorized: false,
      writeOrExecutionAuthorized: false,
      seniorOrFundingCommitted: false
    },
    nextAction: 'CUSTOMER_AND_VALO_REVIEW_SCOPE_THEN_CONFIGURE_SEPARATE_CONSENTED_CONNECTOR'
  };
}
