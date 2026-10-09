(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.BookCore = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function normaliseText(text) {
    return String(text).replace(/\r\n?/g, '\n');
  }
  function searchText(text, query, limit = 250) {
    const q = String(query || '').trim().slice(0, 160);
    if (q.length < 2) return { matches: [], truncated: false };
    // Literal phrases, with flexible whitespace for OCR's doubled spaces and
    // line breaks. User punctuation is never interpreted as a regular expression.
    const pattern = q.split(/\s+/).map(part => part.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('\\s+');
    const re = new RegExp(pattern, 'giu');
    const matches = [];
    let found;
    while ((found = re.exec(text))) {
      if (matches.length >= limit) return { matches, truncated: true };
      matches.push({ start: found.index, end: found.index + found[0].length });
    }
    return { matches, truncated: false };
  }
  function lineStarts(text) {
    const starts = [0];
    for (let i = 0; i < text.length; i++) if (text[i] === '\n') starts.push(i + 1);
    return starts;
  }
  function lineAt(starts, offset) {
    let low = 0, high = starts.length;
    while (low < high) {
      const mid = (low + high) >>> 1;
      if (starts[mid] <= offset) low = mid + 1;
      else high = mid;
    }
    return Math.max(1, low);
  }
  function excerpt(text, match, radius = 650) {
    const start = Math.max(0, match.start - radius);
    const end = Math.min(text.length, match.end + radius);
    return { start, end, before: text.slice(start, match.start),
      hit: text.slice(match.start, match.end), after: text.slice(match.end, end) };
  }
  return { normaliseText, searchText, lineStarts, lineAt, excerpt };
});
