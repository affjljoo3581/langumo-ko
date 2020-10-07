import re
import ijson
from typing import Iterable
import langumo_ko.utils as utils
from langumo.building import Parser
from langumo.utils import AuxiliaryFile
from langumo_ko.namuwiki.rendering import NamuWikiRenderer


class NamuWikiParser(Parser):
    single_quotes_pattern = re.compile('[\x60\xb4\u2018\u2019]')
    double_quotes_pattern = re.compile('[\u201c\u201d]')

    def extract(self, raw: AuxiliaryFile) -> Iterable[str]:
        with raw.open('r') as fp:
            for prefix, event, value in ijson.parse(fp):
                if not prefix.endswith('.text'):
                    continue

                # Skip the redirection pages.
                if value.lower().strip().startswith('#redirect'):
                    continue

                yield value

    def parse(self, text: str) -> str:
        text = NamuWikiRenderer.render(text)
        text = utils.normalize_quotes(text)
        text = utils.remove_duplicated_spaces(text)

        return '\n'.join([line for line in text.splitlines()
                          if '.' in line
                          and utils.korean_character_ratio(line) > 0.1])
