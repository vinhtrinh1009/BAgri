'''
String utilities

References:
- Ants Aasma - [Answer in StackOverflow](https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python)
'''

import unicodedata, re, itertools, sys

all_chars = (chr(i) for i in range(sys.maxunicode))
categories = {'Cc'}
control_chars = ''.join(c for c in all_chars if unicodedata.category(c) in categories)
# or equivalently and much more efficiently
control_chars = ''.join(map(chr, itertools.chain(range(0x00,0x20), range(0x7f,0xa0))))

control_char_re = re.compile('[%s]' % re.escape(control_chars))

def remove_control_chars(s):
    """Remove control characters (non-printable characters) in string"""
    return control_char_re.sub('', s)


def remove_duplicated_space(s):
    return re.sub(r'\s+', ' ', s)


def split_lines(text, max_characters_per_lines=40, max_lines=2):
    '''
    Split long text into lines. Append '...' if the text is too long.
    '''
    words = text.split(' ')

    start = 0
    end = 0
    count_chars = 0
    count_lines = 0
    max_lines = max_lines

    lines = []
    for w in words:
        len_w = len(w)
        if count_chars + len_w <= max_characters_per_lines:
            count_chars += len_w + 1
        else:
            # create a line
            if count_lines < max_lines:
                end = start + count_chars
                lines.append(text[start:end])

                start = end
                count_chars = 0
                count_lines += 1
            else:
                # too many lines, must skip the overflow
                if len(lines) > 0:
                    lines[-1] += '...'
                break
    
    if count_chars > 0 and count_lines < max_lines:
        lines.append(text[start:])
    
    return lines


def is_youtube_video_url(url):
    pattern = r'http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?'

    found = re.search(pattern, url)

    return True if found else False


def parse_bool(data, key, default=False, raise_exc=False):
    if data.get(key, '').lower() in ('1', 'true'):
        return True
    elif data.get(key, '').lower() in ('0', 'false'):
        return False
    else:
        if raise_exc:
            raise Exception(f"Unable to parse value with key '{key}'")
    return default


def parse_int(data, key, raise_exc=False, default=None):
    try:
        return int(data[key])
    except (ValueError, KeyError) as e:
        if raise_exc:
            raise e
    
    return default