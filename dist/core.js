(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.CollectionCore = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const types = { community: 'Community identity', clan: 'Clan or group name', title: 'Name or lineage title' };
  const regions = { punjab: 'Punjab', kashmir: 'Kashmir (AJK)' };
  // Where Panjab Castes discusses a name: its part and section headings, lightly reworded.
  const groups = { 'baloch-pathan': 'Baloch, Pathan and allied tribes', jat: 'Jat tribes', rajput: 'Rajput tribes', dominant: 'Minor dominant tribes', agricultural: 'Agricultural and pastoral tribes', foreign: '“Foreign races” (1881 term)', religious: 'Religious, professional and other castes', artisan: 'Artisan and service castes', project: 'Project material only' };
  function normalise(value) {
    return String(value || '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9\u0600-\u06ff]+/g, ' ').trim();
  }
  function matchRecords(records, filters = {}, review = {}) {
    const terms = normalise(filters.query).split(' ').filter(Boolean);
    return records.filter(record => {
      if (filters.region && filters.region !== 'all' && !record.regions.includes(filters.region)) return false;
      if (filters.type && filters.type !== 'all' && record.type !== filters.type) return false;
      if (filters.group && filters.group !== 'all' && record.group !== filters.group) return false;
      if (filters.leads && record.hasContext) return false;
      if (filters.needsReview && review[record.id]?.reviewed) return false;
      if (filters.saved && !review[record.id]?.saved) return false;
      const text = normalise([record.name, ...record.aliases.map(a => a.name), ...record.locations, ...(record.historicalLocations || []), record.classification].join(' '));
      return terms.every(term => text.includes(term));
    }).sort((a, b) => a.name.localeCompare(b.name, 'en'));
  }
  function cleanReview(raw, records) {
    const clean = Object.create(null);
    if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return clean;
    for (const record of records) {
      const row = Object.prototype.hasOwnProperty.call(raw, record.id) ? raw[record.id] : null;
      if (!row || typeof row !== 'object') continue;
      clean[record.id] = { saved: row.saved === true, reviewed: row.reviewed === true, notes: typeof row.notes === 'string' ? row.notes.slice(0, 12000) : '' };
    }
    return clean;
  }
  function localUrl(path, origin = '') {
    return origin ? new URL(path, origin + '/').href : path;
  }
  function passageUrl(id, sources, origin = '') {
    return localUrl(sources.ibbetson.readerUrl + '#passage=' + encodeURIComponent(id), origin);
  }
  function references(record, sources, origin = '') {
    return record.sourceIds.map(id => {
      const source = sources[id];
      const url = source.image ? localUrl(source.url, origin) : source.url;
      const locators = [...new Set(record.claims.filter(c => c.source === id).map(c => c.locator))].join('; ');
      const passages = [...new Set(record.claims.filter(c => c.source === id && c.passageId).map(c => c.passageId))];
      return source.author + '. ' + source.title + '. ' + source.date + '. ' + locators + '. ' + url + (source.image ? ' (project material)' : '') + (passages.length ? '\nUploaded passages: ' + passages.map(p => passageUrl(p, sources, origin)).join('; ') : '');
    }).join('\n\n');
  }
  function qualifiedSummary(record, sources, origin = '') {
    const classificationSource = sources[record.classificationSource || record.locationSource];
    const lines = [record.name, 'Working collection | ' + record.regions.map(r => regions[r]).join(' / '), '', record.summary, '', 'Classification as recorded in ' + classificationSource.title + ': ' + record.classification];
    for (const claim of record.claims.filter(c => c.status === 'context' || c.status === 'tradition')) lines.push('', (claim.status === 'tradition' ? 'Reported tradition, not verified ancestry: ' : 'Specific source context: ') + claim.text + ' [' + sources[claim.source].title + ', ' + claim.locator + ']' + (claim.passageId ? '\nRead uploaded passage: ' + passageUrl(claim.passageId, sources, origin) : ''));
    lines.push('', 'Qualification: ' + record.caution);
    if (record.aliases.length) lines.push('', 'Names in sources: ' + record.aliases.map(a => a.name + (a.kind.includes('Unconfirmed') ? ' (unconfirmed project label)' : ' (' + a.kind.toLowerCase() + ')')).join('; '));
    if (record.locations.length) lines.push('', (sources[record.locationSource].image ? 'Locality examples from project material: ' : 'Historical locality examples in the 1881 account: ') + record.locations.join(', ') + '. These are examples, not exclusive territories or verified current distribution.');
    if (record.historicalLocations?.length) lines.push('', 'Separate historical examples (1881 account): ' + record.historicalLocations.join(', ') + '. Historical district names and boundaries apply. This does not verify the poster examples.');
    lines.push('', 'Sources:', references(record, sources, origin));
    lines.push('', 'Reviewed as content does not mean verified ancestry.');
    return lines.join('\n');
  }
  function exportSaved(records, sources, review, origin = '') {
    const saved = records.filter(r => review[r.id]?.saved).sort((a, b) => a.name.localeCompare(b.name, 'en'));
    return ['PUNJAB AND KASHMIR | SAVED RESEARCH RECORDS', 'A working selection. Qualifications and sources are retained.', 'Exported ' + new Date().toISOString().slice(0, 10), '', ...saved.flatMap(record => [qualifiedSummary(record, sources, origin), '', 'Editorial review: ' + (review[record.id].reviewed ? 'Reviewed' : 'Needs review'), 'Your notes: ' + (review[record.id].notes || '(none)'), '', '========================================', ''])].join('\n');
  }
  return { types, regions, groups, normalise, matchRecords, cleanReview, qualifiedSummary, exportSaved, references, passageUrl };
});
