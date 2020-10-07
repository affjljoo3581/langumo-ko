import re


_single_quotes_pattern = re.compile('[\x60\xb4\u2018\u2019]')
_double_quotes_pattern = re.compile('[\u201c\u201d]')


def normalize_quotes(text: str) -> str:
    text = _single_quotes_pattern.sub('\'', text)
    text = _double_quotes_pattern.sub('"', text)
    return text


def remove_duplicated_spaces(text: str) -> str:
    text = text.replace('\t', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text


def korean_character_ratio(text: str, ignore_whitespace: bool = True) -> float:
    if ignore_whitespace:
        text = ''.join(text.split())

    korean_characters = len([
        c for c in text if ord('가') <= ord(c) <= ord('힣')])
    return korean_characters / len(text) if len(text) > 0 else 0


def is_normal_character(c: str) -> bool:
    return (ord('0') <= ord(c) <= ord('9')
            or ord('a') <= ord(c) <= ord('z')
            or ord('A') <= ord(c) <= ord('Z')
            or ord('가') <= ord(c) <= ord('힣'))
