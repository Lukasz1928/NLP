import regex


def find_external_references(data, filename):
    references = []
    for k in data.keys():
        try:
            references.extend(find_external_in_single_file(data[k]))
        except TypeError:
            pass # file in incorrect format
    aggregated = aggregate_results(references)
    dec_keys = sorted(aggregated.keys(), key=lambda x : aggregated[x]['count'], reverse=True)
    with open('results/{}.txt'.format(filename), "w") as file:
        file.write('journal year, journal position, references\n')
        for i in dec_keys:
            file.write('{}, {}, {}\n'.format(aggregated[i]['year'], aggregated[i]['position'], aggregated[i]['count']))


def format_title(title):
    remove_leading = r'^-?\s*'
    remove_tail = r'\s*$'
    remove_redundant_whites_regex = r'\s+'
    if title is None:
        return None
    title = regex.sub(remove_leading, '', title, regex.MULTILINE | regex.DOTALL)
    title = regex.sub(remove_tail, '', title, regex.MULTILINE | regex.DOTALL)
    title = regex.sub(remove_redundant_whites_regex, ' ', title, regex.MULTILINE | regex.DOTALL)
    return title


def find_external_in_single_file(text):

    date_regex = r'\bz\s+\bdnia\b\s+(?P<day>\d{1,2})\s+(?P<month>\d{1,2}|\b.+\b)\s+(?P<year>\d{4})\s*r(oku|\.)\s*'
    title_regex = r'(?P<title>(\s*(\bo\b)|-)\s*(\w|\s)*?)(?=\s*\()'
    journal_regex = r'\(\s*[Dd]z\.\s*U.\s+(?P<journal_details>(.|\s)*?)\)'

    journal_year_groups_regex = r'((z\s+(?P<journal_year>\d{4})\s+r.\s+)?(?P<numbers>(([Nn]r\s+\d+,\s+poz\.\s+\d+\s*(,|i|oraz|$)\s*))+))'
    journal_numbers_regex = r'[Nn]r\s+(?P<number>\d+),\s+poz\.\s+(?P<position>\d+)'

    reference_regex = r'\b[Uu]staw.+\s+({})\s*({})\s*({})'.format(date_regex, title_regex, journal_regex)

    references = []
    for ref in regex.finditer(reference_regex, text, regex.MULTILINE):
        ref_data = {}
        ref_data['day'] = ref.group('day')
        ref_data['month'] = ref.group('month')
        ref_data['year'] = ref.group('year')
        ref_data['title'] = format_title(ref.group('title'))
        ref_data['journals'] = []
        for year_group in regex.finditer(journal_year_groups_regex, ref.group('journal_details'), regex.MULTILINE):
            year = year_group.group('journal_year')
            for journal_data in regex.finditer(journal_numbers_regex, year_group.group('numbers'), regex.MULTILINE):
                ref_data['journals'].append({'number': journal_data.group('number'),
                                             'position': journal_data.group('position'),
                                             'year': year if year is not None else ref_data['year']})
        references.append(ref_data)
    return references


def aggregate_results(references):
    agg = {}
    for ref in references:
        for journal in ref['journals']:
            if (journal['year'], journal['position']) in agg.keys():
                agg[(journal['year'], journal['position'])]['count'] += 1
            else:
                agg[(journal['year'], journal['position'])] = {'count': 1,
                                                               'year': journal['year'],
                                                               'position': journal['position']}
    return agg
