import langumo_ko.utils as utils
from langumo_ko.moducorpus.base import ModuBaseParser


class ModuWrittenParser(ModuBaseParser):
    pass


class ModuWebParser(ModuBaseParser):
    def parse(self, text: str) -> str:
        return super().parse(
            '\n'.join([line.strip() for line in text.splitlines()
                       if utils.korean_character_ratio(line) > 0.5]))


class ModuNewsParser(ModuBaseParser):
    def parse(self, text: str) -> str:
        # Skip the contents which contain too many non-Korean characters.
        if utils.korean_character_ratio(text) < 0.5:
            return ''

        # Normalize the contents by removing abnormal sentences.
        text = '\n'.join([
            line for line in text.splitlines()
            if utils.is_normal_character(line[0]) and line[-1] == '.'])

        return super().parse(text)
