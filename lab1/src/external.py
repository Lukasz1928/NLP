import regex

from src.utils import omit_header


def find_external_references(data, filename):
    references = []
    for d in data:
        references.append(find_external_in_single_file(d))
    aggregated = aggregate_results(references)
    print(aggregated)


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
    main_text = omit_header(text)

    date_regex = r'\bz\s*\bdnia\b\s*(?P<day>\d{1,2})\s*(?P<month>\d{1,2}|\b\w*\b)\s*(?P<year>\d{4})\s*r(oku|\.)\s*'
    journal_regex = r'\([Dd]z((iennik)\w*|\.)\s*U(staw|\.)\s*(?P<journal_details>.*?)\)'
    title_regex = r'(?P<title>((\bo\b)|-)\s*.*?)(?=\s*\()'
    journal_details_regex = r'(Nr\s*(?P<journal_number>\d+),)?\s*poz\.\s*(?P<journal_position>\d+)'

    reference_regex = r'\b[Uu]staw\w*\s*(({})?({})?){{,2}}({})'.format(date_regex, title_regex, journal_regex)

    references = []
    for ref in regex.finditer(reference_regex, main_text, regex.MULTILINE | regex.DOTALL):
        ref_data = {}
        ref_data['day'] = ref.group('day')
        ref_data['month'] = ref.group('month')
        ref_data['year'] = ref.group('year')
        ref_data['title'] = format_title(ref.group('title'))
        ref_data['journals'] = []
        for j in regex.finditer(journal_details_regex, ref.group('journal_details'), regex.MULTILINE | regex.DOTALL):
            ref_data['journals'].append({'number' : j.group('journal_number'), 'position': j.group('journal_position')})
        references.append(ref_data)
    return references


def aggregate_results(references):
    return references