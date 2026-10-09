import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { createRequire } from 'node:module';
import vm from 'node:vm';
import { createHash } from 'node:crypto';

const require = createRequire(import.meta.url);
const core = require('./dist/core.js');
const bookCore = require('./dist/book-core.js');
const context = { window: {} };
vm.runInNewContext(readFileSync('dist/data.js', 'utf8'), context);
vm.runInNewContext(readFileSync('dist/passages.js', 'utf8'), context);
const { records, sources } = context.window.COLLECTION;
const book = context.window.BOOKPASSAGES;
const uploadedBytes = readFileSync('dist/' + book.fullTextUrl);
const fullText = bookCore.normaliseText(uploadedBytes.toString('utf8'));
const ids = result => Array.from(result, r => r.id);
const find = id => records.find(r => r.id === id);
let checks = 0;
function check(label, run) { run(); checks++; console.log('PASS ' + label); }

check('Collection identity and source references are internally complete', () => {
  assert.equal(records.length, 109);
  assert.equal(new Set(records.map(r => r.id)).size, records.length);
  for (const record of records) {
    assert.ok(record.caution.length > 40, record.id);
    assert.ok(record.regions.every(r => core.regions[r]), record.id);
    assert.ok(core.types[record.type]);
    assert.ok(sources[record.locationSource]);
    assert.ok(sources[record.classificationSource]);
    if (!sources[record.locationSource].image) {
      assert.equal(record.locationSource, 'ibbetson');
      assert.ok(record.locationLocator && record.locationPassageId);
      assert.ok(record.localityLabel.includes('1881'));
    }
    assert.ok(record.claims.every(c => sources[c.source] && c.locator && ['context', 'tradition', 'verify'].includes(c.status)));
    assert.equal(record.hasContext, record.claims.some(c => c.status === 'context'));
    assert.ok(record.sourceIds.includes(record.locationSource));
    assert.ok(record.claims.every(c => record.sourceIds.includes(c.source)));
  }
});
check('Alternative and historical spellings resolve to distinct records', () => {
  for (const [query, id] of [['cHoHaN','chauhan'],['manhas','minhas'],['Minhas','minhas'],['Gakkhar','gakhar'],['Jutt','jat'],['Gujar','gujjar'],['Bajju','bajwa'],['Saiyad','syed'],['Kasar','kassar'],['Zargar','sunar'],['Ansari','sheikh']]) {
    assert.deepEqual(ids(core.matchRecords(records, { query })), [id]);
  }
  // Chibhali hill people are discussed in the Kashmiri passage, so both records answer this search.
  assert.deepEqual(ids(core.matchRecords(records, { query: 'Chibh' })), ['chibb', 'kashmiri']);
  assert.deepEqual(ids(core.matchRecords(records, { query: 'Khokhar' })), ['khokhar']);
  assert.ok(find('dogar').aliases.find(a => a.name === 'Dogan').kind.includes('Unconfirmed'));
  assert.ok(find('naru').aliases.find(a => a.name === 'Narwa').kind.includes('Unconfirmed'));
});
check('Region, type, place and no-result searches compose correctly', () => {
  assert.equal(core.matchRecords(records, { region: 'punjab' }).length, 106);
  assert.equal(core.matchRecords(records, { region: 'kashmir' }).length, 12);
  for (const region of ['punjab', 'kashmir']) {
    assert.ok(ids(core.matchRecords(records, { region })).includes('minhas'));
    assert.ok(ids(core.matchRecords(records, { region })).includes('chibb'));
  }
  assert.deepEqual(ids(core.matchRecords(records, { query: 'rawalpindi jasra', region: 'punjab', type: 'clan' })), ['jasra']);
  assert.deepEqual(ids(core.matchRecords(records, { region: 'punjab', type: 'title' })), ['qureshi', 'sheikh', 'syed']);
  assert.deepEqual(ids(core.matchRecords(records, { query: 'mitha tiwana', region: 'punjab' })), ['tiwana']);
  assert.equal(core.matchRecords(records, { query: 'unlisted-name-xyz' }).length, 0);
});
check('Every record has one 1881 grouping, and the grouping filter composes', () => {
  for (const record of records) assert.ok(core.groups[record.group], record.id);
  assert.deepEqual(Object.keys(core.groups).filter(g => !records.some(r => r.group === g)), []);
  assert.deepEqual(ids(core.matchRecords(records, { group: 'baloch-pathan', query: 'rajanpur' })), ['baloch', 'bozdar', 'drishak']);
  assert.deepEqual(ids(core.matchRecords(records, { group: 'religious', region: 'kashmir' })), ['kashmiri', 'syed']);
  assert.deepEqual(ids(core.matchRecords(records, { group: 'foreign', type: 'title' })), ['qureshi', 'sheikh']);
  assert.deepEqual(ids(core.matchRecords(records, { group: 'project' })), ['abbasi', 'jasgam', 'jasra', 'khawaja', 'sudhan']);
  assert.equal(core.matchRecords(records, { group: 'artisan', region: 'kashmir' }).length, 0);
  for (const record of core.matchRecords(records, { group: 'artisan' })) assert.ok(record.caution.includes('did not define descent'), record.id);
});
check('Modern spellings resolve but stay marked as editorial', () => {
  for (const [query, id] of [['Leghari','laghari'],['Gill','gil'],['Sandhu','sindhu'],['Aulakh','aulak'],['Joiya','joya'],['Qaisrani','qasrani'],['Baluch','baloch']]) {
    assert.deepEqual(ids(core.matchRecords(records, { query })), [id]);
  }
  const editorial = records.flatMap(r => r.aliases).filter(a => a.kind.startsWith('Modern spelling'));
  assert.ok(editorial.length >= 10);
  assert.ok(editorial.every(a => a.note.includes('does not come from the 1881 source')));
  assert.ok(core.qualifiedSummary(find('laghari'), sources).includes('Leghari (modern spelling, editorial search aid)'));
  assert.ok(find('kashmiri').caution.includes('the passage names no AJK district'));
  // Khawaja cites the book only as a pointer; its copied summary must carry the disclaimer with the citation.
  const khawajaNote = find('khawaja').claims.find(c => c.passageId === 'khojah-paracha');
  assert.equal(khawajaNote.status, 'verify');
  const khawajaCopy = core.qualifiedSummary(find('khawaja'), sources);
  assert.ok(khawajaCopy.includes('#passage=khojah-paracha') && khawajaCopy.includes('does not identify the AJK Khawaja entry'));
  const page = readFileSync('dist/index.html', 'utf8');
  assert.ok(page.includes('<strong>' + context.window.COLLECTION.book.bookAddedRecords + ' records now come from'));
  assert.ok(page.includes('id="total-count">' + records.length + '<'));
});
check('Saved and reviewed filters do not change evidence status', () => {
  const review = { jasra: { saved: true, reviewed: true, notes: 'Find a district reference.' }, dogar: { saved: true, reviewed: false, notes: '' } };
  assert.deepEqual(ids(core.matchRecords(records, { saved: true, needsReview: true }, review)), ['dogar']);
  assert.ok(!ids(core.matchRecords(records, { needsReview: true }, review)).includes('jasra'));
  assert.ok(ids(core.matchRecords(records, { leads: true }, review)).includes('jasra'));
  assert.ok(!find('jasra').hasContext);
});
check('Copy retains classification, source context, locators and uncertainty', () => {
  for (const record of records) {
    const summary = core.qualifiedSummary(record, sources, 'https://example.test');
    assert.ok(summary.includes(record.caution));
    assert.ok(summary.includes(record.classification));
    assert.ok(summary.includes('not exclusive territories or verified current distribution'));
    assert.ok(summary.includes('Reviewed as content does not mean verified ancestry.'));
    if (record.sourceIds.some(id => sources[id].image)) assert.ok(summary.includes('private project material'));
    for (const claim of record.claims) {
      assert.ok(summary.includes(claim.locator));
      if (claim.status === 'context' || claim.status === 'tradition') assert.ok(summary.includes(claim.text));
      if (claim.passageId) assert.ok(summary.includes('https://example.test/book.html#passage=' + claim.passageId));
    }
  }
  assert.ok(core.qualifiedSummary(find('dogar'), sources).includes('Dogan (unconfirmed project label)'));
});
check('Export includes only saved records and keeps review notes and caveats', () => {
  const exported = core.exportSaved(records, sources, { dogar: { saved: true, reviewed: true, notes: 'Check Dogan spelling.' }, jasra: { saved: false, reviewed: false, notes: '' } }, 'https://example.test');
  assert.ok(exported.includes(find('dogar').caution));
  assert.ok(exported.includes('Editorial review: Reviewed'));
  assert.ok(exported.includes('Your notes: Check Dogan spelling.'));
  assert.ok(!exported.includes(find('jasra').summary));
});
check('Storage validation drops unknown keys and invalid review state', () => {
  const review = core.cleanReview(JSON.parse('{"dogar":{"saved":true,"reviewed":"yes","notes":"Keep context"},"unknown":{"saved":true},"__proto__":{"saved":true}}'), records);
  assert.equal(Object.getPrototypeOf(review), null);
  assert.equal(review.dogar.saved, true);
  assert.equal(review.dogar.reviewed, false);
  assert.equal(review.dogar.notes, 'Keep context');
  assert.deepEqual(Object.keys(review), ['dogar']);
  assert.equal(core.cleanReview({ dogar: { notes: 'a'.repeat(13000) } }, records).dogar.notes.length, 12000);
});
check('Local source assets are present and the pages start no downloads', () => {
  // The hosted copy runs where downloads are blocked, so the pages must not depend on them.
  for (const page of ['dist/index.html', 'dist/book.html']) assert.ok(!/<a\b[^>]*\sdownload\b/.test(readFileSync(page, 'utf8')), page);
  for (const script of ['dist/app.js', 'dist/book.js']) assert.ok(!/\.download\s*=|createObjectURL/.test(readFileSync(script, 'utf8')), script);
  for (const source of Object.values(sources)) if (source.image) assert.ok(existsSync('dist/' + source.url));
  assert.ok(existsSync('dist/assets/Punjab_Kashmir_Design_Report.docx'));
  assert.ok(existsSync('dist/' + sources.ibbetson.readerUrl));
  assert.ok(existsSync('dist/' + sources.ibbetson.uploadedTextUrl));
});
check('Every curated passage matches the preserved uploaded text exactly', () => {
  const sha = createHash('sha256').update(uploadedBytes).digest('hex');
  assert.equal(sha, book.sha256);
  assert.equal(sha, sources.ibbetson.uploadedSha256);
  assert.equal(sha, context.window.COLLECTION.book.uploadedSourceSha256);
  const lines = fullText.split('\n');
  if (lines.at(-1) === '') lines.pop();
  assert.equal(lines.length, book.totalLines);
  assert.equal(book.passages.length, 98);
  assert.equal(new Set(book.passages.map(p => p.id)).size, book.passages.length);
  for (const passage of book.passages) {
    let previousEnd = 0;
    for (const segment of passage.segments) {
      assert.ok(segment.startLine > previousEnd, passage.id);
      assert.ok(segment.endLine >= segment.startLine, passage.id);
      assert.equal(segment.text, lines.slice(segment.startLine - 1, segment.endLine).join('\n'), passage.id);
      previousEnd = segment.endLine;
    }
  }
  for (const record of records) for (const claim of record.claims.filter(c => c.passageId)) {
    const passage = book.passages.find(p => p.id === claim.passageId);
    assert.ok(passage, record.id);
    assert.equal(claim.locator, passage.locator, record.id);
  }
});
check('Period, unresolved labels and disputed descent stay qualified', () => {
  assert.equal(book.accountYear, 1881);
  assert.equal(book.reportYear, 1883);
  assert.equal(book.editionYear, 1916);
  assert.ok(sources.ibbetson.date.includes('1881'));
  assert.ok(find('awan').claims.some(c => c.locator.includes('section 465')));
  assert.ok(!find('awan').claims.some(c => c.locator.includes('section 461')));
  for (const id of ['abbasi', 'khawaja', 'jasgam', 'jasra']) assert.equal(find(id).hasContext, false);
  assert.ok(!find('abbasi').aliases.some(a => a.name === 'Dhund'));
  assert.ok(!find('naru').aliases.some(a => a.name === 'Nam'));
  const kathia = core.qualifiedSummary(find('kathia'), sources);
  const ketwal = core.qualifiedSummary(find('ketwal'), sources);
  assert.ok(kathia.includes('not a verified continuity of descent'));
  assert.ok(ketwal.includes('not established ancestry'));
  assert.ok(kathia.includes('Reported tradition, not verified ancestry:'));
  for (const record of records.filter(r => r.historicalLocations)) {
    assert.ok(sources[record.locationSource].image);
    const summary = core.qualifiedSummary(record, sources);
    assert.ok(summary.includes('Separate historical examples (1881 account):'));
    assert.ok(summary.includes('This does not verify the poster examples.'));
  }
});
check('OCR search handles whitespace, punctuation, limits and upload line positions', () => {
  const text = bookCore.normaliseText('First\r\nQutb  Shah\nAwan\n[.*] <tag>\nqutb\nShah');
  const result = bookCore.searchText(text, 'qutb shah');
  assert.equal(result.matches.length, 2);
  const starts = bookCore.lineStarts(text);
  assert.equal(bookCore.lineAt(starts, result.matches[0].start), 2);
  assert.equal(bookCore.lineAt(starts, result.matches[1].start), 5);
  assert.equal(bookCore.searchText(text, '[.*]').matches.length, 1);
  assert.equal(bookCore.searchText(text, '<tag>').matches.length, 1);
  assert.equal(bookCore.searchText(text, '.*+?^${}()|[]\\').matches.length, 0);
  assert.equal(bookCore.searchText(text, 'a').matches.length, 0);
  assert.equal(bookCore.searchText(text, 'missing phrase').matches.length, 0);
  const capped = bookCore.searchText('awan '.repeat(300), 'awan');
  assert.equal(capped.matches.length, 250);
  assert.equal(capped.truncated, true);
  assert.equal(bookCore.searchText('awan '.repeat(250), 'awan').truncated, false);
  const snippet = bookCore.excerpt(text, result.matches[0], 4);
  assert.equal(snippet.hit, 'Qutb  Shah');
  assert.equal(text.slice(snippet.start, snippet.end), snippet.before + snippet.hit + snippet.after);
  const awan = bookCore.searchText(fullText, '465. The Awan');
  assert.equal(awan.matches.length, 1);
  assert.equal(bookCore.lineAt(bookCore.lineStarts(fullText), awan.matches[0].start), 24758);
});
check('Reader DOM bindings and static asset links resolve', () => {
  for (const [htmlFile, scriptFile] of [['dist/index.html','dist/app.js'],['dist/book.html','dist/book.js']]) {
    const html = readFileSync(htmlFile, 'utf8');
    const script = readFileSync(scriptFile, 'utf8');
    const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]);
    assert.equal(new Set(ids).size, ids.length, htmlFile);
    // Drawer controls are generated by app.js and are checked there too.
    const available = new Set([...ids, ...[...script.matchAll(/\bid="([^"]+)"/g)].map(m => m[1])]);
    for (const match of script.matchAll(/\$\('([^']+)'\)/g)) assert.ok(available.has(match[1]), match[1]);
    for (const match of html.matchAll(/(?:src|href)="([^"#]+)"/g)) {
      const path = match[1].split('#')[0];
      if (path.startsWith('http')) continue;
      assert.ok(existsSync('dist/' + path), path);
    }
  }
  const readerScript = readFileSync('dist/book.js', 'utf8');
  assert.ok(!readerScript.includes('innerHTML'), 'OCR must be rendered as text, never HTML');
});
console.log(`${checks} functional and content checks passed.`);
