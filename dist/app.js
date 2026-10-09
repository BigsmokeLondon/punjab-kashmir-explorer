(function () {
  'use strict';
  const collection = window.COLLECTION;
  const core = window.CollectionCore;
  const records = collection.records;
  const sources = collection.sources;
  const $ = id => document.getElementById(id);
  const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const mark = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h12v18l-6-4-6 4z"/></svg>';
  const pin = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2"/></svg>';
  const stateKey = 'punjab-kashmir-review-v1';
  const filters = { region: 'all', type: 'all', group: 'all', query: '', leads: false, needsReview: false, saved: false };
  let review = Object.create(null);
  let storageAvailable = true;
  let activeId = null;
  let lastTrigger = null;
  let returnToRecord = false;
  let historyTrigger = null;
  let toastTimer;
  try { review = core.cleanReview(JSON.parse(localStorage.getItem(stateKey) || '{}'), records); } catch { storageAvailable = false; }
  function updateStorageMessage() {
    if (!storageAvailable) {
      $('storage-note').classList.add('error');
      $('storage-note').textContent = 'Your browser cannot save review changes. Keep this page open and use Copy saved to keep your notes.';
    }
  }
  function persist() {
    try { localStorage.setItem(stateKey, JSON.stringify(review)); }
    catch { storageAvailable = false; updateStorageMessage(); }
  }
  function row(id) { return review[id] || (review[id] = { saved: false, reviewed: false, notes: '' }); }
  function notify(message) {
    clearTimeout(toastTimer);
    $('toast').textContent = message; $('toast').hidden = false;
    toastTimer = setTimeout(() => { $('toast').hidden = true; }, 3300);
  }
  function saveButton(record) {
    const saved = !!review[record.id]?.saved;
    return '<button class="save-button" data-save="' + record.id + '" aria-pressed="' + saved + '" aria-label="' + (saved ? 'Unsave ' : 'Save ') + escape(record.name) + '">' + mark + '</button>';
  }
  function card(record) {
    // Related names are separate groups; they appear only in the record panel, with their notes.
    const aliases = record.aliases.filter(a => !a.kind.includes('Unconfirmed') && !a.kind.startsWith('Related')).map(a => a.name).join(' · ');
    const reviewed = !!review[record.id]?.reviewed;
    return '<article class="record-card"><div class="card-top"><span class="evidence-pill ' + (record.hasContext ? '' : 'lead') + '">' + (record.hasContext ? 'Context located' : 'Research lead') + '</span>' + saveButton(record) + '</div><h3><button class="name-button" data-open="' + record.id + '">' + escape(record.name) + '</button></h3><p class="aliases">' + escape(aliases || core.types[record.type]) + '</p><p class="classification">' + escape(record.classification) + '</p><p class="card-locations">' + pin + '<span><span class="location-label">' + escape(record.localityLabel || 'Project examples') + '</span>' + escape(record.locations.filter(l => !l.includes('outside')).slice(0, 3).join(' · ')) + '</span></p><div class="card-footer"><span class="' + (reviewed ? 'reviewed-label' : 'pending') + '">' + (reviewed ? '✓ Reviewed' : '○ Needs review') + '</span><button class="card-open" data-open="' + record.id + '">Open record <span aria-hidden="true">↗</span></button></div></article>';
  }
  function render() {
    const matches = core.matchRecords(records, filters, review);
    $('record-grid').innerHTML = matches.map(card).join('');
    $('record-grid').hidden = matches.length === 0;
    $('empty-state').hidden = matches.length !== 0;
    let description = matches.length + (matches.length === 1 ? ' record' : ' records');
    if (filters.region !== 'all') description += ' in ' + core.regions[filters.region];
    if (filters.group !== 'all') description += ' · ' + core.groups[filters.group];
    if (filters.query.trim()) description += ' for “' + filters.query.trim() + '”';
    $('results-count').textContent = description;
    const saved = records.filter(r => review[r.id]?.saved).length;
    $('saved-total').textContent = saved;
    $('export-button').disabled = saved === 0;
    $('clear-search').hidden = !filters.query;
    $('total-count').textContent = records.length;
  }
  function sourceLink(source, label) {
    if (source.image) return '<button data-poster="' + source.id + '">' + (label || 'View project image') + ' <span aria-hidden="true">↗</span></button>';
    if (source.readerUrl) return '<a href="' + escape(source.readerUrl) + '">Read uploaded text <span aria-hidden="true">↗</span></a><a class="edition-link" href="' + escape(source.url) + '" target="_blank" rel="noopener noreferrer">View edition catalogue <span aria-hidden="true">↗</span></a>';
    return '<a href="' + escape(source.url) + '" target="_blank" rel="noopener noreferrer">' + (label || 'Open source') + ' <span aria-hidden="true">↗</span></a>';
  }
  function passageLink(id, label = 'Read uploaded passage') {
    return '<a class="passage-link" href="' + escape(core.passageUrl(id, sources)) + '">' + escape(label) + ' <span aria-hidden="true">↗</span></a>';
  }
  function localitySection(record) {
    const source = sources[record.locationSource];
    const historical = !source.image;
    let html = '<section class="detail-section"><h3>' + (historical ? 'Historical locality examples (1881)' : 'Project locality examples') + '</h3><div class="location-pills">' + record.locations.map(l => '<span>' + escape(l) + '</span>').join('') + '</div><p>' + (historical ? 'Named in the 1881 account. Historical district names and boundaries apply. These are not exclusive territories or verified current distribution.' : 'Examples from the project poster. They are not exclusive territories or independently verified current distribution.') + '</p><p class="source-note">' + escape(source.title) + ' · ' + escape(record.locationLocator || record.name + ' panel') + '</p>' + (record.locationPassageId ? passageLink(record.locationPassageId) : '') + '</section>';
    if (record.historicalLocations?.length) html += '<section class="detail-section"><h3>Separate historical examples (1881)</h3><div class="location-pills">' + record.historicalLocations.map(l => '<span>' + escape(l) + '</span>').join('') + '</div><p>From the dated book account. These examples do not verify the project poster\'s localities. Historical names, districts and boundaries apply.</p>' + passageLink(record.historicalPassageId) + '</section>';
    return html;
  }
  function claimMarkup(claim) {
    return '<article class="claim"><span class="claim-status ' + claim.status + '">' + ({context:'Recorded in cited context',tradition:'Reported tradition, not verified ancestry',verify:'Needs verification'}[claim.status]) + '</span><h4>' + escape(claim.title) + '</h4><p>' + escape(claim.text) + '</p><p class="claim-source">' + escape(sources[claim.source].title) + ' · ' + escape(claim.locator) + '</p>' + (claim.passageId ? passageLink(claim.passageId) : '') + '</article>';
  }
  function renderSources() {
    $('source-grid').innerHTML = Object.values(sources).map(source => '<article class="source-card" id="source-' + source.id + '"><div class="source-visual ' + (source.image ? '' : 'book') + '">' + (source.image ? '<img src="' + source.url + '" loading="lazy" alt="Thumbnail of ' + escape(source.title) + '">' : '<span>' + (source.id === 'ibbetson' ? '19<br>16' : '20<br>06') + '</span>') + '</div><div class="source-body"><p class="eyebrow">' + escape(source.kind) + '</p><h3>' + escape(source.title) + '</h3><p>' + escape(source.author) + ' · ' + escape(source.date) + '</p>' + sourceLink(source) + '<p class="source-limit">' + escape(source.limitation) + '</p></div></article>').join('');
  }
  function reset() {
    Object.assign(filters, { region: 'all', type: 'all', group: 'all', query: '', leads: false, needsReview: false, saved: false });
    $('search').value = ''; $('type-filter').value = 'all'; $('group-filter').value = 'all';
    for (const id of ['lead-filter', 'review-filter', 'saved-filter']) $(id).checked = false;
    document.querySelectorAll('[data-region]').forEach(b => b.setAttribute('aria-pressed', b.dataset.region === 'all'));
    render();
  }
  function sourceDetail(source) {
    return '<div class="detail-source"><strong>' + escape(source.title) + '</strong><p>' + escape(source.author) + ' · ' + escape(source.date) + '</p>' + sourceLink(source) + '<p>' + escape(source.limitation) + '</p></div>';
  }
  function openRecord(id, trigger) {
    const record = records.find(r => r.id === id);
    if (!record) return;
    activeId = id;
    if (trigger) lastTrigger = trigger;
    const own = row(id);
    const aliases = record.aliases.map(a => '<p><strong>' + escape(a.name) + '</strong> · ' + escape(a.kind) + '<br>' + escape(a.note) + '</p>').join('');
    $('record-detail').innerHTML = '<div class="detail-body"><p class="detail-regions">' + record.regions.map(r => escape(core.regions[r])).join(' <span aria-hidden="true">/</span> ') + '</p><div class="detail-title-row"><h2 id="detail-title">' + escape(record.name) + '</h2>' + saveButton(record) + '</div><p class="detail-alias">' + escape(core.types[record.type]) + ' · ' + escape(core.groups[record.group]) + '</p><span class="evidence-pill ' + (record.hasContext ? '' : 'lead') + '">' + (record.hasContext ? 'Context located for a specific claim' : 'Research lead from project material') + '</span><p class="detail-summary">' + escape(record.summary) + '</p><section class="detail-section"><h3>Recorded classification</h3><p class="classification-value">' + escape(record.classification) + '</p><p class="source-note">' + escape(sources[record.classificationSource].title) + '. ' + escape(sources[record.classificationSource].date) + '</p><p>Keep this label attached to its source and locality. It does not settle the ancestry of every family using the name.</p></section>' + (aliases ? '<section class="detail-section"><h3>Names and spellings</h3>' + aliases + '</section>' : '') + localitySection(record) + '<section class="detail-section"><h3>Claims and qualifications</h3>' + record.claims.map(claimMarkup).join('') + '</section><section class="detail-section"><h3>Before you post</h3><p>' + escape(record.question) + '</p><div class="qualified-actions"><button id="copy-summary" class="button button-primary">Copy qualified summary</button><button id="copy-sources" class="button button-secondary">Copy references</button></div><label id="fallback-label" class="sr-only" for="copy-fallback">Text to copy</label><textarea readonly id="copy-fallback" class="copy-fallback" hidden></textarea></section><section class="detail-section"><h3>Your review</h3><label class="review-control"><input id="record-reviewed" type="checkbox" ' + (own.reviewed ? 'checked' : '') + '>Mark this record reviewed</label><p>Review tracks your content checks. It does not verify a lineage claim.</p><label class="notes-label" for="review-notes">Your review notes</label><textarea id="review-notes" class="review-notes" maxlength="12000" placeholder="Add a source to find, a spelling to check, or wording to revise…">' + escape(own.notes) + '</textarea><p id="note-status" class="note-status">' + (storageAvailable ? 'Notes save automatically in this browser.' : 'Browser saving is unavailable. Use Copy saved to keep your notes.') + '</p></section><section class="detail-section"><h3>References for this record</h3>' + record.sourceIds.map(s => sourceDetail(sources[s])).join('') + '</section></div>';
    $('record-reviewed').addEventListener('change', event => { row(id).reviewed = event.target.checked; persist(); render(); notify(event.target.checked ? 'Marked reviewed. Claim qualifications stay in place.' : 'Returned to needs review.'); });
    $('review-notes').addEventListener('input', event => { row(id).notes = event.target.value; persist(); $('note-status').textContent = storageAvailable ? 'Saved in this browser.' : 'Not saved to browser storage. Use Copy saved to keep your notes.'; });
    $('copy-summary').addEventListener('click', () => copyText(core.qualifiedSummary(record, sources, location.origin), 'Qualified summary copied with sources.'));
    $('copy-sources').addEventListener('click', () => copyText(core.references(record, sources, location.origin), 'References copied.'));
    if (!$('record-dialog').open) $('record-dialog').showModal();
    $('record-dialog').scrollTop = 0;
    setHash('#record=' + encodeURIComponent(id));
    $('close-record').focus();
  }
  function closeRecord() {
    $('record-dialog').close(); activeId = null;
    setHash('#explorer');
    if (lastTrigger?.isConnected) lastTrigger.focus();
    else $('search').focus({ preventScroll: true });
  }
  // Hosted copies run in a locked-down frame where URL updates can be refused; the page works without them.
  function setHash(hash) { try { history.replaceState(null, '', hash); } catch {} }
  async function copyText(text, message, fallbackId = 'copy-fallback') {
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(text); notify(message);
    } catch {
      const field = $(fallbackId); field.hidden = false; field.value = text; field.focus(); field.select();
      notify('Text selected. Use your browser’s copy command.');
    }
  }
  function openPoster(id) {
    const source = sources[id]; if (!source?.image) return;
    returnToRecord = $('record-dialog').open;
    if (returnToRecord) $('record-dialog').close();
    $('poster-title').textContent = source.title; $('poster-image').src = source.url;
    $('poster-image').alt = source.title + '. A working project poster with named groups and locality examples; decorative symbols are not authenticated.';
    $('poster-dialog').showModal(); $('poster-dialog').scrollTop = 0;
  }
  // Copy rather than download: hosted pages cannot start file downloads.
  function copySaved() {
    copyText(core.exportSaved(records, sources, review, location.origin), 'Saved records copied with qualifications and review notes.', 'export-fallback');
  }
  document.addEventListener('click', event => {
    const save = event.target.closest('[data-save]');
    if (save) {
      const id = save.dataset.save;
      const record = records.find(r => r.id === id);
      if (!record) return;
      const inDialog = save.closest('dialog');
      row(id).saved = !row(id).saved;
      persist(); render();
      if (inDialog && activeId === id && $('record-dialog').open) {
        save.setAttribute('aria-pressed', row(id).saved);
        save.setAttribute('aria-label', (row(id).saved ? 'Unsave ' : 'Save ') + record.name);
      } else {
        const replacement = $('record-grid').querySelector('[data-save="' + id + '"]');
        (replacement || $('saved-filter')).focus({ preventScroll: true });
      }
      notify(row(id).saved ? record.name + ' saved for review.' : record.name + ' removed from saved records.');
      return;
    }
    const open = event.target.closest('[data-open]'); if (open) { openRecord(open.dataset.open, open); return; }
    const poster = event.target.closest('[data-poster]'); if (poster) { openPoster(poster.dataset.poster); return; }
    const historical = event.target.closest('[data-history]');
    if (historical) {
      const card = historical.closest('figure');
      const img = historical.querySelector('img');
      historyTrigger = historical;
      $('history-viewer-title').textContent = card.querySelector('h3')?.textContent || 'Regional heritage, imagined';
      $('history-viewer-image').src = img.getAttribute('src');
      $('history-viewer-image').alt = img.alt;
      $('history-viewer-caption').innerHTML = card.querySelector('figcaption').innerHTML;
      $('history-dialog').showModal();
      $('history-dialog').scrollTop = 0;
      $('close-history').focus();
      return;
    }
    const region = event.target.closest('[data-region]');
    if (region) { filters.region = region.dataset.region; document.querySelectorAll('[data-region]').forEach(b => b.setAttribute('aria-pressed', b === region)); render(); }
  });
  $('search').addEventListener('input', event => { filters.query = event.target.value; render(); });
  $('type-filter').addEventListener('change', event => { filters.type = event.target.value; render(); });
  $('group-filter').append(...Object.entries(core.groups).map(([value, label]) => new Option(label, value)));
  $('group-filter').addEventListener('change', event => { filters.group = event.target.value; render(); });
  for (const [id,key] of [['lead-filter','leads'],['review-filter','needsReview'],['saved-filter','saved']]) $(id).addEventListener('change', event => { filters[key] = event.target.checked; render(); });
  $('clear-search').addEventListener('click', () => { filters.query = ''; $('search').value = ''; render(); $('search').focus(); });
  $('reset-filters').addEventListener('click', reset); $('empty-reset').addEventListener('click', reset);
  $('export-button').addEventListener('click', copySaved); $('close-record').addEventListener('click', closeRecord);
  $('record-dialog').addEventListener('cancel', event => { event.preventDefault(); closeRecord(); });
  $('record-dialog').addEventListener('click', event => { if (event.target === $('record-dialog') && event.clientX < $('record-dialog').getBoundingClientRect().left) closeRecord(); });
  $('close-poster').addEventListener('click', () => $('poster-dialog').close());
  $('close-history').addEventListener('click', () => $('history-dialog').close());
  $('history-dialog').addEventListener('close', () => { if (historyTrigger?.isConnected) historyTrigger.focus({ preventScroll: true }); });
  $('poster-dialog').addEventListener('close', () => { if (returnToRecord && activeId) { returnToRecord = false; $('record-dialog').showModal(); $('close-record').focus(); } });
  document.addEventListener('keydown', event => { if (event.key === '/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName) && !$('record-dialog').open && !$('poster-dialog').open && !$('history-dialog').open) { event.preventDefault(); $('search').focus(); $('search').scrollIntoView({block:'center'}); } });
  renderSources(); render(); updateStorageMessage();
  if (location.hash.startsWith('#record=')) {
    try { openRecord(decodeURIComponent(location.hash.slice(8))); }
    catch { setHash('#explorer'); }
  }
})();
