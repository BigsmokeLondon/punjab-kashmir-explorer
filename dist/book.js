(function () {
  'use strict';
  const book = window.BOOKPASSAGES;
  const core = window.BookCore;
  const $ = id => document.getElementById(id);
  const selector = $('passage-select');
  let fullText = null, fullTextPromise = null, starts = [], matches = [], matchIndex = 0, searchSerial = 0;
  const passages = [...book.passages].sort((a, b) => {
    if (a.id === 'edition') return -1;
    if (b.id === 'edition') return 1;
    return a.title.localeCompare(b.title, 'en');
  });
  for (const passage of passages) {
    const option = document.createElement('option');
    option.value = passage.id; option.textContent = passage.title;
    selector.append(option);
  }
  function selectPassage(id) {
    const passage = book.passages.find(p => p.id === id) || book.passages.find(p => p.id === 'edition');
    selector.value = passage.id;
    $('passage-title').textContent = passage.title;
    $('passage-locator').textContent = passage.locator;
    $('passage-text').replaceChildren();
    passage.segments.forEach((segment, index) => {
      const label = document.createElement('p'); label.className = 'segment-label';
      label.textContent = 'Upload lines ' + segment.startLine.toLocaleString('en') + '–' + segment.endLine.toLocaleString('en') + (index ? ' · Intervening material omitted' : '');
      const pre = document.createElement('pre'); pre.className = 'ocr-text';
      pre.tabIndex = 0; pre.setAttribute('aria-label', 'Original OCR, upload lines ' + segment.startLine + ' to ' + segment.endLine);
      pre.textContent = segment.text;
      $('passage-text').append(label, pre);
    });
    document.title = passage.title + ' | Panjab Castes source reader';
  }
  function fromHash() {
    try { selectPassage(location.hash.startsWith('#passage=') ? decodeURIComponent(location.hash.slice(9)) : 'edition'); }
    catch { selectPassage('edition'); }
  }
  selector.addEventListener('change', () => {
    try { history.replaceState(null, '', '#passage=' + encodeURIComponent(selector.value)); } catch {}
    selectPassage(selector.value);
  });
  window.addEventListener('hashchange', fromHash);
  $('original-filename').textContent = book.originalFilename;
  $('source-fingerprint').textContent = book.sha256;
  fromHash();

  async function loadFullText() {
    if (fullText !== null) return fullText;
    if (!fullTextPromise) fullTextPromise = fetch(book.fullTextUrl).then(response => {
      if (!response.ok) throw new Error('Text request failed');
      return response.text();
    }).then(text => {
      fullText = core.normaliseText(text); starts = core.lineStarts(fullText); return fullText;
    }).catch(error => { fullTextPromise = null; throw error; });
    return fullTextPromise;
  }
  function showMatch() {
    const match = matches[matchIndex];
    if (!match) return;
    const snippet = core.excerpt(fullText, match);
    const highlight = document.createElement('mark'); highlight.textContent = snippet.hit;
    $('search-excerpt').replaceChildren(document.createTextNode((snippet.start ? '…\n' : '') + snippet.before), highlight, document.createTextNode(snippet.after + (snippet.end < fullText.length ? '\n…' : '')));
    $('search-lines').textContent = 'Match at upload line ' + core.lineAt(starts, match.start).toLocaleString('en') + ' · Surrounding text shown for context';
    $('match-position').textContent = (matchIndex + 1) + ' of ' + matches.length;
    $('previous-match').disabled = matchIndex === 0;
    $('next-match').disabled = matchIndex === matches.length - 1;
  }
  $('book-search-form').addEventListener('submit', async event => {
    event.preventDefault();
    const query = $('book-query').value.trim();
    if (query.length < 2) { $('book-search-status').textContent = 'Enter at least two characters.'; return; }
    const serial = ++searchSerial;
    $('book-search-button').disabled = true;
    $('book-search-status').textContent = 'Loading and searching the uploaded text…';
    for (const id of ['match-controls', 'search-excerpt', 'search-lines']) $(id).hidden = true;
    try {
      const text = await loadFullText();
      if (serial !== searchSerial) return;
      const result = core.searchText(text, query);
      matches = result.matches; matchIndex = 0;
      $('book-search-status').textContent = result.truncated ? 'Showing the first 250 matches. Try a more specific phrase to narrow the search.' : matches.length ? matches.length + (matches.length === 1 ? ' match' : ' matches') + ' in the uploaded text.' : 'No OCR matches. Try a shorter name or another spelling. A missing match does not prove the group is absent.';
      for (const id of ['match-controls', 'search-excerpt', 'search-lines']) $(id).hidden = matches.length === 0;
      showMatch();
    } catch {
      if (serial === searchSerial) $('book-search-status').textContent = 'The full text could not load. Try again. Selected passages remain available.';
    } finally {
      if (serial === searchSerial) $('book-search-button').disabled = false;
    }
  });
  $('previous-match').addEventListener('click', () => { if (matchIndex > 0) { matchIndex--; showMatch(); } });
  $('next-match').addEventListener('click', () => { if (matchIndex < matches.length - 1) { matchIndex++; showMatch(); } });
})();
