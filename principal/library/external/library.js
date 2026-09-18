const CORPUS_URL = '/data/research/external-research.json';
const TOPICS_URL = '/data/research/topics.json';

async function loadLibraryData() {
  const [corpusResponse, topicsResponse] = await Promise.all([fetch(CORPUS_URL), fetch(TOPICS_URL)]);
  if (!corpusResponse.ok || !topicsResponse.ok) throw new Error('Unable to load research index');
  return { corpus: await corpusResponse.json(), topics: await topicsResponse.json() };
}

function normalizedText(record) {
  return [record.title, ...(record.authors || []), record.organization, ...(record.keywords || []), record.summary, record.principal_relevance]
    .filter(Boolean).join(' ').toLowerCase();
}

function filterRecords(records, state) {
  const q = state.query.trim().toLowerCase();
  return records.filter(record => {
    if (record.status === 'excluded') return false;
    if (q && !normalizedText(record).includes(q)) return false;
    if (state.topic && !(record.topics || []).includes(state.topic)) return false;
    if (state.type && record.document_type !== state.type) return false;
    if (state.year && String(record.year ?? '') !== state.year) return false;
    return true;
  });
}

function labelForTopic(id, labels) {
  return labels.get(id) || id.replaceAll('-', ' ');
}

function displayByline(record) {
  const parts = [];
  if ((record.authors || []).length) parts.push(record.authors.join(', '));
  if (record.organization) parts.push(record.organization);
  return parts.join(' · ') || 'External source';
}

function createCard(record, topicLabels) {
  const article = document.createElement('article');
  article.className = 'research-card';

  const meta = document.createElement('div');
  meta.className = 'meta';
  meta.textContent = [record.document_type?.replaceAll('-', ' '), record.year].filter(Boolean).join(' · ') || 'External research';

  const title = document.createElement('h2');
  title.textContent = record.title;

  const byline = document.createElement('p');
  byline.className = 'byline';
  byline.textContent = displayByline(record);

  const summary = document.createElement('p');
  summary.className = 'summary';
  summary.textContent = record.summary || 'Metadata indexed; summary pending.';

  const topics = document.createElement('div');
  topics.className = 'topics';
  for (const topicId of record.topics || []) {
    const chip = document.createElement('span');
    chip.className = 'topic';
    chip.textContent = labelForTopic(topicId, topicLabels);
    topics.appendChild(chip);
  }

  const relevance = document.createElement('div');
  relevance.className = 'relevance';
  const why = document.createElement('strong');
  why.textContent = 'Why it matters';
  const whyText = document.createElement('div');
  whyText.textContent = record.principal_relevance || 'Relevance note pending.';
  relevance.append(why, whyText);

  article.append(meta, title, byline, summary, topics, relevance);

  if (record.source_url) {
    const source = document.createElement('a');
    source.className = 'source-link';
    source.href = record.source_url;
    source.target = '_blank';
    source.rel = 'noopener noreferrer';
    source.textContent = 'Open original source →';
    article.appendChild(source);
  }

  if (record.status && record.status !== 'indexed') {
    const status = document.createElement('div');
    status.className = 'status-note';
    status.textContent = `Index status: ${record.status.replaceAll('-', ' ')}`;
    article.appendChild(status);
  }
  return article;
}

function fillSelect(select, values, labels = new Map()) {
  for (const value of values) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = labels.get(value) || value.replaceAll('-', ' ');
    select.appendChild(option);
  }
}

function render(records, topicLabels) {
  const results = document.querySelector('#research-results');
  const count = document.querySelector('#result-count');
  results.replaceChildren();
  count.textContent = `${records.length} external source${records.length === 1 ? '' : 's'}`;
  if (!records.length) {
    const empty = document.createElement('div');
    empty.className = 'empty-state';
    empty.textContent = 'No sources match these filters.';
    results.appendChild(empty);
    return;
  }
  for (const record of records) results.appendChild(createCard(record, topicLabels));
}

async function init() {
  const search = document.querySelector('#research-search');
  const topic = document.querySelector('#topic-filter');
  const type = document.querySelector('#type-filter');
  const year = document.querySelector('#year-filter');
  try {
    const { corpus, topics } = await loadLibraryData();
    const records = corpus.records || [];
    const topicLabels = new Map((topics.topics || []).map(item => [item.id, item.label]));
    fillSelect(topic, [...topicLabels.keys()], topicLabels);
    fillSelect(type, [...new Set(records.map(r => r.document_type).filter(Boolean))].sort());
    fillSelect(year, [...new Set(records.map(r => r.year).filter(y => y !== null && y !== undefined).map(String))].sort().reverse());
    const state = {query:'', topic:'', type:'', year:''};
    const rerender = () => render(filterRecords(records, state), topicLabels);
    search.addEventListener('input', event => { state.query = event.target.value; rerender(); });
    topic.addEventListener('change', event => { state.topic = event.target.value; rerender(); });
    type.addEventListener('change', event => { state.type = event.target.value; rerender(); });
    year.addEventListener('change', event => { state.year = event.target.value; rerender(); });
    rerender();
  } catch (error) {
    const results = document.querySelector('#research-results');
    results.innerHTML = '<div class="empty-state">Research index is temporarily unavailable.</div>';
    console.error(error);
  }
}

document.addEventListener('DOMContentLoaded', init);
