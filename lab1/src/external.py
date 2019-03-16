import regex

from src.utils import omit_header


def find_external_references(data):
    references = []
    for d in data:
        references.append(find_external_in_single_file(d))
    return aggregate_results(references)


def find_external_in_single_file(text):
    main_text = omit_header(text)

    print(main_text)

    date_regex = r'\bz\s*\bdnia\b\s*(?P<day>\d{1,2})\s*(?P<month>\d{1,2}|\b\w*\b)\s*(?P<year>\d{4})\s*r(oku|\.)\s*'
    journal_regex = r'\([Dd]z((iennik)\w*|\.)\s*U(staw|\.)\s*(?P<journal_details>.*?)\)'
    title_regex = r'(?P<title>((\bo\b)|-)\s*.*?)(?=\s*\()'
    journal_details_regex = r'(Nr\s*(?P<journal_number>\d+),)?\s*poz\.\s*(?P<journal_position>\d+)'
    title_detailed_regex = r'^-'

    reference_regex = r'\b[Uu]staw\w*\s*(({})?({})?){{,2}}({})'.format(date_regex, title_regex, journal_regex)

    references = []
    for ref in regex.finditer(reference_regex, main_text, regex.MULTILINE | regex.DOTALL):
        ref_data = {}
        ref_data['day'] = ref.group('day')
        ref_data['month'] = ref.group('month')
        ref_data['year'] = ref.group('year')
        ref_data['title'] = regex.sub(title_detailed_regex, '', ref.group('title')) if ref.group('title') is not None else None
        ref_data['journals'] = []
        for j in regex.finditer(journal_details_regex, ref.group('journal_details'), regex.MULTILINE | regex.DOTALL):
            ref_data['journals'].append({'number' : j.group('journal_number'), 'position': j.group('journal_position')})
        references.append(ref_data)
    return references


def aggregate_results(references):
    return references