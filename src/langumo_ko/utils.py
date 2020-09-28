

def korean_character_ratio(text: str, ignore_whitespace: bool = True) -> float:
    if ignore_whitespace:
        text = ''.join(text.split())

    korean_characters = len([
        c for c in text if ord('가') <= ord(c) <= ord('힣')])
    return korean_characters / len(text) if len(text) > 0 else 0
