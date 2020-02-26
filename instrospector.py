import inspect
import reprlib
import itertools


def full_sig(method):
    try:
        return method.__name__ + str(inspect.signature(method))
    except ValueError as e:
        return method.__name__ + '(...)'


def brief_doc(obj):
    doc = obj.__doc__
    if doc is not None:
        lines = doc.splitlines()
        if len(lines) > 0:
            return lines[0]
    return ''


def print_table(rows_of_columns, *headers):
    num_col = len(rows_of_columns[0])
    num_headers = len(headers)
    if num_headers != num_col:
        raise TypeError('Expected {} header arguments,'
                        'got {}.'.format(num_columns, num_headers))
    rows_of_columns_with_header = itertools.chain([headers], rows_of_columns)
    columns_of_rows = list(zip(*rows_of_columns_with_header))
    col_widths = [max(map(len, col)) for col in columns_of_rows]
    col_specs = ('{{:{w}}}'.format(w=width) for width in col_widths)
    format_spec = ' '.join(col_specs)
    print(format_spec.format(*headers))
    rules = ('-' * width for width in col_widths)
    print(format_spec.format(*rules))
    for row in rows_of_columns:
        print(format_spec.format(*row))


def dump(obj):
    print("Type")
    print("====")
    print(type(obj))
    print()

    print("Documentation")
    print("=============")
    print(inspect.getdoc(obj))
    print()

    print("Attributes")
    print("==========")
    all_attr = set(dir(obj))
    method_names = set(
        filter(lambda x: callable(getattr(obj, x)), all_attr))
    assert method_names <= all_attr
    attr_names = all_attr - method_names
    attr_nv = [(name, reprlib.repr(getattr(obj, name))) for name in attr_names]
    print_table(attr_nv, "Name", "Value")
    # print(type(obj))
    print()

    print("Methods")
    print("=======")
    methods = (getattr(obj, method_name) for method_name in method_names)
    methods_nd = [(full_sig(method), brief_doc(method)) for method in methods]
    print_table(methods_nd, "Name", "Description")
    print()
