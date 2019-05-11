import json


class Results:
    def __init__(self):
        self.results = {
            'svm': {
                'full_text': {'accuracy': None, 'recall': None, 'f1': None},
                'tenth_of_text': {'accuracy': None, 'recall': None, 'f1': None},
                'ten_lines_of_text': {'accuracy': None, 'recall': None, 'f1': None},
                'single_line_of_text': {'accuracy': None, 'recall': None, 'f1': None}
            },
            'fasttext': {
                'full_text': {'accuracy': None, 'recall': None, 'f1': None},
                'tenth_of_text': {'accuracy': None, 'recall': None, 'f1': None},
                'ten_lines_of_text': {'accuracy': None, 'recall': None, 'f1': None},
                'single_line_of_text': {'accuracy': None, 'recall': None, 'f1': None}
            },
            'flair': {
                'full_text': {'accuracy': None, 'recall': None, 'f1': None},
                'tenth_of_text': {'accuracy': None, 'recall': None, 'f1': None},
                'ten_lines_of_text': {'accuracy': None, 'recall': None, 'f1': None},
                'single_line_of_text': {'accuracy': None, 'recall': None, 'f1': None}
            }
        }

    def save(self, file):
        with open('results/{}'.format(file), 'w+', encoding='utf-8') as f:
            results_str = json.dumps(self.results, indent=2, ensure_ascii=False)
            f.write(results_str)
