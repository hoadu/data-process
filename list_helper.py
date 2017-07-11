def slice_list(a_list, slice_count):
    head, tail = a_list[:slice_count], a_list[slice_count:]
    yield head
    while tail:
        head, tail = tail[:slice_count], tail[slice_count:]
        yield head

