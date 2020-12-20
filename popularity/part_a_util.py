def sort_dict_by_value_desc(dictionary):
    dictionary_sorted_keys = sorted(dictionary, key=dictionary.get, reverse=True)
    res = {}
    for r in dictionary_sorted_keys:
        res[r] = dictionary[r]
    return res


def report_if_field_is_unique(df):
    fields = df.columns.tolist()
    for field in fields:
        if len(df[field].unique()) == df.shape[0]:
            print("Field [", str(field), "] is unique")
        else:
            print("Field [", str(field), "] is NOT unique")


def get_country(string):
    if type(string) == str:
        a = string.split(", ")
        if len(a) == 3:
            return a[2]
        else:
            return "null_country"
    else:
        return "null_country"
