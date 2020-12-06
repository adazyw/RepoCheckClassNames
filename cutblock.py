"""
>>> remove_block([ '' ], '<', '>')
['']
>>> remove_block([ 'classname<GenericType>' ], '<', '>')
['classname']
>>> remove_block([ 'firstline', 'classname<GenericType>', 'lastline' ], '<', '>') # doctest: +NORMALIZE_WHITESPACE
['firstline', 'classname', 'lastline']
>>> remove_block([ 'firstline<', 'classname', '>lastline' ], '<', '>') # doctest: +NORMALIZE_WHITESPACE
['firstline', 'lastline']
>>> remove_block([ 'firstline<', 'classname<Type>', '>lastline' ], '<', '>') # doctest: +NORMALIZE_WHITESPACE
['firstline', 'lastline']
"""
from typing import List


def remove_block(processed: List[str], start: str, end: str, file_name: str = '') -> str:
    if len(start) <= 0 or len(end) <= 0:
        raise AttributeError

    result = []
    start_end_ct = 0
    for line in processed:
        if len(line) <= 0 and start_end_ct == 0:
            result.append(line)
            continue

        line_to_append = []
        i = 0
        line_len = len(line)

        while i < line_len:
            if i <= len(line) - len(start) and line[i:i+len(start)] == start:
                start_end_ct += 1
                i += len(start)
                continue

            if start_end_ct > 0 and i <= len(line) - len(end) and line[i:i+len(end)] == end:
                start_end_ct -= 1
                i += len(end)
                continue

            if start_end_ct == 0:
                # Zapisz znak
                line_to_append.append(line[i])
            i += 1

        if len(line_to_append) > 0:
            result.append(''.join(line_to_append))

    return result

# def remove_block(processed: List[str], start: str, end: str, file_name: str = '') -> str:
#     start_id = None
#     end_id = None
#
#     result = []
#     for i, line in enumerate(processed):
#
#         # TODO policzyć otwierające i zamykające; zawsze wycinać od zewnętrznych
#         # Uwaga: zabezpieczyć się przed powtórzeniami w rodzaju ./././ przy './.'
#
#         if start_id is None:
#             found = line.find(start)
#             if found < 0:
#                 result.append(line)
#                 continue
#
#             start_id = (i, found)
#             result.append(line[:found])
#
#         found = line.find(end)
#         if found < 0:
#             continue
#         if found + 1 < len(line):
#             trimmed_line = line[found + 1:]
#             if len(result) > 0 and start_id[0] == i:
#                 result[-1] = str.join(result[-1], trimmed_line)
#             else:
#                 result.append(trimmed_line)
#
#         start_id = None
#
#     if start_id is not None:
#         print(f'Warning! End index not found: {start_id} {file_name}')
#         return processed
#     return result

