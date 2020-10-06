import langumo_ko.utils as utils
from langumo_ko.moducorpus.base import ModuBaseParser


class ModuWrittenParser(ModuBaseParser):
    def parse(self, text: str) -> str:
        return text


class ModuWebParser(ModuBaseParser):
    def parse(self, text: str) -> str:
        return text


class ModuNewsParser(ModuBaseParser):
    def parse(self, text: str) -> str:
        text = '\n'.join([line.strip() for line in text.splitlines()
                          if line.strip()])

        # Skip the contents which contain too many non-Korean characters.
        if utils.korean_character_ratio(text) < 0.5:
            return ''

        # Normalize the contents by removing abnormal sentences.
        text = '\n'.join([
            line for line in text.splitlines()
            if utils.is_normal_character(line[0]) and line[-1] == '.'])

        return text
