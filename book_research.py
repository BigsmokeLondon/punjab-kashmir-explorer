"""Curated additions from the owner's uploaded Panjab Castes OCR.

Line locators refer to the preserved upload, not reconstructed page numbers.
Source wording is retained in the reader; summaries do not repeat caste rankings
or assertions about a community's character. Reported descent remains attributed.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent
TEXT_PATH = ROOT / 'dist/assets/sources/Panjab_Castes_uploaded.txt'

# Inclusive, one-based upload lines. Separate ranges explicitly omit intervening
# material (usually OCR of a large census table); the reader labels every gap.
SPECS = [
    ('edition', 'Edition and introductory note', 'Title page and introductory note', [(180, 196), (235, 288)], '1916'),
    ('classification', 'Jat and Rajput: changing census categories', 'Part III, sections 423–425', [(12750, 12909)], '425.'),
    ('chhadhar', 'Chhadhar', 'Part III, section 430, Chhadhar, No. 6', [(14773, 14783)], 'Chhadhar'),
    ('sipra', 'Sipra', 'Part III, section 430, Sipra, No. 7', [(14785, 14787)], 'Sipra'),
    ('langrial', 'Langrial', 'Part III, section 430, Langrial passage', [(14791, 14798)], 'Langrial'),
    ('tarar', 'Tarar', 'Part III, section 432, Tarar, No. 8', [(14888, 14898)], 'Tarar'),
    ('varaich', 'Varaich', 'Part III, section 432, Varaich, No. 9', [(14900, 14919)], 'Varaich'),
    ('sahi', 'Sahi', 'Part III, section 432, Sahi, No. 10', [(14921, 14927)], 'Sahi'),
    ('chima', 'Chima', 'Part III, section 432, Chima, No. 12', [(14941, 14952)], 'Chima'),
    ('bajwa', 'Bajwa and Bajju', 'Part III, section 432, Bajwa, No. 13', [(14954, 14968)], 'Bajwa'),
    ('dhillon', 'Dhillon', 'Part III, section 435, Dhillon, No. 1', [(15824, 15833)], 'Dhillon'),
    ('virk', 'Virk', 'Part III, section 435, Virk, No. 2', [(15835, 15845)], 'Virk'),
    ('chauhan', 'Chauhan', 'Part III, section 445, Chauhan, No. 2', [(18866, 18892)], 'Chauhan'),
    ('bhatti', 'Bhatti and Bhati', 'Part III, section 448, Bhatti, No. 2', [(21552, 21596)], 'Bhatti'),
    ('sial', 'Sial', 'Part III, section 450, Sial, No. 8', [(21746, 21791)], 'Sial'),
    ('ranjha', 'Ranjha', 'Part III, section 451, Ranjha, No. 9', [(21835, 21844)], 'Ranjha'),
    ('gondal', 'Gondal', 'Part III, section 451, Gondal, No. 10', [(21846, 21862)], 'Gondal'),
    ('tiwana', 'Tiwana', 'Part III, section 451, Tiwana, No. 12', [(21869, 21890)], 'Tiwana'),
    ('dhund-satti', 'Dhund and Satti', 'Part III, section 453, Dhund and Satti, Nos. 1–2', [(21934, 21935), (22600, 22637)], 'Satti'),
    ('ketwal', 'Ketwal', 'Part III, section 453, Ketwal, No. 3', [(22638, 22642)], 'Ketwal'),
    ('dhanial', 'Dhanial', 'Part III, section 453, Dhanial, No. 4', [(22644, 22651)], 'Dhanial'),
    ('gheba', 'Jodra and Gheba', 'Part III, section 454, Jodra and Gheba passage', [(22709, 22736)], 'Gheba'),
    ('janjua', 'Janjua', 'Part III, section 454, Janjua, No. 8', [(22738, 22768)], 'Janjua'),
    ('manhas', 'Manhas', 'Part III, section 455, Manhas, No. 9', [(22770, 22787)], 'Manhas'),
    ('chibh', 'Chibh', 'Part III, section 455, Chibh, No. 10', [(22789, 22805)], 'Chibh'),
    ('naru', 'Naru (OCR sometimes reads Nam)', 'Part III, section 457, Naru, No. 12', [(23678, 23690)], 'Naru'),
    ('gakkhar', 'Gakkhar', 'Part IV, Gakkhar, Caste No. 68', [(23975, 23986), (24721, 24757)], 'Gakkhar'),
    ('awan', 'Awan', 'Part IV, section 465, Awan, Caste No. 12', [(24758, 24763), (24848, 24920)], '465.'),
    ('khattar', 'Khattar', 'Part IV, section 467, Khattar, Caste No. 182', [(25049, 25074)], 'Khattar'),
    ('khokhar', 'Khokhar', 'Part IV, sections 468–469, Khokhar, Caste No. 58', [(25320, 25424)], 'Khokhar'),
    ('kharral', 'Kharral', 'Part IV, section 470, Kharral, Caste No. 77', [(25571, 25604)], 'Kharral'),
    ('kathia', 'Kathia', 'Part IV, section 472, Kathia passage', [(25675, 25751)], 'Kathia'),
    ('dogar', 'Dogar', 'Part IV, sections 474–475, Dogar, Caste No. 46', [(25785, 25842)], 'Dogar'),
    ('gujar', 'Gujar and Gujjar', 'Part IV, section 480, Gujar, Caste No. 8', [(26283, 26369)], '480.'),
    ('arain', 'Arain, Baghban and Maliar', 'Part IV, sections 485–486', [(27326, 27341), (29352, 29416)], 'Arain'),
    ('kamboh', 'Kamboh', 'Part IV, section 492, Kamboh, Caste No. 33', [(30272, 30316)], 'Kamboh'),
    ('mughal', 'Mughal', 'Part IV, section 507, Mughal, Caste No. 37', [(31582, 31617)], 'Mughal'),
    ('saiyad', 'Saiyad and Syed', 'Part V, section 515, Saiyads, Caste No. 24', [(32797, 32830)], 'Saiyads'),
    # Part II: Biloch and Pathan. The Derah Ghazi Khan entries follow a long census table.
    ('baloch', 'Biloch (Baloch): name, origin account and settlement', 'Part II, sections 375, 378 and 379', [(4284, 4315), (4430, 4452), (4486, 4497), (4526, 4568)], 'Biloch'),
    ('mazari', 'Mazari', 'Part II, section 382, Mazari, No. 11', [(4679, 4690)], 'Mazari'),
    ('drishak', 'Drishak (OCR heading reads Drlshak)', 'Part II, section 382, Drishak, No. 18', [(6420, 6428)], 'Rajanpur'),
    ('gurchani', 'Gurchani', 'Part II, section 382, Gurchani, No. 4', [(6430, 6445)], 'Dragal'),
    ('lund', 'Tibbi Lund and Sori Lund', 'Part II, sections 382–383, Lund, Nos. 8 and 49', [(6447, 6452), (6520, 6526)], 'Tibbi'),
    ('laghari', 'Laghari', 'Part II, section 382, Laghari, No. 22', [(6454, 6466)], 'Laghari'),
    ('khosa', 'Khosa', 'Part II, section 383, Khosa, No. 6', [(6503, 6518)], 'Khosa'),
    ('bozdar', 'Bozdar', 'Part II, section 383, Bozdar, No. 22', [(6528, 6538)], 'Bozdar'),
    ('qasrani', 'Qasrani', 'Part II, section 383, Qasrani, No. 16', [(6540, 6546)], 'Qasrani'),
    ('nutkani', 'Nutkani', 'Part II, section 383, Nutkani, No. 13', [(6548, 6553)], 'Nutkani'),
    ('niazi', 'Niazi', 'Part II, sections 399, 403 and 404, Niazi', [(10039, 10063), (10344, 10357), (10404, 10409), (10444, 10459)], 'Niazi'),
    # Part III: Jat tribes of the western plains, western sub-montane and Sikh tract.
    ('tahim', 'Tahim (OCR heading reads Tallim)', 'Part III, section 429, Tahim, No. 1', [(13810, 13822)], 'Tahim'),
    ('bhutta', 'Bhutta', 'Part III, section 429, Bhutta, No. 2', [(14694, 14704)], 'Bhutta'),
    ('langah', 'Langah', 'Part III, section 429, Langah, No. 3', [(14706, 14746)], 'Langah'),
    ('chhina', 'Chhina', 'Part III, section 429, Chhina, No. 4', [(14748, 14758)], 'Chhina'),
    ('sumra', 'Sumra', 'Part III, section 430, Sumra, No. 5', [(14760, 14771)], 'Sumra'),
    ('hinjra', 'Hinjra', 'Part III, section 432, Hinjra, No. 11', [(14928, 14939)], 'Hinjra'),
    ('deo', 'Deo', 'Part III, section 433, Deo, No. 14', [(14970, 14977)], 'Mahaj'),
    ('ghumman', 'Ghumman', 'Part III, section 433, Ghumman, No. 15', [(14979, 14983), (15737, 15739)], 'Ghumman'),
    ('kahlon', 'Kahlon', 'Part III, section 433, Kahlon, No. 16', [(15741, 15745)], 'Kahlon'),
    ('goraya', 'Goraya', 'Part III, section 433, Goraya, No. 18', [(15760, 15769)], 'Goraya'),
    ('sindhu', 'Sindhu', 'Part III, section 435, Sindhu, No. 3', [(15847, 15864)], 'Sindhu'),
    ('pannun', 'Pannun', 'Part III, section 436, Pannun, No. 10', [(17112, 17114)], 'Pannun'),
    ('aulak', 'Aulak', 'Part III, section 436, Aulak, No. 12', [(17119, 17123)], 'Aulak'),
    ('gil', 'Gil', 'Part III, section 436, Gil, No. 13', [(17125, 17131)], 'Shergil'),
    # Part III: Rajput tribes of the western plains, western hills and Jammu border.
    ('punwar', 'Punwar', 'Part III, section 448, Punwar, No. 1', [(21538, 21550)], 'Punwar'),
    ('wattu', 'Wattu', 'Part III, section 449, Wattu, No. 3', [(21645, 21676)], 'Wattu'),
    ('joya', 'Joya and Mahar', 'Part III, section 449, Joya, No. 4', [(21678, 21717)], 'Joya'),
    ('khichi', 'Khichi', 'Part III, section 449, Khichi, No. 5', [(21719, 21726)], 'Khichi'),
    ('dhudhi', 'Dhudhi', 'Part III, section 449, Dhudhi, No. 6', [(21731, 21738)], 'Dhudhi'),
    ('hiraj', 'Hiraj', 'Part III, section 450, Hiraj, No. 7', [(21740, 21744)], 'Hiraj'),
    ('mekan', 'Mekan', 'Part III, section 451, Mekan, No. 11', [(21864, 21867)], 'Mekan'),
    ('bhakral', 'Bhakral and Budhal', 'Part III, section 453, Bhakral, No. 5', [(22653, 22661)], 'Bhakral'),
    ('alpial', 'Alpial', 'Part III, section 453, Alpial passage', [(22663, 22669)], 'Alpial'),
    ('kanial', 'Kanial', 'Part III, section 453, Kanial, No. 6', [(22680, 22683)], 'Kanial'),
    ('kahut-mair', 'Kahut and Mair', 'Part III, section 454, Kahut, No. 7, and Mair', [(22685, 22707)], 'Kahut'),
    ('salahria', 'Salahria and Thakar', 'Part III, section 455, Thakar and Salahria, Nos. 11–12', [(22807, 22810), (22822, 22823), (22825, 22837)], 'Salahria'),
    ('raghbansi', 'Raghbansi', 'Part III, section 455, Raghbansi, No. 14', [(22842, 22847)], 'Raghbansi'),
    # Part IV: minor dominant, agricultural and pastoral tribes, and "foreign races".
    ('daudpotra', 'Daudpotra', 'Part IV, section 473, Daudpotra, Caste No. 79', [(25762, 25783)], 'Daudpotra'),
    ('gujar-tribes', 'Gujar tribes and clans', 'Part IV, section 482, Gujar tribes', [(27224, 27232)], 'Khatana'),
    ('shekh', 'Shekh (Sheikh) and its sub-divisions', 'Part IV, sections 501–502, Shekh, Caste No. 17', [(30738, 30754), (31164, 31193), (31357, 31373)], 'Shekh'),
    ('qureshi', 'Qureshi', 'Part IV, sections 501–502, Qureshi', [(31188, 31193), (31195, 31196), (31341, 31355)], 'Qureshi'),
    ('hans-khagga', 'Hans and Khagga', 'Part IV, sections 501 and 503, Hans and Khagga', [(31176, 31179), (31374, 31449)], 'Khagga'),
    ('nekokara', 'Nekokara and Jhandir', 'Part IV, section 504, Nekokara and Jhandir', [(31457, 31468)], 'Nekokara'),
    ('kasar', 'Kasar (Kassar) of Jhelum', 'Part IV, section 508, The Kasars of Jahlam', [(31720, 31736), (31748, 31750)], 'Kasars'),
    # Part V: religious, professional, mercantile and miscellaneous castes.
    ('bodla', 'Bodla', 'Part V, section 519, Bodla, Caste No. 172', [(33075, 33091)], 'Bodla'),
    ('nai', 'Nai', 'Part V, section 525, Nai, Caste No. 21', [(33459, 33476), (33487, 33519)], 'barber'),
    ('mirasi', 'Mirasi', 'Part V, section 527, Dum and Mirasi, Caste No. 25', [(34220, 34271)], 'Mirasi'),
    ('khojah-paracha', 'Khojah and Paracha', 'Part V, section 545, Khojah and Paracha, Caste Nos. 44 and 104', [(36858, 36868), (36876, 36925)], 'Paracha'),
    ('kashmiri', 'Kashmiri and Chibhali', 'Part V, section 557, Kashmiri, Caste No. 26', [(37721, 37733), (38371, 38407)], 'Chibhalis'),
    # Part VI: artisan and service castes (the book's heading is "vagrant, menial and artisan").
    ('mochi', 'Mochi', 'Part VI, section 607, Mochi, Caste No. 19', [(44132, 44151), (44162, 44173)], 'Mochi'),
    ('julaha', 'Julaha and Paoli', 'Part VI, section 612, Julaha and Paoli, Caste No. 9', [(44369, 44400)], 'Julaha'),
    ('machhi', 'Machhi and Men', 'Part VI, section 619, Machhi and Men, Caste No. 28', [(45507, 45538)], 'Machhi'),
    ('mallah', 'Mallah and Mohana', 'Part VI, section 621, Mallah and Mohana, Caste No. 42', [(45642, 45670)], 'Mallah'),
    ('lohar', 'Lohar', 'Part VI, section 624, Lohar, Caste No. 22', [(45777, 45792)], 'blacksmith'),
    ('tarkhan', 'Tarkhan', 'Part VI, section 627, Tarkhan, Caste No. 111', [(47402, 47424)], 'Tarkhan'),
    ('kumhar', 'Kumhar', 'Part VI, section 632, Kumhar, Caste No. 13', [(47618, 47643)], 'Kumhar'),
    ('sunar', 'Sunar (Zargar)', 'Part VI, section 634, Sunar, Caste No. 30', [(47705, 47723)], 'Zargar'),
    ('dhobi', 'Dhobi and Chhimba', 'Part VI, section 642, Dhobi and Chhimba, Caste Nos. 32 and 33', [(48187, 48205), (48214, 48219)], 'Dhobi'),
    ('teli-qassab', 'Penja, Teli and Qassab', 'Part VI, section 647, Penja, Teli and Qassab', [(49024, 49047)], 'Qassab'),
]
LOCATORS = {item[0]: item[2] for item in SPECS}


def claim(passage, title, text, status='context'):
    return {'title': title, 'text': text, 'status': status, 'source': 'ibbetson',
            'locator': LOCATORS[passage], 'passageId': passage}


def source_alias(name, note):
    return {'name': name, 'kind': 'Historical source spelling', 'note': note}


def related_alias(name, note):
    return {'name': name, 'kind': 'Related name in the source', 'note': note}


def modern_alias(name):
    return {'name': name, 'kind': 'Modern spelling, editorial search aid',
            'note': 'Added so the record can be found under a common present-day spelling. It does not come from the 1881 source.'}


# The book's own parts and section headings, lightly reworded. Every record belongs to exactly one.
GROUPS = {
    'baloch-pathan': ['baloch', 'mazari', 'drishak', 'gurchani', 'lund', 'laghari', 'khosa', 'bozdar', 'qasrani', 'nutkani', 'niazi'],
    'jat': ['jat', 'chhadhar', 'sipra', 'langrial', 'tarar', 'varaich', 'sahi', 'chima', 'bajwa', 'dhillon', 'virk',
            'tahim', 'bhutta', 'langah', 'chhina', 'sumra', 'hinjra', 'deo', 'ghumman', 'kahlon', 'goraya', 'sindhu', 'pannun', 'aulak', 'gil'],
    'rajput': ['rajput', 'bhatti', 'chauhan', 'janjua', 'chibb', 'minhas', 'naru', 'sial', 'tiwana', 'ranjha', 'gondal',
               'dhund', 'satti', 'ketwal', 'dhanial', 'gheba', 'punwar', 'wattu', 'joya', 'khichi', 'dhudhi', 'hiraj', 'mekan',
               'bhakral', 'alpial', 'kanial', 'kahut', 'mair', 'jodra', 'salahria', 'raghbansi'],
    'dominant': ['gakhar', 'awan', 'khattar', 'khokhar', 'kharral', 'kathia', 'dogar', 'daudpotra'],
    'agricultural': ['gujjar', 'arain', 'kamboh'],
    'foreign': ['mughal', 'qureshi', 'sheikh', 'hans', 'khagga', 'nekokara', 'jhandir', 'kassar'],
    'religious': ['syed', 'bodla', 'nai', 'mirasi', 'khoja', 'paracha', 'kashmiri'],
    'artisan': ['mochi', 'julaha', 'machhi', 'mallah', 'lohar', 'tarkhan', 'kumhar', 'sunar', 'dhobi', 'teli', 'qassab'],
    'project': ['sudhan', 'abbasi', 'khawaja', 'jasgam', 'jasra'],
}


def enrich(records, sources):
    source_bytes = TEXT_PATH.read_bytes()
    text = source_bytes.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
    lines = text.splitlines()
    passages = []
    for id, title, locator, ranges, expected in SPECS:
        segments = []
        for start, end in ranges:
            assert 1 <= start <= end <= len(lines), id
            segments.append({'startLine': start, 'endLine': end,
                             'text': '\n'.join(lines[start - 1:end])})
        assert expected.casefold() in '\n'.join(s['text'] for s in segments).casefold(), id
        passages.append({'id': id, 'title': title, 'locator': locator, 'segments': segments})
    sha = hashlib.sha256(source_bytes).hexdigest()
    reader = {'title': 'Panjab Castes', 'author': 'Denzil Ibbetson', 'accountYear': 1881,
              'reportYear': 1883, 'editionYear': 1916,
              'originalFilename': 'PANJAB  CASTES.txt', 'totalLines': len(lines),
              'sha256': sha, 'fullTextUrl': 'assets/sources/Panjab_Castes_uploaded.txt',
              'passages': passages}
    sources['ibbetson'].update({
        'date': '1881 census account, first published 1883; reprinted 1916',
        'readerUrl': 'book.html', 'uploadedTextUrl': reader['fullTextUrl'], 'uploadedSha256': sha,
        'limitation': 'A colonial census account using period-specific categories and prejudicial language. The 1916 introduction says its figures and boundaries were not updated. It records usage, traditions and the author\'s theories; it does not establish family ancestry or current distribution. The uploaded OCR contains errors.'
    })
    by_id = {r['id']: r for r in records}

    def extend(id, passage, context, places, tradition=None, summary=None, aliases=None, punjab=False):
        r = by_id[id]
        retained = [c for c in r['claims'] if c['source'] != 'ibbetson']
        added = [claim(passage, 'Historical source context (1881)', context)]
        if tradition:
            added.append(claim(passage, 'Origin account in the source', tradition, 'tradition'))
        # Keep the independently sourced AJK context first, and the poster qualification last.
        r['claims'] = [c for c in retained if c['status'] == 'context'] + added + [c for c in retained if c['status'] != 'context']
        r['historicalLocations'] = places
        r['historicalPassageId'] = passage
        r['hasContext'] = True
        r['sourceIds'] = list(dict.fromkeys(r['sourceIds'] + ['ibbetson']))
        if punjab and 'punjab' not in r['regions']:
            r['regions'].insert(0, 'punjab')
        if summary:
            r['summary'] = summary
        if aliases:
            r['aliases'].extend(aliases)

    extend('gujjar', 'gujar',
        'Ibbetson uses Gujar in his 1881 account. He records Gujrat and the Punjab foothills, and distinguishes cultivation in the plains from seasonal herding in the Jammu, Chibhal and Hazara hills. These are historical descriptions, not a rule for all Gujjar communities.',
        ['Gujrat', 'Jhelum', 'Gujranwala', 'Punjab foothills'],
        'The section repeats Cunningham\'s proposed identification with ancient Kushan or Yuchi populations. This is a nineteenth-century theory, not demonstrated continuity or a verified genealogy.',
        summary='Gujjar is recorded in both the AJK project directory and a historical Punjab account. The latter describes different local livelihoods and uses the spelling Gujar.',
        aliases=[source_alias('Gujar', 'Ibbetson uses this spelling in section 480. It links this source passage for comparison; it does not prove a shared ancestor.')], punjab=True)
    extend('jat', 'classification',
        'In sections 423–425 of the 1881 account, Ibbetson says Jat and Rajput classifications varied by district and that census offices grouped local tribal returns under broader heads. A census category here cannot be treated as a single genealogy.',
        ['Historical Punjab: district-dependent usage'],
        summary='Jat is a broad identity recorded in the AJK directory and historical Punjab material. The book shows why district, period and the particular group matter when interpreting the label.', punjab=True)
    extend('rajput', 'classification',
        'The 1881 account explicitly describes the same named tribe being classed as Rajput in one district and Jat in another. Ibbetson also acknowledges incomplete figures and uncertainty in the grouping of returns.',
        ['Salt Range', 'Jhang', 'Shahpur'],
        summary='Rajput is used as a broader identity in the project. Historical census classifications depended on local usage, so individual clan affiliations need their own evidence.', punjab=True)
    extend('awan', 'awan',
        'Section 465 places Awan in the Salt Range between the Jhelum and Indus and mentions extensions towards Jhang and Multan. The author notes that some Awan returns were grouped as Jat in western districts. This Punjab passage does not verify the poster\'s AJK districts.',
        ['Salt Range', 'Chakwal (western boundary in the account)', 'Jhang', 'Multan'],
        'Ibbetson records a Qutb Shah of Ghazni and Ali descent claim alongside several competing explanations proposed by colonial writers. None is accepted here as a proven common ancestry.',
        summary='Awan appears in the AJK project directory and in a substantial historical Salt Range entry. The book records census classification issues and conflicting origin accounts.', punjab=True)
    extend('mughal', 'mughal',
        'Section 507 records Mughal returns in Rawalpindi, Jhelum and other historical Punjab districts. Ibbetson argues that the census label included people also identified by local tribal names. His assessment is a source interpretation, not a verdict on any present-day family.',
        ['Rawalpindi', 'Jhelum', 'Gujrat'],
        summary='Mughal is a community label in the AJK directory and in the 1881 Punjab account. A recorded Mughal identity should be distinguished from a documented relationship to the imperial dynasty.', punjab=True)
    extend('syed', 'saiyad',
        'Section 515 uses Saiyad for a lineage title and discusses its returns across historical Punjab, including the Salt Range and Multan. The author acknowledges that the count cannot establish the ancestry of each person returned under that heading.',
        ['Salt Range', 'Multan'],
        'The source describes the title in terms of descent associated with Ali and Fatima. Recording a title or a community\'s claim does not authenticate a particular family genealogy.',
        summary='Syed is a lineage identity in the AJK directory. Ibbetson\'s Saiyad entry gives historical usage and census limitations, without verifying the Bhimber example or individual family descent.',
        aliases=[source_alias('Saiyad', 'Singular form used in the historical source.'), source_alias('Saiyads', 'Plural heading in section 515 of the historical source.')], punjab=True)
    extend('bhatti', 'bhatti',
        'Section 448 calls Bhatti the Punjab form of Bhati and records the name across several river valleys, Gujrat, Sialkot and the Salt Range. It describes both Rajput and Jat returns, so the label should be interpreted locally.',
        ['Gujrat', 'Sialkot', 'Salt Range', 'Lower Satluj and Indus valleys'],
        'The entry connects Bhatti with Yadu or Lunar descent and Jaisalmer traditions, and repeats Cunningham\'s ancient Kashmir reconstruction. These traditions and theories do not prove the ancestry of every Bhatti family.',
        summary='Bhatti is a widely recorded name in the historical Punjab account. The source explicitly links the spelling Bhati, while showing that census classification and local branches varied.',
        aliases=[source_alias('Bhati', 'Section 448 explicitly compares the Rajputana spelling Bhati with Punjab Bhatti. Apply this spelling link within the cited context.')])
    extend('chauhan', 'chauhan',
        'Section 445 discusses Chauhan under Rajput tribes of the eastern plains. It also records overlapping returns with other group names and warns that several figures appear under more than one heading. The account includes Rawalpindi and Gujranwala as well as eastern districts.',
        ['Rawalpindi', 'Gujranwala', 'Shahpur', 'Karnal and Ambala (wider historical Punjab)'],
        'The source places Chauhan within Agnikula and royal origin traditions. Such a classification is not evidence that every family using Chauhan or Chohan has an identical pedigree.',
        summary='Chauhan appears in the project clan chart and in Ibbetson\'s eastern plains discussion. The book is useful for checking overlapping census names and the limits of a single broad classification.')
    extend('janjua', 'janjua',
        'Section 454 locates the Janjua entry in the eastern Salt Range and treats it among Rajput tribes of that tract. The uploaded OCR misspells the heading as Januja; this is retained in the source reader, not added as a confirmed name variant.',
        ['Eastern Salt Range', 'Jhelum'],
        'Ibbetson presents different explanations attributed to Cunningham, Griffin and local genealogies, including a Raja Mal Rathor tradition. The competing accounts are not reconciled here into a settled lineage.',
        summary='Janjua has a dedicated Salt Range entry in the historical source. Its geographical context is clearer than the competing explanations of ancestral origin.')
    extend('minhas', 'manhas',
        'Section 455 uses Manhas under Jammu-border Rajputs and records Rawalpindi, Jhelum and Sialkot. It discusses Jamwal and Manhas as related labels within its account, but this does not justify merging all present-day families using those names.',
        ['Rawalpindi', 'Jhelum', 'Sialkot', 'Jammu border'],
        'The entry records Solar descent from Ram Chandra and several routes of migration. These are reported origin narratives, not an independently established family genealogy.',
        summary='The project uses Minhas and pairs it with Manhas. The historical Manhas entry supplies Jammu-border context; the connection should still be checked for the particular family and locality.')
    extend('chibb', 'chibh',
        'Section 455 uses Chibh and places the entry around northern Gujrat and the Jammu hills. It reports a Bhimbar settlement tradition and discusses the name Chibhal in historical Kashmir geography.',
        ['Northern Gujrat', 'Jammu hills', 'Bhimbar (reported settlement tradition)'],
        'The entry reports Katoch descent and a Chib Chand migration story, but Ibbetson doubts the ancestry explanation and suggests another possibility. Neither his doubt nor his alternative theory settles the genealogy.',
        summary='Chibb is linked to Chibh in the historical Jammu-border entry. The source distinguishes recorded geography from disputed explanations of descent.')
    extend('naru', 'naru',
        'Section 457 places Naru around Jalandhar and Hoshiarpur in its eastern hills discussion. The uploaded OCR sometimes renders Naru as Nam, while correctly reading Naru later in the same passage. This does not support the poster\'s southern Punjab locality example.',
        ['Jalandhar and Hoshiarpur (wider historical Punjab)'],
        'The entry reports different Lunar and Solar origin accounts in the two districts. A shared name is insufficient to resolve those stories or prove a Narwa equivalence.',
        summary='The historical Naru passage concerns the eastern part of historical Punjab. Its geography and conflicting origin accounts need to remain separate from the project\'s southern Punjab example.')
    extend('sial', 'sial',
        'Section 450 places Sial in Jhang and the Chenab country. Quoting Steedman, it describes pastoral activity in the river lowlands and Jhang bar and the rise of Sial chiefs. This is a dated account of particular regional histories.',
        ['Jhang', 'Chenab valley', 'Jhang bar'],
        'The account gives incompatible versions of a Rai Shankar origin narrative linking Sial, Tiwana and Gheba. It records a tradition of relationship, not demonstrated descent from a common ancestor.',
        summary='Sial has a substantial Jhang entry in the book, covering pastoral geography and chiefly history. The origin stories linking other groups remain explicitly attributed.')
    extend('ranjha', 'ranjha',
        'Section 451 places Ranjha between the Jhelum and Chenab in Shahpur and Gujrat. Although included under Rajput tribes, most returns outside Shahpur were Jat, and Ibbetson himself says the entry might have been better classed as Jat.',
        ['Shahpur', 'Gujrat', 'Jhelum–Chenab uplands'],
        'The source presents a Bhatti association and reports a Qureshi origin claim in Gujrat. This disagreement should be retained as source context, not resolved into one universal lineage.',
        summary='Ranjha illustrates the book\'s classification uncertainty: the discussion heading, recorded returns and author\'s preferred category do not fully agree.')
    extend('tiwana', 'tiwana',
        'Section 451 places Tiwana at the foot of the Shahpur Salt Range and names Mitha Tiwana. It discusses a chiefly family\'s history and describes pastoral and agricultural activity in its period.',
        ['Shahpur Salt Range', 'Mitha Tiwana'],
        'The entry says Tiwana are of Punwar origin and share an ancestor with Sial and Gheba. The related Sial passage gives different versions of that relationship, so common descent remains a reported tradition.',
        summary='Tiwana is recorded around Mitha Tiwana and the Shahpur Salt Range. The history of its chiefly family should be distinguished from claims about every Tiwana branch.')
    extend('gakhar', 'gakkhar',
        'The Gakkhar entry in Part IV discusses the northern cis-Indus Salt Range tract; section 464 then describes Rawalpindi and Jhelum localities. The source treats Gakkhar separately from Khokhar, despite historical confusion between their names.',
        ['Rawalpindi', 'Jhelum', 'Northern cis-Indus Salt Range tract'],
        'Ibbetson reports a Kayani or Ispahan origin story and disputes the story of arrival with Mahmud of Ghazni. This records an argument within the source, not a verified conclusion about family ancestry.',
        summary='Gakhar is listed with related spellings in the project. The historical Gakkhar entry provides a separate regional discussion, rather than settling the project chart\'s Rajput grouping.')
    extend('khokhar', 'khokhar',
        'Sections 468–469 discuss Khokhar under separate Khokhar, Rajput and Jat returns. Ibbetson admits he cannot yet say exactly how much of the grouping came from household returns and how much from census office decisions. He distinguishes Khokhar from Gakkhar.',
        ['Jhelum valley', 'Chenab valley', 'Jhang', 'Shahpur'],
        summary='Khokhar has a dedicated historical discussion of mixed census classifications. It remains a distinct record from Gakhar; resemblance between names is insufficient to merge them.')
    extend('dogar', 'dogar',
        'Sections 474–475 place Dogar along the upper Satluj and Beas and mention extensions towards Sialkot. The quoted accounts concern particular districts and branches, rather than a verified current distribution.',
        ['Upper Satluj and Beas valleys', 'Lahore', 'Sialkot'],
        'Brandreth reports a Chauhan origin explanation, while Purser reports Chauhan and Punwar claims. Ibbetson proposes another explanation using appearance and customs; those methods do not demonstrate ancestry. Dogan remains an unconfirmed project label.',
        summary='Dogar is recorded along the Satluj and Beas in the book. Its reported Rajput origins and the author\'s alternative explanation remain qualified, and the Dogan pairing still needs verification.')

    def add(id, name, passage, classification, places, summary, context, tradition=None, caution=None, aliases=None, type='clan', regions=('punjab',)):
        cs = [claim(passage, 'Historical source context (1881)', context)]
        if tradition:
            cs.append(claim(passage, 'Origin account in the source', tradition, 'tradition'))
        warning = caution or 'This is a description from the 1881 account, reprinted in 1916. Its census category and locality examples do not establish current distribution, every branch\'s identity or a shared genealogy. Origin stories remain attributed traditions.'
        cs.append(claim(passage, 'Limits of this entry', warning, 'verify'))
        records.append({'id': id, 'name': name, 'regions': list(regions), 'type': type,
                        'classification': classification, 'classificationSource': 'ibbetson',
                        'aliases': aliases or [], 'locations': places, 'locationSource': 'ibbetson',
                        'locationLocator': LOCATORS[passage], 'locationPassageId': passage,
                        'localityLabel': 'Historical examples (1881)',
                        'summary': summary, 'caution': warning, 'hasContext': True,
                        'claims': cs, 'sourceIds': ['ibbetson'],
                        'question': 'Check the cited passage and the exact branch or locality. Retain the 1881 context, and attribute any origin narrative before adapting this for a post.'})

    add('chhadhar', 'Chhadhar', 'chhadhar', 'Jat discussion; many Jhang returns recorded as Rajput (1881)', ['Jhang', 'Chenab valley', 'Ravi valley'],
        'Chhadhar is recorded in the Chenab and Ravi valleys, particularly Jhang. Its placement in a Jat discussion coexists with Rajput returns.',
        'Section 430 describes Chhadhar along both valleys and says many in Jhang returned themselves as Rajput. These are local census categories, not a complete genealogy.',
        'The entry reports descent from Raja Tur, a Tunwar, and a migration through Bahawalpur and Uch to Jhang. The narrative is a reported tradition, not established ancestry.')
    add('sipra', 'Sipra', 'sipra', 'Listed in the western plains Jat discussion (1881)', ['Jhang', 'Jhelum valley', 'Lower Chenab'],
        'Sipra has a short entry centred on Jhang and the Jhelum and lower Chenab valleys.',
        'Section 430 records Sipra in those river valleys, with Jhang as its main example. The uploaded OCR renders the proposed parent name unclearly, so it is not used as a confirmed alias.',
        'Ibbetson tentatively describes Sipra as a subdivision of another Jat group. His tentative wording does not establish that relationship for every family.')
    add('langrial', 'Langrial', 'langrial', 'Pastoral group in the western plains discussion (1881)', ['Multan steppes', 'Rawalpindi', 'Sialkot', 'Kot Kamalia (historical account)'],
        'Langrial is described in a pastoral setting in the Multan steppes, with Rawalpindi and Sialkot also named.',
        'Section 430 says Langrial was not separately shown in its abstract. The prose records Multan and other district examples; this is a reminder that absence from a summary table need not mean absence from the source.',
        'The passage contrasts Solar Rajput claims with a Multan account of descent from a Brahman Charan of Bikaner. It also reports a migration through Jhang and Kot Kamalia. The competing narratives remain traditions.')
    add('tarar', 'Tarar', 'tarar', 'Jat discussion with Rajput returns in some districts (1881)', ['Upper Chenab', 'Gujrat', 'Gujranwala', 'Shahpur'],
        'Tarar is recorded near the meeting of Gujrat, Gujranwala and Shahpur along the upper Chenab.',
        'Section 432 treats Tarar among western submontane Jat tribes but notes substantial Rajput returns in Gujranwala and Shahpur. Keep the district-specific category attached to its period.',
        'The section reports a Solar or Bhatti origin claim and different stories dating settlement to Mahmud of Ghazni or Humayun. They are not a single established chronology.')
    add('varaich', 'Varaich', 'varaich', 'Listed among western submontane Jat tribes (1881)', ['Gujrat', 'Gujranwala', 'Wazirabad', 'Lahore (name usage)'],
        'Varaich is the spelling used in the book. The entry centres on Gujrat and Gujranwala and discusses a Wazirabad family.',
        'Section 432 records Varaich in Gujrat and Gujranwala, mentions the Wazirabad family in Sikh-period history, and says Chung was also used in Lahore. That local naming statement is not a universal equivalence.',
        'The entry gives different Jat, Solar Rajput and Raja Karan origin stories. None is accepted here as a verified common pedigree.',
        aliases=[source_alias('Chung', 'Section 432 reports interchangeable usage in Lahore only. Check the locality and family before treating it as the same identity elsewhere.')])
    add('sahi', 'Sahi', 'sahi', 'Listed among western submontane Jat tribes (1881)', ['Gujrat', 'Sialkot'],
        'Sahi has a short historical entry whose locality examples are Gujrat and Sialkot.',
        'Section 432 records Sahi in Gujrat and Sialkot. Its statements about customs concern the author\'s period and should not be generalized to present-day communities.',
        'The source reports Solar Rajput descent and a story of movement through Ghazni to the Ravi near Lahore. This is an attributed origin account.')
    add('chima', 'Chima', 'chima', 'Listed among western submontane Jat tribes (1881)', ['Sialkot', 'Gujranwala'],
        'Chima is the book\'s spelling for this entry. The account places it particularly in Sialkot and Gujranwala.',
        'Section 432 lists Chima among Jat tribes, names Sialkot and Gujranwala, and identifies Nagara as one of its clans in that account.',
        'A Chauhan ancestor and movement from Delhi through Kangra and Amritsar are reported traditions. Ibbetson also infers origin from customs; such inference is not genealogical proof.')
    add('bajwa', 'Bajwa', 'bajwa', 'Bajwa Jat and Bajju Rajput labels discussed (1881)', ['Bajwat', 'Sialkot', 'Jammu border'],
        'The Bajwa entry connects the name with Bajwat in Sialkot and records Bajwa and Bajju labels within its local account.',
        'Section 432 describes Bajwa Jats and Bajju Rajputs in the Bajwat. The source records a relationship between those labels; this does not make them interchangeable for every family.',
        'The two-brothers explanation of Jat and Rajput branches and a different Delhi migration story are reported origin traditions, not independently verified genealogies.',
        aliases=[source_alias('Bajju', 'The entry uses Bajju for a Rajput label in the Bajwat. It is included for searching this passage, with its local and branch-specific distinction retained.')])
    add('dhillon', 'Dhillon', 'dhillon', 'Listed among Jat tribes of the Sikh tract (1881)', ['Gujranwala', 'Amritsar (wider historical Punjab)', 'Upper Satluj'],
        'Dhillon is discussed among Jat tribes of the Sikh tract, with Gujranwala, Amritsar and the upper Satluj named.',
        'Section 435 records Dhillon across those areas. Ibbetson questions whether Delhi returns under the same name refer to the same group, showing why names should be checked locally.',
        'The section reports a Saroha and Sirsa origin account and another involving a Solar ancestor in Malwa. The alternatives remain source traditions.')
    add('virk', 'Virk', 'virk', 'Jat discussion with some Gujranwala Rajput returns (1881)', ['Gujranwala', 'Lahore'],
        'Virk is recorded especially in Gujranwala and Lahore. The account includes mixed census returns and regional political history.',
        'Section 435 lists Virk in the Jat discussion but records a portion of Gujranwala returns as Rajput. It describes regional political power before subjugation by Ranjit Singh.',
        'The section reports descent from a Manhas ancestor called Virak and a route from Jammu to Amritsar and Gujranwala. This is a recorded tradition, not proof of a shared ancestry.')
    add('gondal', 'Gondal', 'gondal', 'Both Rajput and Jat descriptions in the account (1881)', ['Gondal bar', 'Shahpur', 'Gujrat', 'Jhelum'],
        'Gondal is recorded in the uplands between the Jhelum and Chenab. The author warns against assuming that every regional use of the name refers to the same group.',
        'Section 451 places the plains Gondal in Shahpur, Gujrat and Jhelum. It records overlapping Chauhan returns and says the author does not know the relationship to Gondal names in Kangra and Hoshiarpur.',
        'The source reports a Chauhan association and a conversion story involving Baba Farid at Pakpattan. Neither establishes the genealogy of every Gondal branch.')
    add('kharral', 'Kharral', 'kharral', 'Separate Kharral, Rajput and Jat returns discussed (1881)', ['Ravi valley', 'Montgomery (historical district)', 'Lahore', 'Gujranwala'],
        'Kharral is the spelling used in the source, which places the entry mainly along the Ravi.',
        'Section 470 discusses Kharral under several census headings and records the Ravi valley from its Chenab junction towards the Lahore–Montgomery boundary. The district names and limits belong to the historical account.',
        'The Montgomery origin account claims descent from Raja Karan. It is reported as a tradition, not authenticated here.')
    add('kathia', 'Kathia', 'kathia', 'Punwar returns interpreted as Kathia by the author (1881)', ['Ravi valley', 'Multan', 'Montgomery (historical district)', 'Southern Jhang'],
        'Kathia illustrates a gap between a known group name and the census table: Ibbetson interprets some Punwar returns as referring to Kathia.',
        'Section 472 places Kathia in the Ravi valley of Multan and Montgomery and in southern Jhang. It says Kathia was not a separate table heading, then gives a locally investigated interpretation of Punwar returns.',
        'The passage presents a Khattya origin story and a proposed identification with ancient Kathaioi encountered by Alexander. That identification is nineteenth-century speculation, not demonstrated historical continuity.',
        caution='The link to Alexander\'s Kathaioi is a colonial-era hypothesis, not a verified continuity of descent. The census reconstruction is also an interpretation. Keep the 1881 localities and classifications dated, and verify particular branches separately.')
    add('arain', 'Arain', 'arain', 'Community and occupational uses distinguished locally (1881)', ['Lahore', 'Rawalpindi division (historical)', 'Multan division (historical)', 'Satluj valley'],
        'Arain is discussed alongside Baghban and Maliar. The book distinguishes community labels from occupational usage and acknowledges errors in its tables.',
        'Sections 485–486 say these labels could denote gardening occupations in parts of western Punjab, while Arain had more specific community usage elsewhere. Ibbetson notes that Rawalpindi and Jhelum Maliar returns had been misentered as Maniar in a table.',
        'The source reports different Delhi, Uch and Multan origin traditions and a supposed relationship to Kamboh. Such reports do not establish a universal identity or common ancestry between the communities.',
        aliases=[source_alias('Rain', 'Section 485 reports this form on the Jamna. Baghban and Maliar are discussed as context-dependent labels, not added as universal Arain aliases.')], type='community')
    add('kamboh', 'Kamboh', 'kamboh', 'Separate agricultural community entry in the account (1881)', ['Upper Satluj valley', 'Montgomery (historical district)', 'Lahore'],
        'Kamboh has a dedicated entry covering cultivation, other livelihoods and regional naming. The source does not consistently equate it with Arain.',
        'Section 492 places Kamboh along the upper Satluj to Montgomery and records Muslim Kamboh as well as Muslim Arain in places including Lahore. It also describes trade, military and office work; these are historical observations.',
        'Raja Karan, Kashmir, Persian and Ghazni connections appear as different reported explanations. The proposed relationship to Arain is discussed rather than proven.', type='community')
    add('dhund', 'Dhund', 'dhund-satti', 'Listed in the Murree and Hazara hills Rajput discussion (1881)', ['Northern Rawalpindi', 'Murree hills', 'Hazara (outside current Punjab/AJK browsing scope)'],
        'Dhund is discussed with Satti in the historical Murree and Hazara hills account. The passage contains several origin narratives that require qualification.',
        'Section 453 places Dhund north of Satti in the right-bank Jhelum hills of Rawalpindi and Hazara. This is nineteenth-century geography, not a definition of all present-day Dhund localities.',
        'The section records a claim to Abbas, the Prophet\'s paternal uncle, alongside a Takht Khan and Kulu Rai narrative. Ibbetson offers his own alternatives. None verifies Abbasid descent or a universal equivalence with the project\'s Abbasi label.')
    add('satti', 'Satti', 'dhund-satti', 'Listed in the Murree and Hazara hills Rajput discussion (1881)', ['Rawalpindi hills', 'Right-bank Jhelum hills'],
        'Satti is placed south of Dhund in the book\'s hill-tribe discussion. The entry preserves disagreement about their proposed relationship.',
        'Section 453 records Satti in the Rawalpindi and Hazara hill setting. It describes the relative position of Satti and Dhund, using the district limits of that period.',
        'The source says Satti reject an origin story connecting them to Dhund and instead claim Nausherwan descent. These are attributed and conflicting traditions, not settled ancestry.')
    add('khattar', 'Khattar', 'khattar', 'Separate entry; some returns included under Awan (1881)', ['Kala Chitta Pahar', 'Indus near Attock', 'Historical Rawalpindi district'],
        'Khattar has a dedicated entry for the Kala Chitta tract. Its census grouping and proposed relationship to Awan are not identical questions.',
        'Section 467 places Khattar around Kala Chitta Pahar and says Rawalpindi Khattar returns were included under Awan, making the separate table figures incomplete.',
        'The passage reports a Qutb Shah claim and disputed Awan kinship, alongside other origin theories. A shared census heading does not establish a proven family relationship.')
    add('gheba', 'Gheba', 'gheba', 'Discussed with Jodra; census identity uncertain (1881)', ['Fateh Jhang', 'Pindi Gheb', 'Historical Rawalpindi district'],
        'Gheba is discussed alongside Jodra in the Salt Range material. The author explicitly admits uncertainty about its census returns and one relationship account.',
        'Section 454 places Gheba in the Fateh Jhang and Pindi Gheb area of the then Rawalpindi district. Ibbetson says returns may have appeared under other broad headings instead of Gheba.',
        'The Sial–Tiwana–Gheba shared-ancestor story and a proposed Jodra branch relationship are reported claims. Ibbetson even says he cannot remember the authority for the latter, so neither is treated as a proven genealogy.')
    add('dhanial', 'Dhanial', 'dhanial', 'Hill-tribe discussion; most returns recorded as Jat (1881)', ['Dhani country', 'Chakwal', 'Lower western Murree hills'],
        'Dhanial is recorded in the Dhani country of Chakwal and in the lower western Murree hills.',
        'Section 453 discusses Dhanial with the hill tribes, mentions a Chakwal colony and the Murree range, and says most returns were recorded as Jat. The author\'s Rajput-origin suggestion is an interpretation.',
        'The source reports a descent claim associated with Ali. The statement records a tradition, not an authenticated lineage.')
    add('ketwal', 'Ketwal', 'ketwal', 'Listed in the Murree and Hazara hills discussion (1881)', ['Hills south of the Satti country', 'Right-bank Jhelum hill group'],
        'Ketwal has a brief entry placing it south of the Satti country within the same historical hill group.',
        'Section 453 locates Ketwal relative to Satti and Dhund. Its remarks about population size and past conflict are period-specific and are not used here as current figures.',
        'The entry reports a claim of descent from Alexander the Great. It supplies no demonstrated genealogy connecting present-day Ketwal families to Alexander.',
        caution='Alexander descent is an attributed claim in the source, not established ancestry. This short nineteenth-century passage cannot define current population size, all localities or every family\'s identity.')

    # Second expansion: further Pakistani Punjab entries, Kashmiri settlers, and occupational groups.
    period_remarks = 'The passage quotes harsh nineteenth-century official judgments of the group\'s conduct. They are period opinions, not evidence about any family, and are not repeated here. '
    default_limits = 'This is a description from the 1881 account, reprinted in 1916. Its census category and locality examples do not establish current distribution, every branch\'s identity or a shared genealogy. Origin stories remain attributed traditions.'
    occupational = 'This is the 1881 account of an occupation and the people recorded under it. Census occupational headings did not define descent, and present-day families using the name may have different histories, work and self-designations. The source\'s social rankings are prejudices of its period, not facts about the community.'

    # Part II: Biloch (Baloch) and Pathan.
    add('baloch', 'Baloch', 'baloch', 'Frontier tribal nation; the name also used for camel-keepers (1881)',
        ['Derah Ghazi Khan (historical district)', 'Rajanpur', 'Muzaffargarh', 'Multan (Satluj)', 'Montgomery (historical district)', 'Jhang', 'Shahpur'],
        'Baloch, written Biloch in the source, is described as a tribal nation of the lower Sulemans with settlements along the western Punjab rivers. The book also shows the word being used for camel-keepers of any descent.',
        'Section 375 lists four uses of "Biloch" in 1881 Punjab, including any Muslim camelman in several divisions, and says true Biloch and camelmen could not be separated in the figures. Section 379 contrasts the organised tribes of Derah Ghazi Khan with Biloch settlers along the Indus, Chenab, Jhelum, Ravi and Satluj who owed no allegiance to a tribal chief.',
        'Section 378 records the Biloch account of descent from Mir Hamzah and a migration through Aleppo, Kirman and Makran. The author adds his own belief that all Biloch tribes counted themselves in either the Rind or the Lashari division. Section 379 links Mir Chakar and Humayun\'s return to Biloch settlement in Montgomery. These remain reported traditions.',
        caution='The 1881 figures mix people of Biloch descent with anyone called Biloch because they kept camels, as the author himself says. Tribal and district names belong to that period; they do not establish a family\'s descent or current distribution.',
        aliases=[source_alias('Biloch', 'Spelling used throughout the 1881 source.'), modern_alias('Baluch')], type='community')
    add('mazari', 'Mazari', 'mazari', 'Organised Biloch tribe of Derah Ghazi Khan (1881)',
        ['Southern Derah Ghazi Khan', 'Rojhan', 'Sindh frontier (outside scope)'],
        'Mazari is recorded as the southernmost organised Biloch tribe of Derah Ghazi Khan, between the hills and the Indus.',
        'Section 382 places the Mazari in the south of Derah Ghazi Khan, extending over the Sindh frontier, with Rojhan (OCR: Eoihan) as headquarters. It names four clans, Rustamani, Masidani, Balachani and Sargani, and says the chief was a Balachani.',
        'The tribe traces descent from Hot, son of Jalal Khan, and reports a seventeenth-century move from Sindh after a quarrel with the Chandia. These are attributed accounts.')
    add('drishak', 'Drishak', 'drishak', 'Biloch tribe of Derah Ghazi Khan, scattered along the Indus (1881)',
        ['Asni, near Rajanpur', 'Between the Pitok and Sori passes', 'Indus riverbank'],
        'Drishak is described as the most scattered of the Derah Ghazi Biloch tribes, with many villages among a Jat population on the Indus.',
        'Section 382 says the Drishak held no part of the hills and lived between the Pitok and Sori passes, with headquarters at Asni near Rajanpur. It lists the Kirmani, Mingwani, Gulfaz, Sargani, Arbani and Jiskani sections.',
        'The tribe is placed in the Rind section but claims descent from Hot, son of Jalal Khan, and is said to have come down to the plains in the late seventeenth century. These are reported traditions.',
        aliases=[modern_alias('Dreshak')])
    add('gurchani', 'Gurchani', 'gurchani', 'Organised Biloch tribe holding the Mari and Dragal hills (1881)',
        ['Mari and Dragal hills', 'Derah Ghazi Khan (historical district)'],
        'Gurchani is recorded in the Mari and Dragal hills of Derah Ghazi Khan, with some clans then living beyond the British border.',
        'Section 382 says the Gurchani had eleven clans, among them Durkani, Shekhani, Lashari, Petafi, Jiskani and Sabzani, and that all the Durkani and about half the Lashari lived beyond the border. It warns that some Lashari may have been counted in a separate Lashari tribe.',
        'Only some clans are described as of Biloch or Rind descent. The rest are said to descend from Gorish, a grandson of a Raja of Haidarabad who was adopted by the Biloches and is linked to Humayun. These are attributed accounts.',
        caution=period_remarks + default_limits)
    add('lund', 'Lund', 'lund', 'Two Biloch tribes: Tibbi Lund and Sori Lund (1881)',
        ['Within the Gurchani country (Tibbi Lund)', 'Between the Khosa tracts to the Indus (Sori Lund)', 'Derah Ghazi Khan (historical district)'],
        'The book distinguishes two Lund tribes in Derah Ghazi Khan, Tibbi Lund and Sori Lund, and warns that their census figures were mixed up.',
        'Sections 382–383 describe Tibbi Lund as a small area within the Gurchani country, made up of Lund, Rind and Khosa sections recently united under one chief, and Sori Lund as a small tribe whose land divided the Khosa territory. The author says the figures for the two cannot be trusted.',
        'Tibbi Lund sections are described as of Rind origin, while Sori Lund are said not to be pure Biloch. These classifications are the source\'s, not a verified genealogy.',
        aliases=[source_alias('Tibbi Lund', 'Name used in section 382 for the Lund within the Gurchani country.'), source_alias('Sori Lund', 'Name used in section 383 to distinguish the second Lund tribe.')])
    add('laghari', 'Laghari', 'laghari', 'Organised Biloch tribe of Derah Ghazi Khan (1881)',
        ['Chhoti Zerin (headquarters)', 'Derah Ghazi Khan hills', 'Derah Ismail Khan (outlying, outside scope)', 'Muzaffargarh (outlying)'],
        'Laghari is recorded north of the Gurchani in Derah Ghazi Khan, with headquarters at Chhoti Zerin and outlying settlements elsewhere.',
        'Section 382 places the Laghari between the Kura pass and a pass a little north of Derah (the OCR is garbled; it appears to be Sakhi Sarwar), and names the Haddiani, Aliani, Bughlani and Haibatani sections. It says outlying settlements in Derah Ismail Khan and Muzaffargarh owed no allegiance to the tribe, and that the Talpur dynasty of Sindh belonged to it.',
        'The source calls the Laghari of pure Rind origin and says they settled at Chhoti Zerin after returning from accompanying Humayun. These are reported traditions.',
        caution=period_remarks + default_limits, aliases=[modern_alias('Leghari')])
    add('khosa', 'Khosa', 'khosa', 'Organised Biloch tribe of Derah Ghazi Khan (1881)',
        ['Between the Laghari and Qasrani country', 'Derah Ghazi Khan (historical district)', 'Bahawalpur', 'Sindh (outside scope)'],
        'Khosa is recorded between the Laghari and Qasrani in Derah Ghazi Khan, its land split into northern and southern parts by Lund territory.',
        'Section 383 describes Khosa territory running from the hills nearly to the Indus, a group in Bahawalpur, and lands in Sindh said to have been granted by Humayun for military service. It lists six clans, one of them described as a Khetran offshoot.',
        'They are said to have first settled in Kech and are called true Rinds. These are attributed origin statements.',
        caution=period_remarks + default_limits)
    add('bozdar', 'Bozdar', 'bozdar', 'Biloch tribe beyond the 1881 frontier, with settlers near Rajanpur',
        ['Hills behind the Qasrani country (beyond the 1881 border)', 'Around Rajanpur', 'Among the Laghari'],
        'Bozdar is described as a tribe beyond the 1881 frontier. Over 2,000 were counted inside Punjab, almost all in Derah Ghazi Khan.',
        'Section 383 places the Bozdar between the Sanghar pass and the Khosa and Khetran country, and says those living in scattered villages around Rajanpur and among the Laghari had no connection with the parent tribe. It names nine clans and describes the tribe as great graziers.',
        'The source calls them of Rind extraction and repeats a derivation of the name from the Persian word for goat. Both are attributed statements.')
    add('qasrani', 'Qasrani', 'qasrani', 'Northernmost organised Biloch tribe (1881)',
        ['Hills on the boundary of the two Derahs', 'Derah Ghazi Khan (historical district)'],
        'Qasrani is recorded as the northernmost organised Biloch tribe, in the hills and sub-montane strip on the boundary of Derah Ghazi Khan and Derah Ismail Khan.',
        'Section 383 gives a written form of the name meaning "Imperial" (the OCR is garbled; it appears to be Qaisarani), lists seven clans, Lashkarani, Khubdin, Budani, Vaswani, Laghari, Jarwar and Rustamani, and records the tribe in Punjab mainly in the Derah district.',
        'The source calls the Qasrani of Rind origin. This is a reported classification.',
        aliases=[modern_alias('Qaisrani')])
    add('nutkani', 'Nutkani', 'nutkani', 'Former organised Biloch tribe of the Sanghar country (1881)',
        ['Sanghar country', 'Between the northern Khosa and the Qasrani', 'Derah Ghazi Khan (historical district)'],
        'Nutkani is recorded as a tribe peculiar to Derah Ghazi Khan that had lost its political organisation but kept much of its tribal coherence.',
        'Section 383 says the Nutkani held a compact tract to the Indus between the northern Khosa and the Qasrani, once held superior rights over the Sanghar country, and lost their tribal organisation early in Ranjit Singh\'s rule.')
    add('niazi', 'Niazi', 'niazi', 'Pathan tribe of the Lodi branch (1881)',
        ['Isa Khel', 'Mianwali', 'Bannu district (historical)'],
        'Niazi is discussed among the Pathan tribes of the historical Bannu district, holding Isa Khel and the country around Mianwali.',
        'Sections 399, 403 and 404 trace Niazi movement from Tank across the Salt Range into Isa Khel and Mianwali, name the Isa Khel, Mushani and Sarhang divisions, and note that the Niazi spoke Hindko, especially east of the Indus.',
        'The source places the Niazi in the Lodi branch of Pathans, descended from an ancestor called Niazai, and says one Niazi was governor of Lahore in the Lodi and Sur period. These are the source\'s historical accounts, not a family genealogy.')

    # Part III: Jat tribes.
    add('tahim', 'Tahim', 'tahim', 'Listed among Jat tribes of the western plains (1881)',
        ['Chiniot (Jhang)', 'Bahawalpur', 'Multan', 'Muzaffargarh', 'Derah Ghazi Khan'],
        'Tahim is recorded on the lower Indus and Chenab and in Bahawalpur, with a history of landholding around Chiniot.',
        'Section 429 says the Tahim formerly held much property in the Chiniot tahsil of Jhang and records them chiefly in Bahawalpur, Multan, Muzaffargarh and Derah Ghazi Khan. It notes that some followed other occupations, or that occupational groups had a Tahim clan, and that the Awan were said to have a Tahim clan.',
        'The source records a claim of Arab descent from an Ansari Qureshi called Tamim and a Multan story of an ancestor, Sambhal Shah, ruling there. These are attributed claims.')
    add('bhutta', 'Bhutta', 'bhutta', 'Listed among Jat tribes of the western plains; many Jhang returns Rajput (1881)',
        ['Shahpur', 'Jhang', 'Multan', 'Muzaffargarh', 'Derah Ghazi Khan', 'Uch (Bahawalpur, reported)'],
        'Bhutta is recorded on the lower Indus, Chenab and Jhelum. In Jhang most returned themselves as Rajput.',
        'Section 429 places Bhutta chiefly in Shahpur, Jhang, Multan, Muzaffargarh and Derah Ghazi Khan, says many took the title Pirzadah after the rise of a Multan family, and notes that some also worked as potters or weavers. It suggests some eastern Bhutta returns belong to a different Malwa clan.',
        'The source reports a claim of Solar Rajput descent, a story of holding Uch before the Saiyads came, and an origin from Bhutan that the author doubts. These are reported traditions.')
    add('langah', 'Langah', 'langah', 'Listed among Jat tribes of the western plains (1881)',
        ['Multan', 'Muzaffargarh', 'Lower Indus and Chenab'],
        'Langah is linked in the source with the dynasty that ruled Multan in the fifteenth and early sixteenth centuries.',
        'Section 429 quotes O\'Brien on the Langah kings of Multan from 1445 until the city fell to Shah Hasan Arghun in 1526, and places the Langah of 1881 almost entirely on the lower Indus and Chenab. It notes that 2,550 people returned as Langah were wrongly classed under Pathans.',
        'The source gives conflicting origins: an Afghan origin attributed to Farishtah, which the author doubts; a Punwar Rajput claim made by a Multan Pirzadah; and Tod\'s description of a clan of the Chaluk or Solanki Rajputs (the OCR reads Solani). None is settled here.')
    add('chhina', 'Chhina', 'chhina', 'Listed among Jat tribes of the western plains (1881)',
        ['Jamki (Sialkot)', 'Derah Ismail Khan, cis-Indus (outside scope)', 'Chenab valley'],
        'Chhina is treated as distinct from the Chima Jats of Sialkot and Gujranwala, although the two names were confused in the census tables.',
        'Section 429 says the town of Jamki in Sialkot was founded by a Chhina Jat from Sindh who kept the title Jam, and that the Chhina of Derah Ismail Khan lived mainly in its cis-Indus part. The author thinks some Gurdaspur and Firozpur returns belong with Chima.',
        caution='Chhina and Chima were confused in the 1881 tables, so some figures and localities may belong to either. Check the specific family and place before connecting the two names. ' + default_limits)
    add('sumra', 'Sumra', 'sumra', 'Discussed among Jat tribes, with a Rajput origin account (1881)',
        ['Lower Indus', 'Thal between the Jhang border and the Indus', 'Satluj and Chenab valleys'],
        'Sumra is discussed among Jat tribes of the western plains, with quoted accounts of a Sumra dynasty in Sindh and Multan.',
        'Section 430 records Sumra up the Satluj and Chenab and says the Derah Ismail Khan figures were probably understated, since they held much of the Thal between the Jhang border and the Indus. About 2,000 returned themselves as Rajput.',
        'The section quotes O\'Brien on a Sumra dynasty that expelled early Arab rulers of Sindh, and Tod\'s identification of the Sumra as a Punwar clan connected with Umarkot. These are quoted historical claims, not checked here.')
    add('hinjra', 'Hinjra', 'hinjra', 'Listed among western sub-montane Jat tribes (1881)',
        ['Gujranwala', 'Hissar (wider historical Punjab)'],
        'Hinjra is recorded as a pastoral tribe whose home was Gujranwala, where it owned 37 villages.',
        'Section 432 says the Hinjra owned 37 villages in Gujranwala and had spread east and west under the hills. It quotes the Hissar Settlement Report on Hinjraon groups there and says the link between the two had not been examined.',
        'The tribe claims Saroha Rajput descent from Hinjrano, said to have come from near Hissar and founded a city called Uskhab. The author also speculates about an aboriginal origin. Neither is a verified genealogy.')
    add('deo', 'Deo', 'deo', 'Listed among western sub-montane Jat tribes (1881)', ['Sialkot'],
        'Deo is recorded as practically confined to Sialkot.',
        'Section 433 places the Deo almost entirely in Sialkot, describes marriage customs shared with the Sahi, and mentions another Jat tribe with which they had an ancestral connection but did not intermarry.',
        'Two origin stories are reported: an ancestor called Mahaj whose sons Aulakh and Deo founded two Jat tribes, and descent from Raja Jagdeo, a Surajbansi Rajput. Both are traditions.')
    add('ghumman', 'Ghumman', 'ghumman', 'Listed among western sub-montane Jat tribes (1881)', ['Sialkot', 'Jammu (reported service)'],
        'Ghumman is recorded chiefly in Sialkot.',
        'Section 433 describes Ghumman wedding customs similar to those of the Sahi and places the tribe chiefly in Sialkot, spreading eastwards. A census table interrupts the entry in the upload.',
        'The tribe claims descent from Raja Malkir, a Lunar Rajput linked to the Janjua, through a descendant who married outside his caste and whose son Ghumman served in Jammu. This is a reported genealogy.')
    add('kahlon', 'Kahlon', 'kahlon', 'Listed among western sub-montane Jat tribes (1881)', ['Southern Sialkot', 'Gurdaspur (wider historical Punjab)'],
        'Kahlon is recorded in the southern parts of Sialkot and Gurdaspur.',
        'Section 433 places the Kahlon almost entirely in southern Gurdaspur and Sialkot, notes marriage customs similar to the Sahi, and says they married with Jats rather than Rajputs.',
        'The tribe claims descent from Raja Vikramajit through Raja Jagdeo of Daranagar, with a move to Batala and then Sialkot. This is a reported tradition.',
        aliases=[modern_alias('Kahloon')])
    add('goraya', 'Goraya', 'goraya', 'Listed among western sub-montane Jat tribes (1881)', ['Gujranwala', 'Sialkot', 'Gurdaspur (wider historical Punjab)'],
        'Goraya is recorded in Gujranwala, Sialkot and Gurdaspur, owning 31 villages in Gujranwala.',
        'Section 433 says the Goraya owned 31 villages in Gujranwala, where the author counted them among the most prosperous tribes, and notes marriage customs similar to the Sahi. It also says they were sometimes described as a Dhillon clan.',
        'Three origin accounts are given: Saroha Lunar Rajput descent with a move from Sirsa, descent from a Sombansi Rajput called Guraya, and a founder from the Jammu hills. They are not reconciled.')
    add('sindhu', 'Sindhu', 'sindhu', 'Listed among Jat tribes of the Sikh tract (1881)',
        ['Lahore', 'Gujranwala', 'Sialkot', 'Amritsar (wider historical Punjab)', 'Upper Satluj'],
        'Sindhu is described as the second-largest Jat tribe in the 1881 figures, centred on Amritsar and Lahore.',
        'Section 435 places Sindhu headquarters in Amritsar and Lahore and records them along the upper Satluj and under the hills from Ambala to Sialkot and Gujranwala. It notes their political importance under the Sikhs, and says the Sindhu of Karnal worship an ancestor, Kala Mahar, whose chief shrine is said to be at Thana Satra in Sialkot, their alleged place of origin.',
        'The tribe claims Raghobansi Solar Rajput descent through Ram Chandar of Ajudhia and gives differing accounts of a return from Ghazni. Griffin suggests an origin in north-western Rajputana. These remain traditions and opinions.',
        aliases=[modern_alias('Sandhu')])
    add('pannun', 'Pannun', 'pannun', 'Listed among Jat tribes of the Sikh tract (1881)',
        ['Sialkot (five villages)', 'Amritsar (wider historical Punjab)', 'Gurdaspur (wider historical Punjab)'],
        'Pannun is recorded chiefly in Amritsar and Gurdaspur, with five villages in Sialkot.',
        'Section 436 gives Amritsar and Gurdaspur as the main areas in the figures and says the Pannun also owned five villages in Sialkot.',
        'The tribe claims Solar Rajput ancestry and an origin in Ghazni or, by another story, Hindustan. These are reported traditions.',
        aliases=[modern_alias('Pannu')])
    add('aulak', 'Aulak', 'aulak', 'Listed among Jat tribes of the Sikh tract (1881)',
        ['West of the Ravi', 'Manjha', 'Amritsar (wider historical Punjab)', 'Northern Malwa (wider historical Punjab)'],
        'Aulak is recorded with headquarters in Amritsar and groups west of the Ravi.',
        'Section 436 places the Aulak headquarters in Amritsar, with groups in the northern Malwa, the Manjha and west of the Ravi. It says they were related to the Sekhu and Deo tribes and did not intermarry with them.',
        'Two ancestries are reported: Solar descent from an ancestor Aulak in the Manjha, and descent from Raja Lui Lak, a Lunar Rajput. Both are traditions.',
        aliases=[modern_alias('Aulakh')])
    add('gil', 'Gil', 'gil', 'Listed among Jat tribes of the Sikh tract (1881)',
        ['Lahore', 'Sialkot', 'Firozpur (wider historical Punjab)', 'Beas and upper Satluj'],
        'Gil is described as one of the largest Jat tribes in the 1881 figures, centred on Lahore and Firozpur.',
        'Section 436 places Gil headquarters in Lahore and Firozpur, with groups along the Beas and upper Satluj and under the hills as far west as Sialkot. It says the tribe rose to some importance under the Sikhs and points to Griffin for the history of its principal family.',
        'The tribe traces itself to an ancestor Gil of Raghobansi Rajput descent and a Bhular Jat mother, and names him as father of Shergil, founder of another tribe. This is a reported genealogy.',
        aliases=[modern_alias('Gill')])

    # Part III: Rajput tribes of the western plains, western hills and Jammu border.
    add('punwar', 'Punwar', 'punwar', 'Rajput tribe of the western plains; many western returns Jat (1881)',
        ['Satluj valley', 'Lower Indus', 'Multan division', 'Derajat'],
        'Punwar (Pramara) is described as a once-powerful Agnikula Rajput tribe, found in 1881 along the Satluj and lower Indus.',
        'Section 448 records Punwar up the Satluj and along the lower Indus, noting that in the Derajat all, and in the Multan division many, were returned as Jats. It also mentions colonies in Rohtak and Hissar, now in India.',
        'The section presents Punwar as an Agnikula Rajput race whose ancient territory ran along the Satluj from the Indus towards the Jamna. This is a historical tradition and the author\'s interpretation.',
        aliases=[source_alias('Pramara', 'Section 448 gives Pramara as the classical form of Punwar.'), modern_alias('Panwar')])
    add('wattu', 'Wattu', 'wattu', 'Bhatti clan among Rajput tribes of the Satluj (1881)',
        ['Both banks of the Satluj', 'Montgomery (historical district)', 'Bahawalpur', 'Ravi valley'],
        'Wattu is described as a Bhatti clan holding both banks of the Satluj around Fazilka and the adjoining parts of Montgomery and Bahawalpur.',
        'Section 449 says the Wattu held both banks of the Satluj in Sirsa and the neighbouring parts of Montgomery and Bahawalpur, with a smaller group on the Ravi. It records a shift from pastoral life to farming along the Satluj and notes that some may have returned themselves simply as Bhatti.',
        'The Sirsa tradition traces the Wattu to the Bhatti Raja Salvahan through Rajpal, and the Wattu date their conversion to Islam to Baba Farid in the time of Khiwa of Haveli. These are reported traditions.',
        caution=period_remarks + default_limits)
    add('joya', 'Joya', 'joya', 'Rajput tribe of the Satluj; about a third returned as Jat (1881)',
        ['Satluj valley below the Wattu', 'Bahawalpur', 'Multan (Joya bar)', 'Lahore', 'Muzaffargarh', 'Shahpur'],
        'Joya is recorded along the Satluj down towards its confluence with the Indus, and the Multan bar was known as the Joya bar.',
        'Section 449 places the Joya on the Satluj from the Wattu border nearly to the Indus, on the middle Satluj of Lahore and Firozpur, and on the lower Indus of the Derajat and Muzaffargarh, with about a third returned as Jat. It also mentions the small Mahar tribe opposite Fazilka.',
        'The section repeats the Joya\'s place among the 36 royal Rajput races, Cunningham\'s identification with ancient warriors in Panini (which the author doubts), and differing Hissar and Montgomery origin stories, including a Biblical one. None is accepted here as proven.',
        caution=period_remarks + default_limits,
        aliases=[modern_alias('Joiya'), related_alias('Mahar', 'Section 449 treats the Mahar as a small related tribe said to descend from a brother of the Joya. It is a separate group, listed only so this passage can be found.')])
    add('khichi', 'Khichi', 'khichi', 'Chauhan clan among Rajput tribes of the Satluj (1881)',
        ['Lower and middle Satluj', 'Ravi from Multan to Lahore', 'Montgomery (historical district)'],
        'Khichi is described as a Chauhan clan along the Satluj and the Ravi between Multan and Lahore.',
        'Section 449 records Khichi along the lower and middle Satluj, on the Ravi from Multan to Lahore, and in Montgomery mainly on the Ravi, with a few on the Chenab and a group in the Delhi district.',
        'A story brings them from Ajmer to Delhi and then to the Satluj under Mughal rule; the author thinks it reflects the movement of Chauhan power rather than the tribe\'s own migration.')
    add('dhudhi', 'Dhudhi', 'dhudhi', 'Punwar clan among Rajput tribes of the Satluj (1881)',
        ['Mailsi (Multan)', 'Satluj valley', 'Chenab valley'],
        'Dhudhi is described as a small Punwar clan whose original seat is said to have been the Mailsi tahsil of Multan.',
        'Section 449 places the Dhudhi with the Rathor along the Satluj and Chenab, records them in Mailsi as early as the fourteenth century, and names a saint, Haji Sher Muhammad, whose shrine in Multan was renowned. The author suspects some eastern Rajputs with a similar name were mixed into the figures.')
    add('hiraj', 'Hiraj', 'hiraj', 'Sial clan among Rajput tribes of the Chenab (1881)',
        ['Ravi just above its junction with the Chenab', 'Multan'],
        'Hiraj is described as a Sial clan holding land on the Ravi just above its junction with the Chenab.',
        'Section 450 says some Hiraj may have returned themselves simply as Sial, and that 3,380 in Multan returned themselves as Sial Hiraj and were counted under both headings.')
    add('mekan', 'Mekan', 'mekan', 'Rajput tribe of the Jhelum, said to be of Punwar origin (1881)',
        ['Shahpur bar, west of the Gondal', 'Jhelum', 'Gujrat'],
        'Mekan is recorded in the Shahpur bar west of the Gondal territory, with smaller numbers in Jhelum and Gujrat.',
        'Section 451 places the Mekan in the Shahpur bar and describes them as a small pastoral tribe.',
        'They are said to be of Punwar origin and to share an ancestor with the Dhudhi. This is a reported tradition.')
    add('bhakral', 'Bhakral', 'bhakral', 'Hill tribe of south-eastern Rawalpindi in the Rajput discussion (1881)',
        ['South-eastern Rawalpindi district', 'Jhelum', 'Gujrat'],
        'Bhakral is recorded with considerable land in south-eastern Rawalpindi and some numbers in Jhelum and Gujrat.',
        'Section 453 discusses the Bhakral with the Budhal in the hill-tribe group, says 5,099 Rawalpindi Bhakral also returned themselves as Punwar, and doubts that a separate Bahawalpur group of the same name is related.',
        'The Budhal, like the Dhanial, claim descent from Ali. The author thinks "both these tribes" probably came from Jammu territory across the Jhelum; the sentence does not make clear which two he means. Neither the claim nor his inference is a verified genealogy.',
        aliases=[related_alias('Budhal', 'A neighbouring tribe discussed in the same entry. It is a separate group, listed only so this passage can be found.')])
    add('alpial', 'Alpial', 'alpial', 'Rajput tribe of the Fateh Jhang tahsil (1881)',
        ['Southern Fateh Jhang tahsil', 'Rawalpindi district (historical)'],
        'Alpial is recorded in the southern corner of the Fateh Jhang tahsil of Rawalpindi.',
        'Section 453 says 8,085 Rawalpindi Rajputs listed under another heading were Alpial of Fateh Jhang, and that the tribe was accepted as Rajput, with wedding customs still showing traces of Hindu origin.',
        'The author infers that they came up from the south through the Khushab and Talagang country. This is his inference, not a recorded genealogy.',
        caution=period_remarks + default_limits)
    add('kanial', 'Kanial', 'kanial', 'Hill tribe of south-eastern Rawalpindi in the Rajput discussion (1881)',
        ['South-eastern Rawalpindi district', 'Sub-montane towards Gujrat'],
        'Kanial is recorded holding much of the south-eastern corner of Rawalpindi and stretching towards Gujrat.',
        'Section 453 quotes Steedman placing the Kanial among groups who called themselves Rajput in south-eastern Rawalpindi, alongside the Budhal and Bhakral, and says they also extended along the sub-montane as far as Gujrat.')
    add('kahut', 'Kahut', 'kahut-mair', 'Salt Range tribe; most Jhelum returns gave Mughal as clan (1881)',
        ['Kahutani, southern Dhani country', 'Chakwal tahsil (Jhelum)'],
        'Kahut is recorded in the southern Dhani country of Chakwal, alongside the Mair in the centre and the Kasar in the north.',
        'Section 454 says the Kahut were classed as a separate caste but discussed with the Salt Range Rajputs, held Kahutani in the south of the Dhani country, and that all but 293 of the 8,766 Jhelum Kahut gave Mughal as their clan. The author links them to the town and hills of Kahuta.',
        'Kahut, Mair and Kasar all say they came from the Jammu hills and were settled by Babar. Their bards claim Mughal origin and they are sometimes called Awan; the author thinks a Rajput connection more likely. None of these is settled here.',
        caution=period_remarks + default_limits)
    add('mair', 'Mair', 'kahut-mair', 'Salt Range tribe of the central Dhani country (1881)',
        ['Central Dhani country', 'Chakwal tahsil (Jhelum)'],
        'Mair is recorded in the centre of the Dhani country of Chakwal, between the Kahut and the Kasar.',
        'Section 454 has no separate figures for the Mair. It says some Mair called themselves Minhas, probably the same word as Manhas, and may have been returned as Manhas Rajputs.',
        'Like the Kahut and Kasar, the Mair say they came from the Jammu hills and were settled by Babar. This is a reported tradition.',
        caution=period_remarks + default_limits)
    add('jodra', 'Jodra', 'gheba', 'Discussed with Gheba; no separate census figures (1881)',
        ['Eastern Pindi Gheb', 'Pindi Gheb town', 'Rawalpindi district (historical)'],
        'Jodra is discussed with the Gheba in the Salt Range material, holding the eastern half of Pindi Gheb.',
        'Section 454 says there were no separate figures for Jodra or Gheba, places the Jodra in the eastern half of Pindi Gheb, and notes that the town of Pindi Gheb was built and held by the Jodra.',
        'The Jodra are said to have come from Jammu or Hindustan and to have held their tract before the Gheba arrived. The author repeats, from an authority he cannot remember, that the Gheba were a branch of the Jodra. These remain unverified.')
    add('salahria', 'Salahria', 'salahria', 'Jammu-border Rajput tribe, partly returned as Thakar (1881)',
        ['Eastern Sialkot', 'Lahore', 'Gurdaspur (wider historical Punjab)'],
        'Salahria is recorded with headquarters in eastern Sialkot. Most of the Thakar Rajputs returned from Sialkot were Salahria.',
        'Section 455 says 5,279 Sialkot men returned themselves as Rajput Salaria Thakar and were counted under both headings, and that some Sialkot Salahria also appeared as Manhas or Bhatti. It describes them as mostly Muslim, with wedding customs that included marking the couple with goat\'s blood.',
        'The Salahria trace descent from Raja Saigal and Chandra Gupta and say their ancestor came from the Deccan as a commander under an early Sultan (the OCR garbles the name) and settled at Sialkot, converting to Islam under Bahlol Lodi. These are reported traditions.',
        aliases=[source_alias('Salaria', 'Spelling in the census return quoted in section 455.'),
                 related_alias('Thakar', 'Section 455 says most Sialkot Thakar returns were Salahria, and explains Thakar as a title also used elsewhere. Do not treat every Thakar as Salahria.')])
    add('raghbansi', 'Raghbansi', 'raghbansi', 'Jammu-border Rajput tribe (1881)',
        ['Sialkot sub-montane', 'Gurdaspur (wider historical Punjab)', 'Hill States (wider historical Punjab)'],
        'Raghbansi is recorded in the Hill States and the sub-montane of Gurdaspur and Sialkot.',
        'Section 455 says that in Punjab the Raghbansi were chiefly found in the Hill States and the Gurdaspur and Sialkot sub-montane, and that many in Gurdaspur and Sialkot also returned themselves as Manhas.',
        'The author says the name implies little more than a traditional origin. Descent claims through the name remain unverified.')

    # Part IV: minor dominant tribes and "foreign races".
    add('daudpotra', 'Daudpotra', 'daudpotra', 'Ruling family of Bahawalpur, listed among minor dominant tribes (1881)',
        ['Bahawalpur', 'Multan (former Bahawalpur territory)', 'Satluj valley'],
        'Daudpotra is described as the ruling family of Bahawalpur, almost confined to Bahawalpur and neighbouring parts of Multan.',
        'Section 473 says 1,421 people returned themselves as Shekh Daudpotra, mostly in Multan, and that the tribe was practically confined to Bahawalpur and parts of Multan once in the state. It quotes Cunningham on their migration up the Satluj after Nadir Shah established his authority in Sindh.',
        'The section reports a Qureshi Arab claim, a descent claim from the Caliph Abbas, a link to the Kalhora rulers of Sindh and a Wattu Rajput story. The author dismisses these and offers his own view of the founder; none of these accounts is treated here as established.',
        caution='The Abbas descent claim in this passage concerns the Daudpotra of Bahawalpur. It is unrelated to the AJK Abbasi research lead and does not verify it. The author\'s dismissal of the tribe\'s own accounts is also an opinion of its period. ' + default_limits)
    add('qureshi', 'Qureshi', 'qureshi', 'Arab descent title, counted under Shekh (1881)',
        ['Multan', 'Jhang', 'Muzaffargarh'],
        'Qureshi is the name of the Prophet\'s Arab tribe. The 1881 census counted most Qureshi returns under the Shekh heading.',
        'Sections 501–502 call Qureshi the favourite tribe from which to claim descent, and the author doubts that many who returned it had a real title to it. They name the Hashmi Qureshis descended from Baha-ul-haqq of Multan, chiefly in Multan, Jhang and Muzaffargarh, and note Faruqi and Sadiqi sub-claims.',
        'Sub-claims to descent from the first two Caliphs and the Hashmi descent of the Multan family are recorded as claims. The author doubts many Qureshi returns; neither the claims nor his doubts verify a particular family.',
        caution='A census return of a descent title does not confirm it, and neither does the author\'s doubt disprove it. Do not treat this record as authenticating any family\'s Qureshi ancestry. ' + default_limits,
        aliases=[modern_alias('Quraishi')], type='title')
    add('sheikh', 'Sheikh', 'shekh', 'Title adopted by many groups; a large 1881 heading',
        ['Bahawalpur', 'Multan', 'Derajat (some returned as Jat)'],
        'Sheikh, written Shekh in the source, is described as an Arabic title meaning elder that was adopted by many Muslim groups. The 1881 heading therefore mixed people of many origins.',
        'Sections 501–502 explain Shekh as a title, say many converts and agricultural tribes returned themselves under it, and admit the author wrongly included some tribes such as the Hans and Khagga. They list Shekh sub-divisions including Naumuslim, Ansari and Muhajarin.',
        'Claims within the heading range from Arab descent to recent adoption of the title. The source records them without verifying any particular family.',
        caution='The source\'s remarks about the social level of people who took the title are prejudices of its period. A Shekh return in 1881 says little about a particular family\'s origin. ' + default_limits,
        aliases=[source_alias('Shekh', 'Spelling used in the 1881 source.'),
                 related_alias('Ansari', 'Section 502 lists Ansari, a title claiming descent from the Medina helpers of the Prophet, as a Shekh sub-division. It is not a spelling of Sheikh.')], type='title')
    add('hans', 'Hans', 'hans-khagga', 'Tribe claiming Qureshi origin, counted under Shekh (1881)',
        ['Pakka Sidhar (Montgomery)', 'Multan', 'Jhang', 'Montgomery (historical district)'],
        'Hans is recorded in Multan, Jhang and Montgomery. The author regretted counting them under Shekh.',
        'Section 503 says the Hans settled at Pakka Sidhar in Montgomery, won independent rule over part of the district under their chief Shekh Qutb in Alamgir\'s time, and lost it under the Sikhs when the streams watering their land dried up.',
        'The Hans claim Qureshi origin and a migration from Arabia through Afghanistan. The author considered the claim apparently valid; that judgment still does not verify a family genealogy.')
    add('khagga', 'Khagga', 'hans-khagga', 'Tribe claiming Qureshi origin, counted under Shekh (1881)',
        ['Montgomery (historical district)', 'Multan', 'Jhang', 'Muzaffargarh'],
        'Khagga is recorded in Multan, Montgomery, Jhang and Muzaffargarh. The author said they should have been kept separate from Shekh.',
        'Section 503 quotes Purser that the Khagga came to Montgomery after Ranjit Singh conquered Multan, and gives 1881 counts by district.',
        'The Khagga claim Qureshi descent from Jalal-ud-din, a disciple of Muhammad Iraq, and explain the name through a story about rescuing a boat in a storm. These are attributed traditions.')
    add('nekokara', 'Nekokara', 'nekokara', 'Tribe claiming Hashmi Qureshi origin (1881)', ['Jhang', 'Gujranwala'],
        'Nekokara, also called Kokara, is recorded chiefly in Jhang, with land in Gujranwala.',
        'Section 504 says many Nekokara in Gujranwala were faqirs and that the tribe generally had a semi-religious character.',
        'They claim to be Hashmi Qureshis who came from Bahawalpur about 450 years before the census. This is a reported claim.',
        aliases=[source_alias('Kokara', 'Section 504 gives this as another form of the name.')])
    add('jhandir', 'Jhandir', 'nekokara', 'Tribe said to be of Qureshi origin (1881)', ['Southern Jhang'],
        'Jhandir is recorded with land in the far south of Jhang district.',
        'Section 504 describes the Jhandir as having a reputation for sanctity and literacy without openly professing to be religious directors.',
        'They are said to be of Qureshi origin and to take their name from having been standard-bearers of a great saint. These are reported traditions.')
    add('kassar', 'Kassar', 'kasar', 'Salt Range tribe, returned as Mughal in 1881',
        ['Northern Dhani country', 'Bubial and Chaupeda', 'Chakwal tahsil (Jhelum)'],
        'Kassar, written Kasar in the source, is recorded in the north of the Dhani country around Bubial and Chaupeda.',
        'Section 508 says 8,527 Jhelum Mughals gave Kasar as their clan, so the Kasar were counted as Mughal. It says that until the census they had been one of the few Salt Range tribes claiming neither Rajput, Awan nor Mughal descent.',
        'They say their old home was in Jammu and that they joined Babar\'s army and received their land. The author treats the Mughal claim as new and suggested by that association.',
        caution=period_remarks + default_limits,
        aliases=[source_alias('Kasar', 'Spelling used in the 1881 source.')])

    # Part V: religious, professional, mercantile and miscellaneous.
    add('bodla', 'Bodla', 'bodla', 'Saintly section of the Wattu claiming Qureshi origin (1881)',
        ['Lower and middle Satluj', 'Montgomery (historical district)', 'Bahawalpur', 'Multan (earlier home)'],
        'Bodla is described as a small section of the Wattu Rajputs of the Satluj with a reputation for sanctity.',
        'Section 519 says 2,435 Bodla returned themselves as Qureshi and were counted under Shekh, that they took Wattu wives but married their daughters only to Bodla, and that they came from Multan through Bahawalpur to Montgomery and Sirsa. It records belief in their power to cure by exorcism.',
        'The Bodla claim Qureshi descent from Abu Bakr Siddiq; the author says their Wattu origin is undoubted. The two views are recorded side by side, not resolved here.',
        caution=period_remarks + default_limits)
    add('nai', 'Nai', 'nai', 'Barbers and hereditary messengers; occupational caste (1881)',
        ['Across the Province', 'Less common in the Derajat'],
        'Nai is the 1881 heading for barbers, who also carried formal messages between villages, helped arrange marriages and performed minor surgery.',
        'Section 525 describes the Nai as barber, carrier of formal messages between villages, go-between in betrothals and village surgeon, and says Muslim barbers in towns were often called Hajjam. It records about 55 percent as Muslim and names Bhatti and Khokhar among the largest clans in the west.',
        caution=occupational, aliases=[source_alias('Hajjam', 'Section 525 says Muslim barbers in towns were often called Hajjam.')], type='community')
    add('mirasi', 'Mirasi', 'mirasi', 'Genealogists and musicians; occupational caste (1881)',
        ['Amritsar, Lahore, Rawalpindi and Multan divisions', 'Bahawalpur'],
        'Mirasi is described as hereditary genealogist, musician and minstrel, attending weddings to recite family histories.',
        'Section 527 says Mirasi were most numerous in the Amritsar, Lahore, Rawalpindi and Multan divisions and Bahawalpur, were almost always Muslim, and served as genealogists for many agricultural groups as well as musicians. It derives the name from the Arabic for inheritance and says the census merged several musician groups under it.',
        caution=occupational, type='community')
    add('khoja', 'Khoja', 'khojah-paracha', 'Muslim trading groups; not one caste in the author\'s view (1881)',
        ['Lahore', 'Gujrat', 'Sialkot', 'Jhang', 'Shahpur', 'Salt Range'],
        'Khoja, written Khojah in the source, is the 1881 table heading for Muslim traders, whom the author did not regard as a single caste.',
        'Section 545 says the Khojah of Shahpur were mostly converted Khatris, those of Jhang were said to be converted Aroras, and some in Lahore claimed Bhatia origin. It describes a cloth trade run by Khojahs of Gujrat and Sialkot and says Khojah and Paracha were often mixed up in the tables.',
        caution='The word had several unrelated uses in 1881 Punjab, and the Khojah and Paracha figures were mixed. A shared name does not identify a family\'s origin. This record is separate from the Khawaja research lead. ' + default_limits,
        aliases=[source_alias('Khojah', 'Spelling used in the 1881 source.')], type='community')
    add('paracha', 'Paracha', 'khojah-paracha', 'Muslim traders; the Makhad section a true caste in the author\'s view (1881)',
        ['Makhad (Rawalpindi district, historical)', 'Attock', 'Salt Range'],
        'Paracha is described as a Muslim trading name. The author regarded one section, based at Makhad on the Indus with colonies at Attock and Peshawar, as a true caste.',
        'Section 545 says the Paracha of the Salt Range traded with Central Asia in cloth, silk, indigo and tea, had seven clans, and married their daughters only to Paracha. It warns that elsewhere Paracha was used loosely for any Muslim pedlar.',
        'They say they came from Dangot in Bannu and moved to Makhad in Shah Jahan\'s time; another account calls them Khatris of Lahore deported by Zaman Shah. They explain the name from parcha, cloth. These are reported traditions.',
        type='community')
    add('kashmiri', 'Kashmiri', 'kashmiri', 'Kashmiri settlers and Chibhali hill people in Punjab (1881)',
        ['Lahore', 'Gujranwala', 'Gujrat', 'Salt Range', 'Chibhal (Kashmir hills, historical)', 'Amritsar and Ludhiana (wider historical Punjab)'],
        'Kashmiri is described as a geographical label for Muslim migrants from Kashmir. The 1881 figures probably also include Chibhalis, the people of the Kashmir hills bordering Gujrat, Rawalpindi and Hazara.',
        'Section 557 divides Kashmiris in Punjab into three groups: the large, permanently settled weaving colonies of Amritsar and Ludhiana; recent migrants driven out by famine or drawn by work in the Salt Range and on the frontier; and Chibhalis who had settled across the border, probably only in Gujrat and the trans-Salt Range tract. It also counts 7,515 people returned as Kashmiri Jats, mostly in Lahore and Gujranwala, whom the author takes to be Kashmiris who took up farming.',
        caution='The 1881 term was geographical and probably covered several distinct communities. Chibhal is the historical hill country on the Kashmir border with Gujrat, Rawalpindi and Hazara, which broadly overlaps present-day AJK, but the passage names no AJK district. It does not verify any family\'s origin. The source\'s remarks about Kashmiri character and its racial theories are prejudices of its period. ' + default_limits,
        aliases=[related_alias('Chibhali', 'Section 557 says Kashmiri returns probably include Chibhalis, the hill people of the Kashmir border. The two are distinct groups in the source.')],
        type='community', regions=('punjab', 'kashmir'))

    # Part VI: artisan and service castes.
    add('mochi', 'Mochi', 'mochi', 'Leather-workers; occupational caste (1881)', ['Western Punjab', 'Across the Province'],
        'Mochi is described as the leather-worker, as distinct from the tanner. In western Punjab the name was used for Muslim leather-workers generally.',
        'Section 607 says Mochi was properly an occupational name for workers in tanned leather, used in the east for skilled town workmen and in the west for Muslim leather-workers generally. It notes that in the west they no longer did general field labour, and that some Mochis returned themselves as Jat.',
        caution=occupational, type='community')
    add('julaha', 'Julaha', 'julaha', 'Weavers; occupational caste (1881)', ['Western districts', 'Most of the Province (scarce in the Derajat)'],
        'Julaha, called Paoli in western villages, is described as the weaver, a numerous artisan group especially in the western districts.',
        'Section 612 says about 92 percent of Julahas were Muslim, that they were paid by the piece rather than by customary dues, and that people of several origins entered the occupation. It records them as scarce in the Derajat, where weaving was often done by others.',
        caution=occupational, aliases=[source_alias('Paoli', 'Section 612 gives Paoli as the name used in western villages.')], type='community')
    add('machhi', 'Machhi', 'machhi', 'Village cooks, oven-keepers and fishermen; occupational caste (1881)',
        ['Lahore', 'Gujranwala', 'Montgomery (historical district)', 'Derajat', 'Central and western Punjab'],
        'Machhi is described as the western, mainly Muslim name for the Jhinwar occupational group, including village cooks, oven-keepers and fishermen.',
        'Section 619 says the Machhi kept the village oven, served as cook and midwife, did much farm labour in the centre and west, and was called Men or Manjhi when fishing. It records the Men mostly on the middle Satluj, in Lahore, Gujranwala and Montgomery.',
        caution=occupational,
        aliases=[source_alias('Men', 'Section 619 says fishermen along the great rivers were often called Men.'), source_alias('Mahigir', 'Section 619 classes Mahigir fishermen under Machhi.')], type='community')
    add('mallah', 'Mallah', 'mallah', 'Boatmen; occupational caste (1881)', ['Indus', 'Navigable river districts'],
        'Mallah is described as the boatman of the Punjab, most numerous where rivers were navigable.',
        'Section 621 says the Mallah was usually Muslim, often combined boat work with fishing or growing water-nuts, and was not a village servant. It counts Mohana, Taru and Dren under the same heading.',
        caution=occupational, aliases=[source_alias('Mohana', 'Section 621 counts Mohana, the Sindh fisherman and boatman, under Mallah.')], type='community')
    add('lohar', 'Lohar', 'lohar', 'Blacksmiths; occupational caste (1881)', ['Hills and sub-montane districts', 'Across the Province'],
        'Lohar is described as the village blacksmith, making and mending iron farm tools in return for a share of the harvest.',
        'Section 624 says the Lohar was most numerous in the hills and the districts below them and unusually scarce in the Multan and Derajat divisions and Bahawalpur, where the author guessed others did the work.',
        caution=occupational, type='community')
    add('tarkhan', 'Tarkhan', 'tarkhan', 'Carpenters; occupational caste (1881)', ['Across the Province', 'Less common on the lower frontier'],
        'Tarkhan is described as the carpenter, making and mending farm implements and household furniture for customary dues.',
        'Section 627 says the Tarkhan was found throughout the Province, was called Barhai, Barhi or Khati further east, and that turners (Kharadi) were counted with them. The author thought Tarkhan and Lohar were probably the same caste in origin.',
        caution=occupational, aliases=[source_alias('Khati', 'Section 627 gives Khati as the name in much of the Eastern Plains.')], type='community')
    add('kumhar', 'Kumhar', 'kumhar', 'Potters and brick-burners; occupational caste (1881)',
        ['Sub-montane and central districts', 'Lower Indus', 'Hissar (wider historical Punjab)'],
        'Kumhar, which the book says was more often called Gumiar in Punjab, is described as potter, brick-burner and village carrier.',
        'Section 632 says the Kumhar supplied household earthenware and the pots for Persian wheels, kept donkeys to carry grain within the village, and burned bricks, with Kuzagar used for makers of finer pottery. Some on the lower Indus returned themselves as Jat.',
        caution=occupational,
        aliases=[source_alias('Gumiar', 'Section 632 says the Kumhar was more often called by this name in Punjab.'), modern_alias('Ghumiar'), source_alias('Kuzagar', 'Section 632 uses Kuzagar for makers of finer pottery.')], type='community')
    add('sunar', 'Sunar', 'sunar', 'Gold and silver smiths; occupational caste (1881)', ['Across the Province', 'Multan division', 'Frontier districts'],
        'Sunar, or Zargar in towns, is described as goldsmith, silversmith and jeweller, often also lending money against pledged jewellery.',
        'Section 634 says the Sunar was found in most sizeable villages, was usually Hindu in the Eastern Plains and Salt Range but often Muslim in the Multan division and on the frontier, and that the author regarded it as a true caste.',
        caution=occupational, aliases=[source_alias('Zargar', 'Section 634 says the Sunar was often called Zargar in towns.')], type='community')
    add('dhobi', 'Dhobi', 'dhobi', 'Washermen and calico-printers; occupational caste (1881)',
        ['Towns across the Province', 'Lahore and Rawalpindi divisions', 'Derajat and Multan (counted as Charhoa)'],
        'Dhobi is described as the washerman, in the centre and west often also a calico-printer.',
        'Section 642 says Dhobi and Chhimba figures had to be taken together, that in the Derajat and Multan divisions Dhobis were counted under Charhoa, and that the Dhobi was most often Muslim and often also worked as a tailor.',
        caution=occupational,
        aliases=[source_alias('Chhimba', 'Section 642 says Chhimba and Dhobi were classed together in several divisions.'), source_alias('Charhoa', 'Section 642 says Dhobis were counted as Charhoa in the Derajat and Multan divisions.')], type='community')
    add('teli', 'Teli', 'teli-qassab', 'Oil-pressers; occupational caste (1881)', ['Across the Province, except the hills', 'Multan and Derajat (as Chaki)'],
        'Teli is described as the oil-presser. The author treated Teli as a caste, and Qassab and Penja as occupations mostly followed by Telis.',
        'Section 647 says the Teli was almost entirely Muslim, spread evenly outside the hills, most numerous in cities, and called Chaki or Chakani in Multan and the Derajat.',
        caution=occupational, aliases=[source_alias('Chaki', 'Section 647 gives Chaki or Chakani as the name in Multan and the Derajat.')], type='community')
    add('qassab', 'Qassab', 'teli-qassab', 'Butchers; occupational name (1881)', ['Cities across the Province', 'Derajat (some returned as Jat)'],
        'Qassab is described as the butcher who slaughters in the Muslim manner and sells meat. The author treated it as an occupation mostly followed by Telis.',
        'Section 647 groups Penja (cotton-scutchers), Teli and Qassab together, says Qassab was an occupational name rather than a true caste in the author\'s view, and notes that some Qassabs in the Derajat returned themselves as Jat.',
        caution=occupational, type='community')

    # Book notes on two existing records.
    by_id['gujjar']['claims'].insert(-1, claim('gujar-tribes', 'Clan names in the source',
        'Section 482 says Gujar tribes and clans were numerous and widely spread, with new local sub-divisions in many places, and names Khatana and Chechi as by far the largest in the figures.'))
    # A pointer, not evidence: the note goes into the caution too, so copied summaries keep it with the citation.
    khawaja = by_id['khawaja']
    khojah_note = 'Section 545 of the 1881 Punjab account traces the word Khojah to the honorific Khwajah and records several unrelated uses, the census one being Muslim traders. It concerns Punjab usage and does not identify the AJK Khawaja entry.'
    khawaja['claims'].append(claim('khojah-paracha', 'A related word in the 1881 account', khojah_note, 'verify'))
    khawaja['caution'] += ' ' + khojah_note
    khawaja['sourceIds'] = list(dict.fromkeys(khawaja['sourceIds'] + ['ibbetson']))

    group_of = {id: group for group, ids in GROUPS.items() for id in ids}
    assert len(group_of) == sum(len(ids) for ids in GROUPS.values()), 'record listed in two groups'
    assert set(group_of) == {r['id'] for r in records}, set(group_of) ^ {r['id'] for r in records}
    for r in records:
        r['group'] = group_of[r['id']]
        r.setdefault('classificationSource', 'project-ajk' if r['type'] != 'clan' else 'project-clans')
        for c in r['claims']:
            if c.get('passageId'):
                assert c['passageId'] in LOCATORS
    # Written only after every check above, so a failed run never leaves passages.js and data.js out of step.
    (ROOT / 'dist/passages.js').write_text('window.BOOKPASSAGES = ' + json.dumps(reader, ensure_ascii=False, indent=2) + ';\n',
                                           encoding='utf-8', newline='\n')
    return {'uploadedSourceSha256': sha, 'passageCount': len(passages),
            'bookAddedRecords': sum(r['locationSource'] == 'ibbetson' for r in records), 'originalProjectRecords': 23}
