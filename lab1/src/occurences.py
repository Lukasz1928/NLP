import regex


def count_ustawa_occurrences(data, filename="occurences"):
    text = merge_data(data)
    search_regex = r'(\b[Uu][Ss][Tt][Aa][Ww]([Aa]|[Aa][Cc][Hh]|[Aa][Mm][Ii]|[Ąą]|[Ęę]|[Ii][Ee]|[Oo][Mm]|[Oo]|[Yy])?\b)'
    occurrences = regex.findall(search_regex, text)
    lower_occurrences = [o[0].lower() for o in occurrences]
    unique_occurrences = set(lower_occurrences)
    unique_occurrences_count = {}
    for uo in unique_occurrences:
        unique_occurrences_count[uo] = lower_occurrences.count(uo)
    save_result(len(occurrences), unique_occurrences_count, filename)


def merge_data(data):
    s = ""
    for d in data:
        s += d
    return s


def save_result(all_count, inflected_count, filename):
    with open("results/{}.txt".format(filename), "w") as f:
        f.write("Total count of all forms of 'ustawa' word: {}\n".format(all_count))
        f.write("Total count of inflected forms of 'ustawa' word:\n")
        for uo in inflected_count:
            f.write("\t{}: {}\n".format(uo, inflected_count[uo]))
